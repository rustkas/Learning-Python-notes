# pylint: disable=missing-function-docstring
import pytest

import awesome_math.p17.scopes_basics as sb


def test_legb_read_and_local_shadow():
    sb.reset_global()
    assert sb.read_global() == "Hack"
    assert sb.write_local_shadow() == "Py!"
    # глобальное значение осталось прежним
    assert sb.read_global() == "Hack"


def test_global_modify_and_reset():
    sb.set_global("Py!")
    assert sb.read_global() == "Py!"
    sb.reset_global()
    assert sb.read_global() == "Hack"


def test_enclosing_reference_closure():
    assert sb.closure_read() == "Py!"


def test_nonlocal_counter_per_call_state():
    c1 = sb.make_counter(0)
    assert c1("a") == ("a", 1)
    assert c1("b") == ("b", 2)

    c2 = sb.make_counter(24)
    assert c2("x") == ("x", 25)

    # состояние раздельное
    assert c1("c") == ("c", 3)
    assert c2("y") == ("y", 26)


def test_function_attribute_counter():
    c1 = sb.make_counter_attr(0)
    assert c1("a") == ("a", 1)
    assert c1("b") == ("b", 2)

    c2 = sb.make_counter_attr(24)
    assert c2("x") == ("x", 25)

    assert c1("c") == ("c", 3)
    assert c2("y") == ("y", 26)

    # внешний доступ к состоянию возможен
    assert getattr(c1, "state") == 3
    assert getattr(c2, "state") == 26


def test_outer_bad_raises_unboundlocal():
    f = sb.outer_bad(0)
    with pytest.raises(UnboundLocalError):
        f("boom")


def test_loop_closure_capture_bad_vs_good():
    bad = sb.make_actions_bad()
    vals_bad = [fn(2) for fn in bad]
    assert vals_bad == [16, 16, 16, 16, 16]  # везде последнее i == 4

    good = sb.make_actions_good()
    vals_good = [fn(2) for fn in good]
    assert vals_good == [i * i for i in range(5)]
