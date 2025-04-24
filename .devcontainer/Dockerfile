# syntax=docker/dockerfile:1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# stage: builder for `task` binary

FROM golang:1.24.2-alpine3.21 AS stage-go

ENV GOBIN=/app/bin

WORKDIR /app

RUN set -eux; \
    go install github.com/go-task/task/v3/cmd/task@latest


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# stage: system layer and binaries

FROM python:3.12.10-alpine3.21
COPY --chmod=0777 --from=stage-go /app/bin/task /usr/local/bin/task

ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONUNBUFFERED=true

RUN set -eux; \
    addgroup \
        -g 1001 \
        developer \
    && \
    adduser \
        -D \
        -G developer \
        -h /home/developer \
        -s /bin/bash \
        -u 1001 \
        developer \
    && \
    install \
        -d \
        -m 0755 \
        /app \
    && \
    chown \
        -R \
        developer:developer \
        /app 

RUN set -eux; \
    apk add \
        --no-cache \
        --no-interactive \
        --progress \
        --timeout=60 \
        --upgrade \
        bash==5.2.37-r0 \
        git-bash-completion==2.47.2-r0 \
        git==2.47.2-r0 \
        openssh==9.9_p2-r0 \
        python3-dev==3.12.10-r0 \
    && \
    pip install \
        --upgrade \
        pip

RUN set -eux; \
    pip install \
        poetry==2.1.2

WORKDIR /app

USER developer

RUN echo source /usr/share/bash-completion/completions/git >> ~/.bashrc

ENTRYPOINT [ "pip", "freeze" ]
