"""
Find and remove adapter sequences, primers, poly-A tails
"""

import os
import subprocess
from pathlib import Path
from latch import small_task, workflow
from latch.types import LatchFile, LatchDir
from typing import Optional
from typing import Tuple


@small_task
def cutadapt_task(adapter_sequence: Optional[str],
                  input_file: Optional[LatchFile],
                  input_file1: Optional[LatchFile],
                  input_file2: Optional[LatchFile],
                  out_dir: LatchDir,
                  forwad_adapt: Optional[str],
                  rev_adapter: Optional[str],
                  adapt3: bool = False,
                  adapt5: bool = False,
                  ADAPTERX: bool = False,
                  XADAPTER: bool = False,
                  ADAPTERp: bool = False,
                  AADAPTER: bool = False,
                  ADAPTERb: bool = False,
                  SE: bool = False,
                  PE: bool = False) -> Tuple[LatchFile, LatchFile, LatchFile, LatchFile, LatchFile]:

    # Degining outputs

    local_file = Path("cutadapt_latch.fasta")
    info_file = Path("info_file_latch.fasta")
    local_file1 = Path("cutadapt_PE_1.fasta")
    local_file2 = Path("cutadapt_PE_2.fasta")
    cutadapt_report = Path("report_report_latch.json")
    untrimmed_file = Path("untrimmed_output.fasta")
    untrimmed_paired_file = Path("untrimmed_paired_output.fasta")
    stderror = Path("standard erro")

    # local_prefix = os.path.join(local_dir, "latch")

    # removing 3' adapter
    if adapt3 or ADAPTERX or ADAPTERp == True:

        _cutadapt_cmd = [
            "cutadapt",
            "--report=full",
            "--json",
            str(cutadapt_report),
            "-a",
            str(adapter_sequence),
            "--output",
            str(local_file),
            "--fasta",
            "--info-file",
            str(info_file),
            "--untrimmed-output",
            str(untrimmed_file),
            input_file.local_path,


        ]
    # removing 5' adapter
    elif adapt5 or XADAPTER or AADAPTER == True:
        _cutadapt_cmd = [
            "cutadapt",
            "--report=full",
            "--json",
            str(cutadapt_report),
            "-g",
            str(adapter_sequence),
            "--output",
            str(local_file),
            "--fasta",
            "--info-file",
            str(info_file),
            "--untrimmed-output",
            str(untrimmed_file),
            input_file.local_path,


        ]

    elif ADAPTERb == True:
        _cutadapt_cmd = [
            "cutadapt",
            "--report=full",
            "--json",
            str(cutadapt_report),
            "-b",
            str(adapter_sequence),
            "--output",
            str(local_file),
            "--fasta",
            "--info-file",
            str(info_file),
            "--untrimmed-output",
            str(untrimmed_file),
            input_file.local_path,


        ]

    _cutadapt_PE = [
        "cutadapt",
        "--report=full",
        "--json",
        str(cutadapt_report),
        "-a",
        str(forwad_adapt),
        "-A",
        str(rev_adapter),
        "-o",
        str(local_file1),
        "-p",
        str(local_file2),
        "--fasta",
        "--info-file",
        str(info_file),
        "--untrimmed-output",
        str(untrimmed_file),
        "--untrimmed-paired-output",
        str(untrimmed_paired_file),
        input_file1.local_path,
        input_file2.local_path,


    ]

    # Run SE
    if SE == True:
        subprocess.run(_cutadapt_cmd, check=True, stderr=stderror)
    elif PE == True:
        subprocess.run(_cutadapt_PE, check=True)
    # shutil.move("/root/out_file", "/root/cutadapt/out_file")

    if SE == True:
        return (LatchFile(str(local_file), f"{out_dir.remote_path}/SE_Trim.fasta"),
                LatchFile(str(info_file),
                          f"{out_dir.remote_path}/cutadapt_info_file.fasta"),
                LatchFile(str(cutadapt_report),
                          f"{out_dir.remote_path}/cutadapt_report.json"),
                LatchFile(str(untrimmed_file),
                          f"{out_dir.remote_path}/untrimmed_file.fasta"),
                LatchFile(str(stderror), f"{out_dir.remote_path}/process_error.fasta"))
    elif PE == True:
        return (LatchFile(str(local_file1), f"{out_dir.remote_path}/PE_trim_1.fasta"),
                LatchFile(str(local_file2),
                          f"{out_dir.remote_path}/PE_trim_2.fasta"),
                LatchFile(str(cutadapt_report),
                          f"{out_dir.remote_path}/cutadapt_report.json"),
                LatchFile(str(untrimmed_file),
                          f"{out_dir.remote_path}/untrimmed_file.fasta"),
                LatchFile(str(untrimmed_paired_file), f"{out_dir.remote_path}/untrimmed__paired_file.fasta"))


@workflow
def cutadapt(adapter_sequence: Optional[str],
             input_file: Optional[LatchFile],
             input_file1: Optional[LatchFile],
             input_file2: Optional[LatchFile],
             out_dir: LatchDir,
             forwad_adapt: Optional[str],
             rev_adapter: Optional[str],
             adapt3: bool = False,
             adapt5: bool = False,
             ADAPTERX: bool = False,
             XADAPTER: bool = False,
             ADAPTERp: bool = False,
             AADAPTER: bool = False,
             ADAPTERb: bool = False,
             SE: bool = False,
             PE: bool = False) -> Tuple[LatchFile, LatchFile, LatchFile, LatchFile, LatchFile]:
    """

     __cutadapt__

    Find and remove adapter sequences, primers, poly-A tails

    ----

    # Case use

    Analyzing next generation sequencing data requires the removal of unwanted adapters 

    from the raw reads. These include:<br>

    > 3’ sequencing adapter from small-RNA sequencing<br>

    > Primer sequence in amplicon reads<br> 

    > Poly-A tails use in pulling out RNA from your sample<br>

    **Cutadapt workflow uses the cutadapt program to remove adapter or primer sequences in an error-tolerant way**<br>

    # Basic usage:

    To use cutadapt, you will need to supply vital specifications: 

    ## Trimming regular adapters<br>

    > Supply the relevant adapter i.e 3’ or 5’ adapter e.g AACCGGTT and checkout the related trimming adapter function<br>

    Additionally, you will need to input the FASTA or FASTQ file and select an output directory<br>
    for your files, then let the console do the rest<br>

    The workflow has been configured to generate: 

    > cutadapt_info_file.fasta: This files contains detailed information about where adapters were found in the read<br>

    > cutadapt_report.json: This contains the full report after it has finished processing the reads.<br>

    > SE_Trim.fasta: This file contains the results of trimming the single end read<br>

    > untrimmed_file.fasta: File contains results of the  first read when the processed pair was not trimmed<br>

    ## Other adapters

    You can also trim other adapters by checking relevant boxes

    > Non-internal 3’ adapter

    > Non-internal 5’ adapter 

    > Anchored 3’ adapter 

    > Anchored 5’ adapter

    ## Paired end reads

    Cutadapt workflow can also process paired end reads.  This will require that you supply read 1 and read 2 as input files<br>

    In paired-end mode, Cutadapt checks whether the input files are properly paired.<br>

    An error is raised if one of the files contains more reads than the other or<br>

    if the read names in the two files do not match. 

    > IMPORTANT NOTE: The info file will only contain information only from the first read.<br>

    In Paired end mode, you will access the following files:<br>

    > cutadapt_report.json: This contains the full report after it has finished processing the reads.<br>

    > PE_trim_1.fasta: This file contains the results of trimming read 1<br>

    > PE_trim_2.fasta: This file contains the results of trimming read 2<br>

    > untrimmed_file.fasta: File contains results of the  first read in a pair when the processed pair was not trimmed<br>

    > untrimmed__paired_file.fasta: File contains results of the  first read in a pair when the processed pair was not trimmed<br>



    __metadata__:

        display_name: Find and remove adapter sequences, primers, poly-A tails and other types of unwanted sequence 

        author:

            name: GeOdette

            email: steveodettegeorge@gmail.com

            github:
        repository: https://github.com/GeOdette/cutadapt.git

        license:
            id: MIT

    Args:
        SE:
          Check this option to trims single end reads

          __metadata__:
            display_name: Trim single end reads

        adapter_sequence:
          Enter the the correct adapter sequence to trim adapter,

          __metadata__:
            display_name: Adapter sequence for single end read

        input_file:
          File containign sequences to be trimmed

          __metadata__:
            display_name: FASTA/FASTQ file

        adapt3:
          Remove Regular 3’ adapter

          __metadata__:
            display_name: Remove regular 3’ adapter

        adapt5:
          Remove Regular 5’ adapter

          __metadata__:
            display_name: Remove regular 5’ adapter

        ADAPTERX:
          Remove Non-internal 3’ adapter

          __metadata__:
            display_name: Remove Non-internal 3’ adapter

        XADAPTER:
          Remove Non-internal 5’ adapter

          __metadata__:
            display_name: Remove Non-internal 5’ adapter

        ADAPTERp:
          Remove Anchored 3’ adapter

          __metadata__:
            display_name: Remove Anchored 3’ adapter

        AADAPTER:
          Remove Anchored 5’ adapter

          __metadata__:
            display_name: Remove Anchored 5’ adapter

        ADAPTERb:
          Remove Remove both 5’ and 3' adapters

          __metadata__:
            display_name: Remove both 5’ and 3' adapters

        PE:
          Check this option to trims paired end reads

          __metadata__:
            display_name: Trim paired end reads

        input_file1:
          File 1 containign paired end reads for paired end trimming

          __metadata__:
            display_name: Read 1

        input_file2:
          File 2 containign paired end reads for paired end trimming

          __metadata__:
            display_name: Read 2

        forwad_adapt:
          Adapter for the forward read

          __metadata__:
            display_name: Read 1 adapter

        rev_adapter::
          Adapter for the second read

          __metadata__:
            display_name: Read 2 adapter

        out_dir:
          Your prefferred output directory. Tip* Create a directory at the latch console

          __metadata__:
            display_name: Output Directory
    """
    return cutadapt_task(adapter_sequence=adapter_sequence,
                         input_file=input_file,
                         input_file1=input_file1,
                         input_file2=input_file2,
                         forwad_adapt=forwad_adapt,
                         rev_adapter=rev_adapter,
                         out_dir=out_dir,
                         adapt3=adapt3,
                         adapt5=adapt5,
                         ADAPTERX=ADAPTERX,
                         XADAPTER=XADAPTER,
                         ADAPTERp=ADAPTERp,
                         AADAPTER=AADAPTER,
                         ADAPTERb=ADAPTERb,
                         SE=SE,
                         PE=PE)
