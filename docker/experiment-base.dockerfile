FROM faasm/cpp-sysroot:0.0.15

RUN apt-get update
RUN apt-get install -y \
    python3-dev \
    python3-pip \
    python3-venv

# Python set-up
WORKDIR /experiments
RUN git clone https://github.com/faasm/experiments experiment-base
WORKDIR /experiments/experiment-base
RUN pip3 install -r requirements.txt
