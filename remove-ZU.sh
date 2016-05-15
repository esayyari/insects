#!/bin/bash

#ZFRE and UXCS
mv genes genes-with-ZU
mkdir genes
for x in `ls genes-with-ZU`; do mkdir genes/$x; done
for x in `ls genes-with-ZU`; do remove_taxon_from_fasta.sh "ZFRE|UXCS" genes-with-ZU/$x/$x.input.FAA > genes/$x/$x.input.FAA; done
for x in `ls genes-with-ZU`; do remove_taxon_from_fasta.sh "ZFRE|UXCS" genes-with-ZU/$x/$x.input.FNA > genes/$x/$x.input.FNA; done
