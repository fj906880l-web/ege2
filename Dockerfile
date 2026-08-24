# ==============================================================================
# EGE-2 Quantum Epistemic System — Production Docker Container
# Ultra-lightweight, zero-dependency, secure runtime
# ==============================================================================

FROM python:3.11-slim

LABEL maintainer="Collaborative Architecture Design"
LABEL description="EGE-2 Quantum Epistemic System Full-Stack Runtime"
LABEL version="2.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Create non-root user for security hardening
RUN groupadd -r ege2 && useradd -r -g ege2 -d /app -s /sbin/nologin ege2

WORKDIR /app

# Copy application files
COPY --chown=ege2:ege2 . /app/

# Make scripts executable
RUN chmod +x /app/server.py /app/ege2_quantum.py /app/model_dropin.py

# Switch to non-root user
USER ege2

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

EXPOSE 8000

# Run full-stack server
CMD ["python3", "server.py"]
