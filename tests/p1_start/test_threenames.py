import sys
import subprocess

def test_threenames_exports():
    from awesome_math.p1_start import threenames as tn
    assert (tn.a, tn.b, tn.c) == ("PC", "Phone", "Tablet")

def test_threenames_script_output():
    proc = subprocess.run(
        [sys.executable, "-m", "awesome_math.p1_start.threenames"],
        capture_output=True, text=True, check=True
    )
    assert proc.stdout.strip() == "PC Phone Tablet"
