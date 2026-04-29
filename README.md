# 🧬 Nanopore Consensus Pipeline

A web-based and command-line pipeline for generating consensus genome sequences from Oxford Nanopore sequencing reads using mapping-based assembly.

This application is deployed using Streamlit and allows users to upload sequencing files, run the pipeline, and download results.

## Features

- Upload **Reference FASTA**
- Upload **Nanopore FASTQ**
- Upload **Primer BED**
- Adjustable thread selection
- Quality control using NanoPlot
- Read mapping using Minimap2
- Primer trimming using iVar
- Variant calling using BCFtools
- Consensus sequence generation
- Download **Consensus FASTA**
- Download **All Results** as ZIP

---

## Pipeline Workflow

1. **Quality Control**
   - NanoPlot generates read quality reports.

2. **Reference Indexing**
   - samtools faidx indexes the reference genome.

3. **Read Mapping**
   - minimap2 aligns Nanopore reads to the reference.

4. **Sorting & Indexing**
   - samtools sorts and indexes BAM files.

5. **Primer Trimming**
   - iVar trims primer regions using BED file.

6. **Variant Calling**
   - bcftools mpileup + call identifies variants.

7. **Consensus Generation**
   - bcftools consensus creates final FASTA.

---

## Tools Used

- Streamlit
- NanoPlot
- Minimap2
- Samtools
- iVar
- BCFtools

---

## Installation

Clone repository:

```bash
git clone https://github.com/sahalpaladan/nanopore-consensus.git
cd nanopore-consensus
