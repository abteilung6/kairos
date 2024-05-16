from dataclasses import dataclass

import pytest


@dataclass
class TestCase:
    test_name: str

    __test__ = False

    def __str__(self) -> str:
        return self.test_name

    @staticmethod
    def parametrize(*test_cases: tuple) -> pytest.MarkDecorator:
        return pytest.mark.parametrize("test_case", test_cases, ids=str)
