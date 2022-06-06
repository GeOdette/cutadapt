FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

#Install conda and build working env for cutadapt/Install cutadapt
# RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
# ENV CONDA_DIR /opt/conda
# RUN bash miniconda.sh -b -p /opt/conda
# ENV PATH=$CONDA_DIR/bin:$PATH
# RUN conda create -n cutadaptenv cutadapt &&\
# conda activate cutadaptenv

# install cutadapt
RUN apt-get install sudo
RUN sudo python3 -m pip install cutadapt

# Stop here
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
