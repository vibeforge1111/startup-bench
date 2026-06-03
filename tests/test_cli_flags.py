import subprocess
def test_bench_help():
    r = subprocess.run(["python3","-m","thestartupbench.cli","--help"], capture_output=True, timeout=5)
    assert r.returncode == 0
