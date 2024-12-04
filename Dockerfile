FROM clinicalgenomics/python3.11-miniconda

LABEL base_image="clinicalgenomics/python3.11-miniconda"
LABEL about.home="https://github.com/Clinical-Genomics/chanjo"
LABEL about.documentation="https://clinical-genomics.github.io/chanjo/"
LABEL about.tags="chanjo,bam,NGS,MPS,WES,WGS,coverage,sambamba,alpine,python"
LABEL about.license="MIT License (MIT)"

# Install Sambamba using conda
RUN conda install -c bioconda sambamba

WORKDIR /home/worker/app
COPY . /home/worker/app

# Install Chanjo requirements
RUN pip install -r requirements.txt

# Install the app
RUN pip install -e .

# Run commands as non-root user
RUN adduser --disabled-login worker
RUN chown worker:worker -R /home/worker
USER worker
