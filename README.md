![image](https://user-images.githubusercontent.com/96872843/176043639-359d461a-2185-4f68-ae09-be005285ce16.png)

<p align="center">
[Launch the workflow at the Latch console](https://console.latch.bio/explore/62939/info)
</p>

# Remove adapter sequences, primers, poly-A tails and other types of unwanted sequence using cutadapt | [Pertinent information obtained from cutadapt original documentation](https://cutadapt.readthedocs.io/en/stable/)


## About

Cutadapt helps with these trimming tasks by finding the adapter or primer sequences in an error-tolerant way. It can also modify and filter single-end and paired-end reads in various ways. Adapter sequences can contain IUPAC wildcard characters. Cutadapt can also demultiplex your reads.<br>


### Case use

Analyzing next generation sequencing data requires the removal of unwanted adapters from the raw reads. These include:<br>

> 3’ sequencing adapter from small-RNA sequencing<br>

> Primer sequence in amplicon reads<br> 

>   Poly-A tails use in pulling out RNA from your sample<br>

**Cutadapt workflow uses the cutadapt program to remove adapter or primer sequences in an error-tolerant way**<br>

### Basic usage:

You can use cutadapt on the single end read mode:

To use cutadapt, you will need to supply: 

#### Trimming regular adapters<br>

> Supply the relevant adapter i.e 3’ or 5’ adapter e.g AACCGGTT and checkout the related trimming adapter function<br>

#### Other adapters

You can also trim other adapters by checking relevant boxes

* Non-internal 3’ adapter

* Non-internal 5’ adapter 

* Anchored 3’ adapter 

* Anchored 5’ adapter

Additionally, you will need to input the FASTA or FASTQ file and select an output directory for your files, then let the console do the rest<br>

**The workflow has been configured to generate:** 

* cutadapt_info_file.fasta: This files contains detailed information about where adapters were found in the read<br>

* cutadapt_report.json: This contains the full report after it has finished processing the reads.<br>

* SE_Trim.fasta: This file contains the results of trimming the single end read<br>

* untrimmed_file.fasta: File contains results of the  first read when the processed pair was not trimmed<br>

## Paired end reads

Cutadapt workflow can also process paired end reads.  This will require that you supply read 1 and read 2 as input files<br>

In paired-end mode, Cutadapt checks whether the input files are properly paired.<br>

An error is raised if one of the files contains more reads than the other or if the read names in the two files do not match. 

    > IMPORTANT NOTE: The info file will only contain information only from the first read.<br>

**In Paired end mode, you will access the following files:**<br>

* cutadapt_report.json: This contains the full report after it has finished processing the reads.<br>

* PE_trim_1.fasta: This file contains the results of trimming read 1<br>

* PE_trim_2.fasta: This file contains the results of trimming read 2<br>

* untrimmed_file.fasta: File contains results of the  first read in a pair when the processed pair was not trimmed<br>

* untrimmed__paired_file.fasta: File contains results of the  first read in a pair when the processed pair was not trimmed<br>
