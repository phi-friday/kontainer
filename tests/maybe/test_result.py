from __future__ import annotations

from typing import Any

import pytest

from tests.maybe.base import BaseTestContainer

from kontainer.maybe import Result


class TestResult(BaseTestContainer):
    container_type = Result

    @pytest.mark.parametrize(
        ("value", "other"),
        [
            (ValueError(1), Exception(4)),
            (TypeError(2), ValueError(5)),
            (Exception(3), TypeError(6)),
        ],
    )
    def test_switch(self, value: Any, other: Any):
        return super().test_switch(value, other)
