FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest
COPY conda.yml /tmp/conda.yml
RUN conda env create -f /tmp/conda.yml
ENV PATH=/opt/conda/envs/sentiment_env/bin:$PATH
