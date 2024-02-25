FROM ubuntu:22.04

LABEL maintainer="Vibhash Singh <singh13@ads.uni-passau.de>"
LABEL description="Docker image for runnng JSONSchemaDiscovery tool"

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8"
ENV NODE_MAJOR=16

RUN apt-get update --fix-missing
RUN apt-get clean
RUN apt-get install -y \
    curl \
    git \
    g++ \
    make \
    python3 \
    python3-pip \
    texlive-latex-base \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    vim

RUN pip install requests pymongo

# Install Node16.x
RUN apt-get install -y ca-certificates gnupg
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" |  tee /etc/apt/sources.list.d/nodesource.list
RUN apt-get update
RUN apt-get install nodejs -y

# Download Dataset
RUN git clone https://github.com/feekosta/datasets.git /dataset

# Clone JSONSchemaDiscovery repository
RUN git clone https://github.com/feekosta/JSONSchemaDiscovery.git
WORKDIR /JSONSchemaDiscovery
RUN git checkout tags/1.1.0

RUN npm install -g @angular/cli
RUN npm install -g typescript
RUN npm install

# Apply patch
COPY npm-dev.patch /JSONSchemaDiscovery
RUN git apply npm-dev.patch

# smoke.sh
COPY doAll.sh /
RUN chmod +x /doAll.sh

# Copy ground truth
COPY ground_truth /ground_truth

# Copy scripts
COPY scripts /scripts

# Copy report repository
RUN git clone https://github.com/vibhash-singh/repr-eng-report.git /report
COPY Makefile /Makefile 

CMD ["npm", "run", "dev"]

EXPOSE 4200
