# run_all.py - Sequential pipeline runner.
# Log written to: C:/Users/maor1/pipeline_run.log
# Watch with: Get-Content C:\Users\maor1\pipeline_run.log -Wait
import subprocess
import sys
import os
from pathlib import Path

os.chdir(Path(__file__).parent)
LOG = Path("C:/Users/maor1/pipeline_run.log")

STEPS = [
    ("FACTORY",  [sys.executable, "prompt_factory1240 (1).py"]),
    ("JUDGE",    [sys.executable, "quality_judge.py"]),
    ("SPLIT",    [sys.executable, "split.py"]),
    ("EDA",      [sys.executable, "eda.py"]),
    ("REPORT",   [sys.executable, "report.py"]),
]

with open(LOG, "w", encoding="utf-8") as log:
    def w(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    w("=" * 60)
    w("PIPELINE START")
    w("=" * 60)

    for name, cmd in STEPS:
        w(f"\n>>> STEP: {name}")
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=Path(__file__).parent,
        )
        for line in proc.stdout:
            w(line.rstrip())
        proc.wait()
        if proc.returncode != 0:
            w(f"[ERROR] {name} exited with code {proc.returncode}. Stopping.")
            sys.exit(proc.returncode)
        w(f"[OK] {name} done.")

    w("\n" + "=" * 60)
    w("[PIPELINE COMPLETE]")
    w("=" * 60)
