#!/usr/bin/env Rscript

## Author Matteo Massidda
## Date 2022/10/21
## An R Script to rename fastq files in a directory to be compliant with BaseSpace filename requirements
#SampleName_SampleNumber_Lane_Read_FlowCellIndex.fastq.gz
#Nomecampione_S01_L008_R1_001.fastq.gz

library(stringr)
args = commandArgs(trailingOnly=TRUE)

fastq_dir=args[1]
setwd(fastq_dir)
files=dir(pattern = ".fq.gz")

## Get sample names ad create a list of unique names, to generate and correctly assign the SampleNumber
sample_list=NULL
for (filename in files) {
  print(filename)
  SampleName=substr(str_split_fixed(filename,pattern = "\\.", 3)[3], start = 1, stop = 16)
  sample_list=append(sample_list,values = SampleName)
}

my_df=data.frame(samples = unique(sample_list))
my_df["SampleNumber"]=NA
counter=1
for (fileline in 1:nrow(my_df)) {
  if (counter<10) {
    my_df[fileline,"SampleNumber"]=paste("S0",counter,sep = "")
  }
  else {my_df[fileline,"SampleNumber"]=paste("S",counter,sep = "")}
  counter=counter+1
}

## Extract information from each filename and rename it if exists
final_names=NULL
for (filefastq in files) {
  SampleName=substr(str_split_fixed(filefastq,pattern = "\\.", 3)[3], start = 1, stop = 16)
  SampleNumber=my_df[my_df$samples==SampleName,"SampleNumber"]
  Lane=str_split_fixed(filefastq,pattern = "\\.", 3)[2]
  Read=substr(str_split_fixed(filefastq,pattern = "\\.", 3)[3], start = 18, stop = 19)
  FlowCellIndex="001"
  
  merged_name=paste(SampleName,SampleNumber,Lane,Read,FlowCellIndex, sep = "_")
  extension="fastq.gz"
  final_name=paste(merged_name,extension,sep = ".")
  final_names=append(final_names, final_name)
  if(file.exists(filefastq)){
    # Rename file name
    file.rename(from = filefastq,to = final_name)
  }else{
    print('File Not found :')
  }
}

message("Rename completed!")