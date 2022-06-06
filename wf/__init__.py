"""
Find and remove adapter sequences, primers, poly-A tails
"""

import os
import subprocess
from pathlib import Path
from latch import small_task, workflow
from latch.types import LatchFile, LatchDir
from typing import Optional
import shutil


@small_task
def cutadapt_task(adapter_sequence: str, input_file: LatchFile, out_dir: LatchDir) -> LatchDir:

    # A reference to our output.
    os.mkdir("/root/cutadapt")

    out_file = Path("out.fasta").resolve()

    _cutadapt_cmd = [
        "cutadapt",
        "-a",
        str(adapter_sequence),
        "-o",
        str(out_file),
        input_file.local_path,
    ]
    with open("out_file", "w") as f:
        subprocess.run(_cutadapt_cmd, stdout=f)
    shutil.move("/root/out_file", "/root/cutadapt/out_file")

    return LatchDir(str("cutadapt"), out_dir.remote_path)


@workflow
def cutadapt(adapter_sequence: str, input_file: LatchFile, out_dir: LatchDir) -> LatchDir:
    """

    # cutadapt

    Find and remove adapter sequences, primers, poly-A tails

    ----

    __metadata__:

        display_name: Find and remove adapter sequences, primers, poly-A tails

        author:

            name:

            email:

            github:
        repository:

        license:
            id: MIT

    Args:

        adapter_sequence:
          Enter the the correct adapter sequence to trim a 3’ adapter,

          __metadata__:
            display_name: 3' adapter sequence

        input_file:
          File containign sequences to be trimmed

          __metadata__:
            display_name: FASTA/FASTQ file

        out_dir:
          Your prefferred output directory. Tip* Create a directory at the latch console

          __metadata__:
            display_name: Output Directory
    """
    return cutadapt_task(adapter_sequence=adapter_sequence, input_file=input_file, out_dir=out_dir)
