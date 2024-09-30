# syntax=docker/dockerfile:1

FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ENV APP_PATH /app/travel_booking_agencies/be
ENV VNCORENLP_DIR /vncorenlp

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        python3 \
        python3-pip \
        && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for GPU runtime
ENV NVIDIA_VISIBLE_DEVICES=all

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR ${APP_PATH}

RUN mkdir ${VNCORENLP_DIR}

# Install openjdk for py_vncorenlp requirements
RUN apt-get update && apt-get install -y default-jdk && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python3 -m pip install -r requirements.txt

# Install py_vncorenlp
RUN mkdir ${VNCORENLP_DIR}/models
RUN mkdir ${VNCORENLP_DIR}/models/dep
RUN mkdir ${VNCORENLP_DIR}/models/ner
RUN mkdir ${VNCORENLP_DIR}/models/postagger
RUN mkdir ${VNCORENLP_DIR}/models/wordsegmenter

RUN wget -O ${VNCORENLP_DIR}/VnCoreNLP-1.2.jar https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/VnCoreNLP-1.2.jar
RUN wget -O ${VNCORENLP_DIR}/models/wordsegmenter/vi-vocab https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/vi-vocab
RUN wget -O ${VNCORENLP_DIR}/models/wordsegmenter/wordsegmenter.rdr https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/wordsegmenter.rdr
RUN wget -O ${VNCORENLP_DIR}/models/postagger/vi-tagger https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/postagger/vi-tagger
RUN wget -O ${VNCORENLP_DIR}/models/ner/vi-500brownclusters.xz https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/ner/vi-500brownclusters.xz
RUN wget -O ${VNCORENLP_DIR}/models/ner/vi-ner.xz https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/ner/vi-ner.xz
RUN wget -O ${VNCORENLP_DIR}/models/ner/vi-pretrainedembeddings.xz https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/ner/vi-pretrainedembeddings.xz
RUN wget -O ${VNCORENLP_DIR}/models/dep/vi-dep.xz https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/dep/vi-dep.xz


# Copy the source code into the container.
COPY . ${APP_PATH}

# Set environment variables for CUDA
ENV CUDA_HOME /usr/local/cuda
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/local/cuda/lib64

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD uvicorn app.main:app --reload --host=0.0.0.0 --port=8000
