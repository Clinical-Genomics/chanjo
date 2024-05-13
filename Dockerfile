FROM frolvlad/alpine-miniconda3

LABEL base_image="frolvlad/alpine-miniconda3"
LABEL about.home="https://github.com/Clinical-Genomics/chanjo"
LABEL about.documentation="https://clinical-genomics.github.io/chanjo/"
LABEL about.tags="chanjo,bam,NGS,coverage,sambamba,alpine,python,python3.7"
LABEL about.license="MIT License (MIT)"

# Install Sambamba using conda
RUN conda update -n base -c defaults conda && conda install -c bioconda sambamba

RUN conda install -c conda-forge ruamel.yaml

# Install required libs
RUN apk update \
	&& apk --no-cache add bash python3

WORKDIR /home/worker/app
COPY . /home/worker/app

# Install Chanjo requirements
RUN pip install -r requirements.txt

# Install the app
RUN pip install -e .

# Run commands as non-root user
RUN adduser -D worker
RUN chown worker:worker -R /home/worker
USER worker
