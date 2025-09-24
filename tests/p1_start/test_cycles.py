import sys
import subprocess
import copy
import json
import pickle
import pytest

from awesome_math.p1_start.cycles import make_cycle

def test_cycle_structure_and_identity():
    L = make_cycle()
    assert L[:2] == [1, 2]
    assert L[-1] is L                 # самоссылка сохранена

def test_cycle_repr_is_finite():
    L = make_cycle()
    assert repr(L) == "[1, 2, [...]]" # стандартный repr для циклических списков

def test_deepcopy_preserves_cycle():
    L = make_cycle()
    L2 = copy.deepcopy(L)
    assert L2 is not L
    assert L2[:2] == [1, 2]
    assert L2[-1] is L2               # цикл сохранился в копии

def test_json_fails_on_cycle():
    L = make_cycle()
    with pytest.raises(ValueError):   # json не умеет циклы по умолчанию
        json.dumps(L)

def test_pickle_roundtrip_cycle():
    L = make_cycle()
    blob = pickle.dumps(L)
    L3 = pickle.loads(blob)
    assert L3[:2] == [1, 2]
    assert L3[-1] is L3               # pickle умеет циклы

def test_script_output_via_module_run():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p2_objects.cycles"],
        capture_output=True, text=True, check=True
    )
    assert proc.stdout.strip() == "[1, 2, [...]]"
