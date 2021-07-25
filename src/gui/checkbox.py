from enum import Enum


class CHECKBOX(Enum):
    CHECKED = "\u2611"
    UNCHECKED = "\u2610"

    def __invert__(self):
        return CHECKBOX.UNCHECKED if self else CHECKBOX.CHECKED

    def __bool__(self):
        return self == CHECKBOX.CHECKED

    def __str__(self):
        return self.value

    def __lt__(self, b):
        return self == CHECKBOX.CHECKED and b == CHECKBOX.UNCHECKED

    def as_tag(self):
        return "CHECKED" if bool(self) else "UNCHECKED"

