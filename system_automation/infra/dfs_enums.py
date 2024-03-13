from enum import Enum


class ResponseFields(Enum):
    STATUS = "Status"
    OUTPUT = "Output"
    IN_PROGRESS = "In Progress"


class ScannerTestDelta(Enum):
    ABS_MIRROR_SHIFT = 0
    SET_ACTIVE_PATTERN = 1.0
    SET_SCANNER_ZEINIT = 0.01

