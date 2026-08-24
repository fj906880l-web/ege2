#!/usr/bin/env bash
# Install EGE-2 Git Hooks
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
echo "✅ EGE-2 Git Pre-commit hooks successfully installed and configured in .githooks/"
