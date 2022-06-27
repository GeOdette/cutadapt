
import os
import subprocess
from pathlib import Path
from latch import small_task, workflow
from latch.types import LatchFile, LatchDir
from typing import Optional
import shutil
from typing import Tuple

# PE


@small_task
def PE_task(input_file1: Optional[LatchFile],
            input_file2: Optional[LatchFile],
            forwad_adapt: str,
            rev_adapter: str,

            ) -> Tuple[LatchFile, LatchFile, LatchFile, LatchFile]:

    # Degining outputs

    local_file1 = Path("cutadapt_PE_1.fasta")

    local_file2 = Path("cutadapt_PE_2.fasta")
    info_file = Path("info_file_latch.fasta")
    cutadapt_report = Path("report_report_latch.json")
    untrimmed_file = Path("untrimmed_output.fasta")

    _cutadapt_PE = [
        "cutadapt",
        "--report=full",
        "--json",
        str(cutadapt_report),
        "-a",
        str(forwad_adapt),
        "-A",
        str(rev_adapter),
        "--output",
        str(local_file1),
        "-p",
        str(local_file2),
        "--fasta",
        "--info-file",
        str(info_file),
        "--untrimmed-output",
        str(untrimmed_file),
        input_file1.local_path,
        input_file2.local_path,


    ]
