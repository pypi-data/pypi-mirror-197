from typing import Iterable, Iterator, List, Optional, Sized, Tuple, TypeVar, Union

import numpy as np
from torchdata.dataloader2 import DataLoader2
from torchdata.dataloader2.adapter import Adapter
from torchdata.dataloader2.reading_service import MultiProcessingReadingService
from torchdata.datapipes import functional_datapipe, DataChunk
from torchdata.datapipes.map import MapDataPipe
from torchdata.datapipes.iter import IterDataPipe

from pyPhasesML.DataAugmentation import DataAugmentation

T_co = TypeVar("T_co", covariant=True)
T = TypeVar("T")


# @functional_datapipe("batchFirst")
# class BatcherIterDataPipe(IterDataPipe[DataChunk]):
#     r"""
#     use the first dimension of the data as batch dimension
#     """
#     datapipe: IterDataPipe
#     batch_size: int
#     drop_last: bool

#     def __init__(
#         self,
#         datapipe: IterDataPipe,
#         batch_size: int,
#         count: int,
#         drop_last: bool = False,
#         wrapper_class=DataChunk,
#     ) -> None:
#         assert batch_size > 0, "Batch size is required to be larger than 0!"
#         super().__init__()
#         self.datapipe = datapipe
#         self.batch_size = batch_size
#         self.count = count
#         self.drop_last = drop_last
#         self.wrapper_class = wrapper_class

#     def __iter__(self) -> Iterator[DataChunk]:
#         batchX: List = []
#         batchY: List = []
#         for record in self.datapipe:
#             x, y = record
#             for i in range(len(x)):
#                 batchX.append(x[i])
#                 batchY.append(y[i])
#                 if len(batchX) == self.batch_size:
#                     yield self.wrapper_class((np.array(batchX), np.array(batchY)))
#                     batchX: List = []
#                     batchY: List = []
#         if len(batchX) > 0:
#             if not self.drop_last:
#                 yield self.wrapper_class((np.array(batchX), np.array(batchY)))

#     def __len__(self) -> int:
#         if self.drop_last:
#             return self.count // self.batch_size
#         else:
#             return (self.count + self.batch_size - 1) // self.batch_size

@functional_datapipe("batchFirst")
class BatcherMapDataPipe(MapDataPipe[DataChunk]):
    r"""
    batch the data by the first dimension
    """
    datapipe: MapDataPipe
    batch_size: int
    drop_last: bool

    def __init__(self,
                 datapipe: MapDataPipe[T],
                 batch_size: int,
                 drop_last: bool = False,
                 wrapper_class=DataChunk,
                 ) -> None:
        assert batch_size > 0, "Batch size is required to be larger than 0!"
        super().__init__()
        self.datapipe = datapipe
        self.batch_size = batch_size
        self.drop_last = drop_last
        self.wrapper_class = wrapper_class

    def __getitem__(self, index) -> DataChunk:
        batchX: List = []
        batchY: List = []
        indices = range(index * self.batch_size, (index + 1) * self.batch_size)
        try:
            for i in indices:
                X, Y = self.datapipe[i]
                if len(X) > 1:
                    raise Exception(f"Batches need to single dimension")
                batchX.append(X[0])
                batchY.append(Y[0])
            return self.wrapper_class((np.array(batchX), np.array(batchY)))
        except IndexError as e:
            if not self.drop_last and len(batchX) > 0:
                return self.wrapper_class((batchX, batchY))
            else:
                raise IndexError(f"Index {index} is out of bound.") from e

    def __len__(self) -> int:
        if isinstance(self.datapipe, Sized):
            if self.drop_last:
                return len(self.datapipe) // self.batch_size
            else:
                return (len(self.datapipe) + self.batch_size - 1) // self.batch_size
        else:
            raise TypeError("{} instance doesn't have valid length".format(type(self).__name__))


@functional_datapipe("unzipXY")
class ZipperMapDataPipe(MapDataPipe[Tuple[T_co, ...]]):
    datapipes: Tuple[MapDataPipe[T_co], ...]

    def __init__(self, datapipe: MapDataPipe[T_co]) -> None:
        self.datapipe = datapipe
        self.index = 0
        
    def __len__(self):
        return len(self.datapipe)

    def __getitem__(self, index) -> Tuple[T_co, ...]:
        x, y = zip(*self.datapipe[index])
        return np.array(x), np.array(y)


# @functional_datapipe("augment")
# class Augmentor(IterDataPipe):
#     datapipes: IterDataPipe

#     def __init__(self, datapipe: MapDataPipe[T_co], augmentation: DataAugmentation) -> None:
#         self.datapipe = datapipe
#         self.augmentation = augmentation

#     def __len__(self):
#         return len(self.datapipe)

#     def __iter__(self) -> int:
#         for r in self.datapipe:
#             yield self.augmentation(r)


@functional_datapipe("augment")
class Augmentor(MapDataPipe):
    datapipes: MapDataPipe

    def __init__(self, datapipe: MapDataPipe[T_co], augmentation: DataAugmentation, config) -> None:
        self.datapipe = datapipe
        self.augmentation = augmentation
        self.config = config

    def __getitem__(self, index) -> MapDataPipe[T_co]:
        return self.augmentation(self.datapipe[index], self.config, index)

    def __len__(self) -> MapDataPipe[T_co]:
        return len(self.datapipe)


@functional_datapipe("segmentWise")
class Segments(MapDataPipe):
    datapipes: MapDataPipe

    def __init__(self, datapipe: MapDataPipe[T_co], recordLengths, segmentLength) -> None:
        self.datapipe = datapipe
        self.segmentLength = segmentLength
        
        # shape = self.datapipe.dataExporterSignals.fileShape
        recordLengths = np.array(recordLengths)
        recordSegmentLength = recordLengths // segmentLength
        recordSegmentLengthIndex = np.insert(recordSegmentLength.cumsum(), 0, 0)
        segmentCount = sum(recordLengths) // segmentLength

        recordMaping = np.concatenate([np.array([i] * length) for i, length in enumerate(recordSegmentLength)])
        segmentIndexes = np.arange(segmentCount) - recordSegmentLengthIndex[recordMaping]
        # mapping returns for each segment the record and the segment index
        self.segmentMapping = np.hstack([recordMaping.reshape(-1, 1), segmentIndexes.reshape(-1, 1)])
        self.segmentCount = segmentCount

    def __len__(self):
        return self.segmentCount

    def __getitem__(self, index) -> Tuple[T_co, ...]:
        recordIndex, segmentIndex = self.segmentMapping[index]
        x, y = self.datapipe[recordIndex]
        x = x.reshape(-1, self.segmentLength, x.shape[-1])
        y = y.reshape(x.shape[0], -1, y.shape[-1])
        return x[segmentIndex], y[segmentIndex]


class AugmentationDataset(MapDataPipe):
    def __init__(self, dataExporterSignals, dataExporterFeatures):
        self.dataExporterSignals = dataExporterSignals
        self.dataExporterFeatures = dataExporterFeatures
        self.segmentMapping = None

    def __len__(self):
        return len(self.dataExporterSignals)

    def __getitem__(self, idx):
        segmentX, segmentY = self.dataExporterSignals[idx], self.dataExporterFeatures[idx]
        # convert to numpy arrays
        return np.array(segmentX), np.array(segmentY)

    def __iter__(self) -> int:
        for d in self:
            yield d


class AugmentationDataLoaderXY(DataLoader2):
    def __init__(
        self,
        datapipe: MapDataPipe,
        threads: int = None,
        pinMemory: bool = False,
        datapipe_adapter_fn: Optional[Union[Iterable[Adapter], Adapter]] = None,
    ) -> None:
        reading_service = None
        if threads is not None:
            reading_service = MultiProcessingReadingService(num_workers=threads, pin_memory=pinMemory)
        super().__init__(datapipe, datapipe_adapter_fn, reading_service)

    def __len__(self):
        return len(self.datapipe)

    def generator(self, wrapper=None):
        while True:
            for d in self:
                yield d if wrapper is None else wrapper(d)

    def __getitem__(self, idx):
        return self.datapipe[idx]
