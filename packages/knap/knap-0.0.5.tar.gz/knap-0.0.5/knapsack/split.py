from enum import Enum


class Split(Enum):
    NONE = "none"
    TRAIN = "train"
    VAL = "val"
    TEST = "test"

    def __str__(self):
        return str(self.value)
