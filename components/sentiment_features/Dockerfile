FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest

COPY conda.yml /tmp/conda.yml
RUN conda env create -f /tmp/conda.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "sentiment_env", "/bin/bash", "-c"]

# Download NLTK data during build
RUN python -c "import nltk; nltk.download('vader_lexicon')"

# Set environment variable for NLTK data path
ENV NLTK_DATA=/opt/conda/envs/sentiment_env/nltk_data

# Set the PATH to use the conda environment
ENV PATH=/opt/conda/envs/sentiment_env/bin:$PATH
