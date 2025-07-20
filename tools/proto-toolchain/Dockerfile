FROM ubuntu:22.04

# Install Python 3, pip, curl, unzip (for protoc install)
RUN apt-get update && apt-get install -y python3 python3-pip curl unzip

# Install protoc (official release, x86_64)
RUN curl -L -o protoc.zip https://github.com/protocolbuffers/protobuf/releases/download/v24.4/protoc-24.4-linux-x86_64.zip \
  && unzip protoc.zip -d /usr/local \
  && rm protoc.zip \
  && chmod +x /usr/local/bin/protoc

# Install the Python plugin for protoc
RUN pip3 install --no-cache-dir protobuf==4.25.3

ENV PATH="/usr/local/bin:${PATH}"
WORKDIR /workspace

# Default entrypoint to bash for easy debugging/experimentation
ENTRYPOINT ["/bin/bash"]