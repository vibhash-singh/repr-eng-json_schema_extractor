FROM ubuntu:22.04
RUN apt-get update --fix-missing
RUN apt-get clean
RUN apt-get install -y git g++ vim iputils-ping curl make python3 jq

# Install Node16.x
RUN apt-get install -y ca-certificates gnupg
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
ENV NODE_MAJOR=16
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" |  tee /etc/apt/sources.list.d/nodesource.list
RUN apt-get update
RUN apt-get install nodejs -y

RUN git clone https://github.com/feekosta/JSONSchemaDiscovery.git
WORKDIR /JSONSchemaDiscovery
# RUN git checkout tags/1.1.0

#RUN npm install -g npm@10.2.5
RUN npm install -g @angular/cli
RUN npm install -g typescript
RUN npm install

COPY npm-dev.patch /JSONSchemaDiscovery
RUN git apply npm-dev.patch

COPY smoke.sh /
RUN chmod +x /smoke.sh

COPY report /report

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get install -y texlive-latex-base texlive-xetex texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra

CMD ["npm", "run", "dev"]

COPY Makefile /Makefile
RUN cd .. && make report

EXPOSE 4200
EXPOSE 3000