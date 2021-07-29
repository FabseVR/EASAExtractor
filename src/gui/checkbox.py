from enum import Enum


class CHECKBOX(Enum):
    CHECKED_OPEN = 0
    CHECKED_CLOSED = 1
    UNCHECKED_OPEN = 2
    UNCHECKED_CLOSED = 3

    def __invert__(self):
        return CHECKBOX((self.value + 2) % 4)

    def __bool__(self):
        return self.value < 2

    def __str__(self):
        return self.name

    def __lt__(self, b):
        return (self.value % 2, self.value) < (b.value % 2, b.value)

    def as_icon(self):
        return "\u2611" if bool(self) else "\u2610"
