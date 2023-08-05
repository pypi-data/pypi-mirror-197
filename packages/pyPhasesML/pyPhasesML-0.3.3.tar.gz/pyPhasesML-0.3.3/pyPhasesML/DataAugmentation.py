import numpy as np
from numpy.random import default_rng
from pyPhases import classLogger


@classLogger
class DataAugmentation:
    def __init__(self, config, splitName) -> None:
        self.segmentAugmentation = config["segmentAugmentation"]
        self.recordAugmentation = config["recordAugmentation"]
        self.config = config
        self.splitName = splitName

    def step(self, stepname, X, Y, index=None, **options):
        # check if augmentation step exist
        self.currentIndex = index
        if hasattr(self, stepname):
            # call method
            return getattr(self, stepname)(X, Y, **options)
        else:
            raise Exception(f"DataAugmentation {stepname} not found")

    def __call__(self, Segment, config=None, index=None):
        X, Y = Segment
        config = config or {}
        return self.augmentByConfig(X, Y, config, index)

    def augmentSegment(self, X, Y, index=None):
        return self.augmentByConfig(X, Y, self.segmentAugmentation, index)

    def augmentRecord(self, X, Y, index=None):
        return self.augmentByConfig(X, Y, self.recordAugmentation, index)

    def augmentByConfig(self, X, Y, config, index=None):
        X = np.expand_dims(X, axis=0)
        Y = np.expand_dims(Y, axis=0)

        for c in config:
            X, Y = self.loadFromConfig(c, X, Y, self.splitName, index)

        return X, Y

    def loadFromConfig(self, config, X, Y, splitName, index=None):
        config = config.copy()
        name = config["name"]
        ignoreChannels = config["ignoreChannels"] if "ignoreChannels" in config else None
        del config["name"]

        if "trainingOnly" in config:
            if config["trainingOnly"] and splitName != "training":
                return X, Y
            del config["trainingOnly"]

        # remove ignored channels for augmentation
        if ignoreChannels is not None:
            ignored = X[:, :, ignoreChannels]
            X = np.delete(X, ignoreChannels, axis=2)
            del config["ignoreChannels"]

        X, Y = self.step(name, X, Y, index, **config)

        # add ignored channels back
        if ignoreChannels is not None:
            X = np.insert(X, ignoreChannels, ignored, axis=2)

        return X, Y
