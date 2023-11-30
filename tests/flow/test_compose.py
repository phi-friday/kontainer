"""https://raw.githubusercontent.com/dbrattli/Expression/main/tests/test_compose.py"""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from kontainer import catch, compose_bind_funcs, compose_funcs


def identity(x):
    return x


def fn(x: int) -> int:
    return x + 42


def gn(x: int) -> int:
    return x - 3


def hn(x: int) -> int:
    return x * 2


identity_bind = catch(identity)
fn_bind = catch(fn)
gn_bind = catch(gn)
hn_bind = catch(hn)


@given(st.integers())
def test_compose_identity_implicit(x: int):
    fn = compose_funcs()

    assert fn(x) == x


@given(st.integers())
def test_compose_identity(x: int):
    fn = compose_funcs(identity)

    assert fn(x) == x


@given(st.integers())
def test_compose_1(x: int):
    gn = compose_funcs(fn)

    assert gn(x) == fn(x) == x + 42


@given(st.integers())
def test_compose_2(x: int):
    hn = compose_funcs(fn, gn)

    assert hn(x) == gn(fn(x))


@given(st.integers())
def test_compose_3(x: int):
    cn = compose_funcs(fn, gn, hn)

    assert cn(x) == hn(gn(fn(x)))


@given(st.integers())
def test_compose_many(x: int):
    cn = compose_funcs(fn, gn, hn, fn, hn, gn, fn)

    assert cn(x) == fn(gn(hn(fn(hn(gn(fn(x)))))))


@given(st.integers())
def test_compose_rigth_identity(x: int):
    cn = compose_funcs(fn, identity)

    assert cn(x) == fn(x)


@given(st.integers())
def test_compose_left_identity(x: int):
    cn = compose_funcs(identity, fn)

    assert cn(x) == fn(x)


@given(st.integers(), st.integers(), st.integers())
def test_compose_associative(x: int, y: int, z: int):
    """Rearranging the parentheses in an expression will not change the result."""

    def _fn(a: int) -> int:
        return a + x

    def _gn(a: int) -> int:
        return a - y

    def _hn(a: int) -> int:
        return a * z

    cn = compose_funcs(_fn, _gn, _hn)

    def _cn(a: int) -> int:
        return _hn(_gn(_fn(a)))

    rn = compose_funcs(_fn, compose_funcs(_gn, _hn))

    # right associative
    def _rn(a: int) -> int:
        def _rnn(b: int) -> int:
            return _hn(_gn(b))

        return _rnn(_fn(a))

    ln = compose_funcs(compose_funcs(_fn, _gn), _hn)

    # left associative
    def _ln(a: int) -> int:
        def _lnn(b: int) -> int:
            return _gn(_fn(b))

        return _hn(_lnn(a))

    assert cn(x) == _cn(x) == rn(x) == _rn(x) == ln(x) == _ln(x)


@given(st.integers())
def test_compose_bind_identity_implicit(x: int):
    fn = compose_bind_funcs()
    result = fn(x)

    assert result.unwrap() == x


@given(st.integers())
def test_compose_bind_identity(x: int):
    fn = compose_bind_funcs(identity_bind)
    result = fn(x)

    assert result.unwrap() == x


@given(st.integers())
def test_compose_bind_1(x: int):
    gn = compose_bind_funcs(fn_bind)

    assert gn(x).unwrap() == fn_bind(x).unwrap() == x + 42


@given(st.integers())
def test_compose_bind_2(x: int):
    hn = compose_bind_funcs(fn_bind, gn_bind)

    assert hn(x).unwrap() == gn_bind(fn_bind(x).unwrap()).unwrap()


@given(st.integers())
def test_compose_bind_3(x: int):
    cn = compose_bind_funcs(fn_bind, gn_bind, hn_bind)

    assert cn(x).unwrap() == hn_bind(gn_bind(fn_bind(x).unwrap()).unwrap()).unwrap()


@given(st.integers())
def test_compose_bind_many(x: int):
    cn = compose_bind_funcs(
        fn_bind, gn_bind, hn_bind, fn_bind, hn_bind, gn_bind, fn_bind
    )

    assert cn(x) == fn_bind(
        gn_bind(
            hn_bind(
                fn_bind(
                    hn_bind(gn_bind(fn_bind(x).unwrap()).unwrap()).unwrap()
                ).unwrap()
            ).unwrap()
        ).unwrap()
    )


@given(st.integers())
def test_compose_bind_rigth_identity(x: int):
    cn = compose_bind_funcs(fn_bind, identity_bind)

    assert cn(x).unwrap() == fn_bind(x).unwrap()


@given(st.integers())
def test_compose_bind_left_identity(x: int):
    cn = compose_bind_funcs(identity_bind, fn_bind)

    assert cn(x).unwrap() == fn_bind(x).unwrap()


@given(st.integers(), st.integers(), st.integers())
def test_compose_bind_associative(x: int, y: int, z: int):
    """Rearranging the parentheses in an expression will not change the result."""

    @catch
    def _fn(a: int) -> int:
        return a + x

    @catch
    def _gn(a: int) -> int:
        return a - y

    @catch
    def _hn(a: int) -> int:
        return a * z

    cn = compose_bind_funcs(_fn, _gn, _hn)

    @catch
    def _cn(a: int) -> int:
        return _hn(_gn(_fn(a).unwrap()).unwrap()).unwrap()

    rn = compose_bind_funcs(_fn, compose_bind_funcs(_gn, _hn))

    # right associative
    @catch
    def _rn(a: int) -> int:
        @catch
        def _rnn(b: int) -> int:
            return _hn(_gn(b).unwrap()).unwrap()

        return _rnn(_fn(a).unwrap()).unwrap()

    ln = compose_bind_funcs(compose_bind_funcs(_fn, _gn), _hn)

    # left associative
    @catch
    def _ln(a: int) -> int:
        @catch
        def _lnn(b: int) -> int:
            return _gn(_fn(b).unwrap()).unwrap()

        return _hn(_lnn(a).unwrap()).unwrap()

    assert (
        cn(x).unwrap()
        == _cn(x).unwrap()
        == rn(x).unwrap()
        == _rn(x).unwrap()
        == ln(x).unwrap()
        == _ln(x).unwrap()
    )
