# SOLIDA-CORE [TOOLKIT]()

Collection of [solida-core]() useful scripts for accessory and supplementary files management.

## Included Scripts:
* **[reference_organizer](#reference_organizerpy)**: this script performs the organization of reference files in [solida-core]() required directory-tree













### reference_organizer.py
This script performs the organization of reference files in [solida-core]() required directory-tree structure.
The user is required to entry the desired reference folder path and to choose between hg19 and hg38 human genome versions.

The scripts attempt to connect and download files from the FTP server of **[GATK resource bundle](https://software.broadinstitute.org/gatk/download/bundle)**.
Files are then extracted and placed in the [solida-core]() expected directory structure.

Given the limit of 25 users of FTP server, the script performs multiple connection attempts [default=5]. This value can be set with the `--reconnection_attempts` parameter.

To get script usage, type:
```bash
python reference_organizer.py -h
```

```bash
usage: reference_organizer.py [-h] --reference_dir PATH --release hg19/hg38
                              [--reconnection_attempts int] [--force]

Prepare reference files for solida-core pipelines

optional arguments:
  -h, --help            show this help message and exit
  --reference_dir PATH, -w PATH
                        Destination folder for reference files
  --release hg19/hg38, -r hg19/hg38
                        UCSC Genome Release to download: [hg19,hg38]
  --reconnection_attempts int, -a int
                        Number of connection attempts to perform in case of
                        busy FTP server [default: 5]
  --force               Download files in the directory even if they exists
                        (Default: FALSE)
```