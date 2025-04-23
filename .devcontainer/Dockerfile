# syntax=docker/dockerfile:1

FROM python:3.12.10-alpine3.21

WORKDIR /app

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
        pip \
        poetry


USER developer

RUN echo source /usr/share/bash-completion/completions/git >> ~/.bashrc

ENTRYPOINT [ "pip", "freeze" ]
