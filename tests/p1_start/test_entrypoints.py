import importlib.metadata as m


def test_console_scripts_present():
    dist = m.distribution("awesome-math")
    eps = {ep.name: ep.value for ep in dist.entry_points if ep.group == "console_scripts"}
    # проверяем, что они объявлены и указывают на правильные функции
    assert eps["amath"] == "awesome_math.core:main"
    assert eps["script1"] == "awesome_math.p1_start.script1:main"
    assert eps["cycles"] == "awesome_math.p1_start.cycles:main"
