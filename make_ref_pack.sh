#!/bin/sh
#
#------------------------------------------
# Reference Package Making Script
#------------------------------------------
#
# FastTree -log pVOG.ref.stat pVOG.aln > pVOG.tre
# hmmalign -o pVOG.sswd.sto --mapali pVOG.hmm sswd.metagenome.fasta
# taxit create -P /path/to/files -l 'gene name' -a 'author' -d 'description of package' --aln-fasta reference/alignment/fasta --seq-info csv/   file/aligned/reference/sequence/info --profile /alignment/profile --readme /readme/file --tree-stats tree/stat/file --aln-sto hmm/align/sto -- tree-file phylogenetic/reference/tree --taxonomy csv/defining/taxonomy
# pplacer -c /path/to/referencepackage sswd.metagenome.fasta


cd ~/test_reference_package/test1

# Remove any undesirable characters from the pVOG alignment file
sed '
s/\[//g
s/\]//g' test.aln > test1.aln

# Build reference tree using the pVOG alignment and output tree statistics log file
FastTree -log test.ref.stat test1.aln >test.tre

# Align pVOG alignment to pVOG hmm
hmmalign -o test.sto --mapali test1.aln test.hmm test.fasta

# Build a reference package using the pVOG alignment, the phylogenetic tree, and tree statistics
taxit create -P 'test.reference.package' -l 'VOG0001' -a 'jon' -d 'a test reference package using pVOGs' --aln-fasta test1.aln --tree-file test.tre --tree-stats test.ref.stat --profile test.ref.sto

# Align reads from sswd metagenome to reference tree
pplacer -c test.reference.package test.sto

# Create an xml file to visualize using archeoptryx
guppy fat test.sto
