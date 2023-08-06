import string
import unittest
import random

from rpgen.password_generator import PasswordGenerator
from rpgen.error_message import ErrorMessage


class TestPasswordGenerator(unittest.TestCase):

    def setUp(self) -> None:
        self.generator = PasswordGenerator()

    def test_generator_contains_common_character_type(self) -> None:
        common_types = [
            ('uppercase', list(string.ascii_uppercase)),
            ('lowercase', list(string.ascii_lowercase)),
            ('digits', list(string.digits)),
            ('special', list(set(string.punctuation)))
        ]

        for name, candidate in common_types:
            self.assertListEqual(
                self.generator.types[name].candidate, candidate)

    def test_set_min_greater_than_max(self):
        expected = ErrorMessage.MIN_MAX_INVALID_RANGE.value

        for min in range(2, 10):
            with self.assertRaisesRegex(ValueError, expected):
                self.generator.min = min
                self.generator.max = min - 1

    def test_set_non_numberic_min_max(self) -> None:
        nums = ["123", "d", 'A', "$"]
        expected = ErrorMessage.MIN_MAX_NOT_NUMBERIC.value

        for num in nums:
            with self.assertRaisesRegex(ValueError, expected):
                self.generator.min = num

            with self.assertRaisesRegex(ValueError, expected):
                self.generator.max = num

    def test_set_min_with_negative_number(self) -> None:
        nums = [-1, -3, -11]
        expected = ErrorMessage.MIN_MAX_NAGATIVE.value

        for num in nums:
            with self.assertRaisesRegex(ValueError, expected):
                self.generator.min = num

    def test_set_max_with_zero_number(self) -> None:
        expected = ErrorMessage.GENERATOR_MAX_NOT_POSITIVE.value

        with self.assertRaisesRegex(ValueError, expected):
            self.generator.max = 0

    def test_sum_char_type_length_range(self) -> None:
        expected_min = 0
        expected_max = 0

        for type in self.generator.types.values():
            type.min = random.randrange(0, 5)
            expected_min += type.min

            type.max = random.randrange(5, 9)
            expected_max += type.max

        self.assertTupleEqual(
            self.generator.sum_range(),
            (expected_min, expected_max))

    def test_sum_char_type_length_range_with_empty_types(self) -> None:
        expected = ErrorMessage.EMPTY_CHAR_TYPE_LIST.value
        self.generator.types = []

        with self.assertRaisesRegex(ValueError, expected):
            self.generator.sum_range()

    def test_sum_char_type_length_range_with_other_types(self) -> None:
        expected = ErrorMessage.NOT_CHARACTER_TYPE.value
        other_types = ["str", 1, [1, 2], {"test": "t"}]

        for other_type in other_types:
            self.generator.types["none_character_type"] = other_type

            with self.assertRaisesRegex(TypeError, expected):
                self.generator.sum_range()

    def test_adjust_length_range_with_worng_length_range(self) -> None:
        min, max = self.generator.sum_range()

        self.generator.min = 0
        self.generator.max = min - 1

        expected = ErrorMessage.GENERATOR_MAX_LT_CHAR_TYPE_MIN.value

        with self.assertRaisesRegex(ValueError, expected):
            self.generator.adjust_length(min, max)

        self.generator.max = max + 2
        self.generator.min = max + 1

        expected = ErrorMessage.GENERATOR_MIN_GT_CHAR_TYPE_MAX.value

        with self.assertRaisesRegex(ValueError, expected):
            self.generator.adjust_length(min, max)

    def test_adjust_length_range_with_zero_max(self) -> None:
        expected = ErrorMessage.ADJUST_MAX_IS_ZERO.value

        for type in self.generator.types.values():
            type.min = 0
            type.max = 0

        min, max = self.generator.sum_range()

        with self.assertRaisesRegex(ValueError, expected):
            self.generator.adjust_length(min, max)

    def test_adjust_length_range(self) -> None:
        range = [
            (self.generator.min - 1, self.generator.max - 1),
            (self.generator.min + 1, self.generator.max - 1),
            (self.generator.min + 1, self.generator.max + 1)
        ]

        expected = [
            (self.generator.min, self.generator.max - 1),
            (self.generator.min + 1, self.generator.max - 1),
            (self.generator.min + 1, self.generator.max)
        ]

        for r, e in zip(range, expected):
            min, max = self.generator.adjust_length(r[0], r[1])
            self.assertTupleEqual((min, max), e)

    def test_generate_character_list(self) -> None:
        length = random.randrange(self.generator.min, self.generator.max + 1)
        character_list = self.generator.generate_character_list(length)

        self.assertEqual(len(character_list), length)

    def test_generate_with_loop(self) -> None:
        for _ in range(self.generator.max):
            length = len(self.generator.generate())

            self.assertLessEqual(length, self.generator.max)
            self.assertGreaterEqual(length, self.generator.min)


if __name__ == '__main__':
    unittest.main()
