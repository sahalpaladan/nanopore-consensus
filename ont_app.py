# app.py
import streamlit as st
import subprocess
import zipfile
import os
from pathlib import Path

st.set_page_config(page_title="Nanopore Consensus Pipeline", layout="wide")

st.title("🧬 Nanopore Consensus Pipeline")

# Upload files
reference = st.file_uploader("Upload Reference FASTA", type=["fa", "fasta"])
reads = st.file_uploader("Upload Nanopore FASTQ", type=["fastq", "fq"])
bed = st.file_uploader("Upload Primer BED", type=["bed"])

threads = st.number_input("Threads", min_value=1, max_value=64, value=8)

run_btn = st.button("Run Pipeline")


def save_uploaded_file(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())


if run_btn:
    if reference and reads and bed:
        workdir = Path("run_output")
        workdir.mkdir(exist_ok=True)

        ref_path = workdir / reference.name
        reads_path = workdir / reads.name
        bed_path = workdir / bed.name

        save_uploaded_file(reference, ref_path)
        save_uploaded_file(reads, reads_path)
        save_uploaded_file(bed, bed_path)

        st.info("Files uploaded successfully.")

        commands = [
            f"NanoPlot --fastq {reads_path} --threads {threads} -o {workdir}/nanoplot_out",

            f"samtools faidx {ref_path}",

            f"minimap2 -ax map-ont -t {threads} {ref_path} {reads_path} | "
            f"samtools sort -@ {threads} -o {workdir}/sorted.bam",

            f"samtools index {workdir}/sorted.bam",

            f"ivar trim -i {workdir}/sorted.bam -b {bed_path} -p {workdir}/trimmed",

            f"samtools sort -o {workdir}/trimmed.sorted.bam {workdir}/trimmed.bam",

            f"samtools index {workdir}/trimmed.sorted.bam",

            f"bcftools mpileup -Ou -f {ref_path} {workdir}/trimmed.sorted.bam | "
            f"bcftools call -mv -Oz -o {workdir}/variants.vcf.gz",

            f"bcftools index {workdir}/variants.vcf.gz",

            f"bcftools consensus -f {ref_path} {workdir}/variants.vcf.gz > "
            f"{workdir}/consensus.fasta"
        ]

        log_box = st.empty()

        for cmd in commands:
            st.write(f"Running: `{cmd}`")
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            log_box.text(process.stdout + "\n" + process.stderr)

            if process.returncode != 0:
                st.error(f"Error running command:\n{cmd}")
                st.stop()

        st.success("Pipeline completed successfully!")

        # Download consensus only
        consensus_file = workdir / "consensus.fasta"
        if consensus_file.exists():
            with open(consensus_file, "rb") as f:
                st.download_button(
                    label="Download Consensus FASTA",
                    data=f,
                    file_name="consensus.fasta",
                    mime="text/plain"
                )

        # Create ZIP of all outputs
        zip_path = workdir / "pipeline_results.zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(workdir):
                for file in files:
                    file_path = Path(root) / file
                    if file != "pipeline_results.zip":
                        zipf.write(file_path, arcname=file_path.relative_to(workdir))

        # Download all results
        with open(zip_path, "rb") as f:
            st.download_button(
                label="⬇ Download All Results",
                data=f,
                file_name="pipeline_results.zip",
                mime="application/zip"
            )

    else:
        st.warning("Please upload all required files.")