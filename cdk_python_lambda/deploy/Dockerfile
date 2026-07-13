# Builds the application code, and runs the CDK to deploy it
#
FROM public.ecr.aws/lambda/python:3.14

ARG GITHUB_ACCESS_TOKEN
ARG NODE_VERSION=24.18.0

# Bootstrap image (cacheable). The Lambda Python 3.14 base image is Amazon Linux 2023,
# so any compiled dependencies are built against the same OS family as the runtime.
RUN dnf install -y git tar gzip xz && \
    dnf clean all

# CDK and dependencies
WORKDIR /deploy
RUN curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz" | tar -xJf -
ENV PATH="/deploy/node-v${NODE_VERSION}-linux-x64/bin:${PATH}"
RUN npm install -g aws-cdk@latest
COPY deploy/requirements.txt ./
RUN python -m pip --no-cache-dir install -r requirements.txt

# Application dependencies
# This supports your company's private github repos
# GITHUB_ACCESS_TOKEN should have read-only access to the code.
WORKDIR /app
COPY source/requirements.txt ./
RUN sed "s|git+ssh://git@github.com|git+https://$GITHUB_ACCESS_TOKEN@github.com|" requirements.txt \
    | python -m pip --no-cache-dir install -r /dev/stdin --target /app/layer/python

# All the other code/scripts.  These change often, do them last
COPY source/. /app/code/
COPY deploy/. /deploy/

# Python unicode breakage without this
ENV LANG=C.UTF-8

WORKDIR /deploy
ENTRYPOINT []
CMD [ "/bin/bash" ]
