from rpgen.error_message import ErrorMessage
from random import choice


class CharacterType:

    def __init__(self, candidate: list) -> None:
        self.validate_candidate(candidate)

        self._candidate: list = candidate
        self._min: int = 1
        self._max: int = 16
        self.characters: list = []

    def validate_candidate(self, candidate: list) -> None:
        if not candidate:
            raise ValueError(ErrorMessage.EMPTY_CANDIDATE.value)

    def validate_range(self, min: int, max: int) -> None:
        if type(min) != int or type(max) != int:
            raise ValueError(ErrorMessage.MIN_MAX_NOT_NUMBERIC.value)

        if min < 0 or max < 0:
            raise ValueError(ErrorMessage.MIN_MAX_NAGATIVE.value)

        if min > max:
            raise ValueError(ErrorMessage.MIN_MAX_INVALID_RANGE.value)

    def validate_length(self, length: int) -> None:
        if type(length) != int:
            raise ValueError(ErrorMessage.GENERATE_LENGTH_NOT_NUMBERIC.value)

        if length < self.min or length > self.max:
            raise ValueError(ErrorMessage.GENERATE_LENGTH_OUT_OF_RANGE.value)

    @property
    def min(self) -> int:
        return self._min

    @min.setter
    def min(self, value: int) -> None:
        self.validate_range(value, self._max)
        self._min = value

    @property
    def max(self) -> int:
        return self._max

    @max.setter
    def max(self, value: int) -> None:
        self.validate_range(self._min, value)
        self._max = value

    @property
    def candidate(self) -> list:
        return self._candidate

    def generate(self, length: int) -> None:
        self.validate_candidate(self._candidate)
        self.validate_length(length)

        for _ in range(length):
            self.characters.append(choice(self._candidate))
