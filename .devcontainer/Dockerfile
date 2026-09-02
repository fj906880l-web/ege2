# Hardened Developer Isolation Environment (SEC-PROTO-2026-04 v2.4)
FROM alpine:latest

# Install essential build and runtime tools
RUN apk add --no-cache bash git curl nodejs npm python3 py3-pip shadow \
    && useradd -m -u 1000 -s /bin/bash developer

WORKDIR /workspace
USER developer
