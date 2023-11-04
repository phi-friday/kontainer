from __future__ import annotations

from typing import Any, Callable

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tests.maybe.base import BaseTestContainer

from kontainer import undefined
from kontainer.maybe import Result


class TestResult(BaseTestContainer):
    container_type = Result

    @given(
        st.builds(
            lambda x, y: x(y),
            st.one_of(st.just(Exception), st.just(ValueError), st.just(TypeError)),
            st.integers(),
        ),
        st.builds(
            lambda x, y: x(y),
            st.one_of(st.just(Exception), st.just(ValueError), st.just(TypeError)),
            st.integers(),
        ),
    )
    def test_switch(self, value: Any, other: Any):
        return super().test_switch(value, other)

    def test_default_other(self):
        container = self.container_type(1, Exception())
        with pytest.raises(NotImplementedError):
            container.default_other(1)

    @pytest.mark.skip()
    def test_non_default_other(self): ...

    def test_map_default_other(self):
        container = self.container_type(1)
        with pytest.raises(NotImplementedError):
            container.map_default_other(lambda: 1)

    @pytest.mark.skip()
    def test_map_non_default_other(self, func: Callable[[], Any]): ...

    @given(
        st.builds(
            lambda x, y: x(y),
            st.one_of(st.just(Exception), st.just(ValueError), st.just(TypeError)),
            st.integers(),
        )
    )
    def test_unwrap_other(self, other: Exception):
        container = self.container_type(undefined, other)
        with pytest.raises(type(other)):
            container.unwrap_other()

    @pytest.mark.skip()
    def test_unwrap_other_error(self): ...

    @given(st.integers())
    def test_switch_non_error_value(self, value: Any):
        result = self.container_type(value, Exception())
        new = result.switch()
        with pytest.raises(
            TypeError, match="The type of value changed to other is not an error type."
        ):
            new.unwrap_other()
