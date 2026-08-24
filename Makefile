.PHONY: help test benchmark run docker-build docker-run security-audit clean

help:
	@echo "EGE-2 Quantum Epistemic System — Build & Automation Commands"
	@echo "============================================================"
	@echo "  make test            Run all 27 unit and integration tests"
	@echo "  make benchmark       Run 10-test model drop-in benchmark suite"
	@echo "  make run             Start full-stack REST server & Web App (port 8000)"
	@echo "  make docker-build    Build production Docker image"
	@echo "  make docker-run      Run service via Docker Compose"
	@echo "  make security-audit  Run security scanner and mind virus defense audit"
	@echo "  make clean           Clean up python cache and temporary files"

test:
	python3 -m unittest test_ege2_quantum.py -v

benchmark:
	python3 -c "from model_dropin import ModelBenchmarker, MockLLM; ModelBenchmarker(MockLLM()).run_benchmark(verbose=True)"

run:
	python3 server.py

docker-build:
	docker build -t ege2-quantum-system:latest .

docker-run:
	docker compose up -d

security-audit:
	python3 scripts/security_audit.py


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
