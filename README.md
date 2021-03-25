# General Notes for Running DREEM
## Credentials for sequencer:
basespace.illumina
uname: yesselmanlab@gmail.com
pword: Yeslab123!
Want it to be in FastQ

## Required Installs

+ [NovocraftAlign](http://www.novocraft.com/support/download/)

+ [bowtie2](https://anaconda.org/bioconda/bowtie2)

+ [fastqc](https://anaconda.org/bioconda/fastqc)

+ [cutadapt](https://github.com/marcelm/cutadapt)
        + must **do version 1.18**, then run `python setup.py install` 

## Workflow

First Step is de-multiplexing
+ data will always be in pairs, with R1 and R2 in opposite directions
+ therefore, R2 is our read 1
+ there will be another file with extension .fa... it is tab delimited 
+ make a folder for the analysis and make a special sub-folder called input
	+ within input, move R2 to test_mate1.fastq and R1 to test_mate2.fastq
+ there must be a fasta file with reference sequences (aka the original sequences minus the t7 promoter but also in DNA format)


`Run_DREEM.py input output test test.fasta mttr-6-alt-h1 1 134 --fastq`


Steps
1. download data into appropriate folder and run command `gunzip *` to unzip it all
	+ if using Linux:
		https://developer.basespace.illumina.com/docs/content/documentation/cli/cli-overview
		i. `bs auth` -- sets up the authorization... I think for this one you only have to do it once?
		ii. `bs list projects` -- shows the projects available... check which one you actually want
		iii. `bs download project -i <ProjectID> -o <output> --extension=fasta.gz` this is the final download that will actually get the files
2. make RTBfile.fa... => includes all barcodes for the run. Format is below. MUST BE TAB DELIMITED, NO EXTRA LINE AT END
```
Distance	4
Format	5
RTB004	TGCGCCATTGCT
RTB005	ACAAAATGGTGG
RTB006	CTGCGTGCAAAC
RTB007	GATTTGCACCTA
RTB013	TGGCGAACATGG
RTB012	GCAAATGTGCTA
```
3. Run `../installs/novocraft/novobarcode -b RTBbarcodes.fa -f input/*` to get the files split up into barcodes. Note that this has to be done once for sure,
 but will often have to be done twice so that the individual designs in a pool can be separated out.

