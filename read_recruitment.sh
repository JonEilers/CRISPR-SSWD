#!/bin/sh
#
#----------------------------------
#SCRIPT FOR RECRUITING AND ASSEMBLING READS FROM SAMPLE METAGENOME TO REFERENCE SEQUENCES
#----------------------------------
#
# STEPS
# 1: remove unneccesary or bad characters from sample fasta using sed or mogrify?
# 2: create blast database using makeblastdb, be sure to index
# 3: use tblastn, pVOG.aln, and the blast database to find reads in sample
# 4: make new fasta with the recruited reads only 
