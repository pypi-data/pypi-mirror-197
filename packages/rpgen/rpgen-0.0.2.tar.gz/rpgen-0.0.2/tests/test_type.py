import unittest
import string

from rpgen.character_type import CharacterType
from rpgen.error_message import ErrorMessage


class TestCharacterType(unittest.TestCase):

    def setUp(self) -> None:
        self.uppercase = CharacterType(list(string.ascii_uppercase))

    def test_create_empty_condidate(self) -> None:
        expected = ErrorMessage.EMPTY_CANDIDATE.value

        with self.assertRaises(TypeError):
            self.uppercase = CharacterType()

        with self.assertRaisesRegex(ValueError, expected):
            self.uppercase = CharacterType([])

    def test_set_min_greater_than_max(self):
        expected = ErrorMessage.MIN_MAX_INVALID_RANGE.value

        for min in range(1, 10):
            with self.assertRaisesRegex(ValueError, expected):
                self.uppercase.min = min
                self.uppercase.max = min - 1

    def test_set_non_numberic_min_max(self) -> None:
        nums = ["123", "d", 'A', "$"]
        expected = ErrorMessage.MIN_MAX_NOT_NUMBERIC.value

        for num in nums:
            with self.assertRaisesRegex(ValueError, expected):
                self.uppercase.min = num

            with self.assertRaisesRegex(ValueError, expected):
                self.uppercase.max = num

    def test_set_negative_number_min_max(self) -> None:
        nums = [-1, -3, -11]
        expected = ErrorMessage.MIN_MAX_NAGATIVE.value

        for num in nums:
            with self.assertRaisesRegex(ValueError, expected):
                self.uppercase.min = num

            with self.assertRaisesRegex(ValueError, expected):
                self.uppercase.max = num

    def test_generate_characters(self) -> None:
        generate_length = self.uppercase.min
        self.uppercase.generate(generate_length)

        self.assertEqual(len(self.uppercase.characters), generate_length)

        for char in self.uppercase.characters:
            self.assertTrue(char in self.uppercase._candidate)

    def test_generate_characters_with_empty_candidate(self) -> None:
        expected = ErrorMessage.EMPTY_CANDIDATE.value
        self.uppercase._candidate = []

        with self.assertRaisesRegex(ValueError, expected):
            self.uppercase.generate(1)

    def test_generate_characters_with_out_of_range(self) -> None:
        expected = ErrorMessage.GENERATE_LENGTH_OUT_OF_RANGE.value

        for length in [self.uppercase.min - 1, self.uppercase.max + 1]:
            with self.assertRaisesRegex(ValueError, expected):
                self.uppercase.generate(length)

    def test_generate_characters_with_not_numberic(self) -> None:
        expected = ErrorMessage.GENERATE_LENGTH_NOT_NUMBERIC.value
        nums = ["123", "d", 'A', "$"]

        for num in nums:
            with self.assertRaisesRegex(ValueError, expected):
                self.uppercase.generate(num)

    def test_generate_characters_with_loop(self) -> None:
        for _ in range(3):
            self.uppercase.generate(self.uppercase.max)

            length = len(self.uppercase.characters)
            self.assertEqual(length, self.uppercase.max)


if __name__ == '__main__':
    unittest.main()
