# Use a minimal Alpine base image
FROM alpine:latest

# Install required packages
RUN apk add --no-cache ca-certificates tini wget bzip2

# Set the Restic version (update as needed)
ENV RESTIC_VERSION=0.15.2

# Download and install Restic
RUN wget https://github.com/restic/restic/releases/download/v${RESTIC_VERSION}/restic_${RESTIC_VERSION}_linux_amd64.bz2 && \
    bzip2 -d restic_${RESTIC_VERSION}_linux_amd64.bz2 && \
    chmod +x restic_${RESTIC_VERSION}_linux_amd64 && \
    mv restic_${RESTIC_VERSION}_linux_amd64 /usr/local/bin/restic

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["restic", "--help"]