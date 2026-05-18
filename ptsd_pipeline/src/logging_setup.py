"""
logging_setup.py
================
Single call to configure_logging() wires up the root logger with:
  - Console handler  (stdout, INFO+, UTF-8 safe for Hebrew)
  - RotatingFileHandler (pipeline_run.log, DEBUG+, 10 MB / 3 backups)

Call once from run_pipeline.py before any stage import.

All comments and docstrings are in English.
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(log_path: Path, level: int = logging.DEBUG) -> None:
    """
    Configure the root logger if it has no handlers yet.

    Parameters
    ----------
    log_path : Path
        Destination for the rotating log file.
    level : int
        Root logger level (default DEBUG so file captures everything).
    """
    root = logging.getLogger()
    if root.handlers:
        return  # idempotent — safe to call multiple times

    root.setLevel(level)

    _FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    _DATE = "%H:%M:%S"

    # Console handler — INFO and above, UTF-8 to avoid Hebrew mojibake
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(_FMT, datefmt=_DATE))
    if hasattr(ch.stream, "reconfigure"):
        ch.stream.reconfigure(encoding="utf-8")
    root.addHandler(ch)

    # Rotating file handler — DEBUG and above
    log_path.parent.mkdir(parents=True, exist_ok=True)
    fh = RotatingFileHandler(
        log_path,
        maxBytes=10 * 1024 * 1024,   # 10 MB
        backupCount=3,
        encoding="utf-8",
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(_FMT, datefmt=_DATE))
    root.addHandler(fh)
