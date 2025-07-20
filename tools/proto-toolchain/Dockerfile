FROM ubuntu:22.04

# Install protoc from the distro package for reliability
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
      python3 python3-pip protobuf-compiler curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Install the Python plugin for codegen
RUN pip3 install --no-cache-dir protobuf

ENV PATH="/usr/local/bin:${PATH}"
WORKDIR /workspace

ENTRYPOINT ["/bin/bash"]