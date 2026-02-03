FROM cld1994/cuda:10.1-cudnn7-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates git \
    python3.8 python3.8-dev python3.8-venv python3-distutils \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Convenience: make `python` / `pip` available.
RUN ln -sf /usr/bin/python3.8 /usr/local/bin/python \
    && ln -sf /usr/bin/pip3 /usr/local/bin/pip

# Optional sanity check (kept lightweight)
RUN python --version && pip --version

# Copy the repo into the image so /workspace is not empty.
COPY . /workspace

# Install SynthSeg and its Python dependencies as specified by setup.py
# (setup.py reads requirements_python3.8.txt based on the installed Python version)
RUN python -m pip install --no-cache-dir setuptools wheel \
    && python setup.py install

CMD ["bash"]
