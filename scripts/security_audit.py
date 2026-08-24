#!/usr/bin/env python3
"""
EGE-2 Repository Security, Secret & Disclaimers Auditor
Zero external dependencies.
"""

import os
import re
import sys

SECRET_PATTERNS = [
    ("Google API Key", re.compile(r"AIza[0-9A-Za-z-_]{35}")),
    ("OpenAI / Anthropic Secret Key", re.compile(r"sk-[a-zA-Z0-9]{32,}")),
    ("GitHub Personal Access Token", re.compile(r"ghp_[a-zA-Z0-9]{36}")),
    ("GitHub OAuth / App Token", re.compile(r"gho_[a-zA-Z0-9]{36}")),
    ("Private Key Block", re.compile(r"-----BEGIN (?:RSA|EC|DSA|OPENSSH) PRIVATE KEY-----")),
]

SCANNED_EXTENSIONS = (
    ".py", ".json", ".html", ".sh", ".yml", ".yaml", ".env", ".cfg", ".ini", ".toml"
)

EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".hypothesis"}

def run_audit(target_dir: str = ".") -> int:
    print(f"🔒 Running EGE-2 Security, Credential & Sanitization Audit on '{target_dir}'...")
    found_secrets = 0
    scanned_files = 0

    # 1. Verify DISCLAIMER.md exists
    disclaimer_path = os.path.join(target_dir, "DISCLAIMER.md")
    if not os.path.exists(disclaimer_path):
        print("❌ CRITICAL: DISCLAIMER.md is missing from repository root!")
        return 1
    print("✅ DISCLAIMER.md verified at repository root.")

    # 2. Verify .gitignore protection
    gitignore_path = os.path.join(target_dir, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            gi_content = f.read()
        for required_rule in [".env", "credentials", "service_account", "id_rsa"]:
            if required_rule not in gi_content:
                print(f"❌ WARNING: Required ignore pattern '{required_rule}' missing from .gitignore")
                return 1
        print("✅ Strict .gitignore rules verified.")

    # 3. Scan code and config files for secret patterns and hardcoded local user paths
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            # Check for illegal sensitive file names
            if file in {"credentials.json", "service_account.json", "id_rsa", "id_ed25519"}:
                print(f"❌ CRITICAL ERROR: Unignored credential file found: {os.path.join(root, file)}")
                found_secrets += 1

            if file.endswith(SCANNED_EXTENSIONS) or file == "Dockerfile":
                scanned_files += 1
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        for line_idx, line in enumerate(f, 1):
                            for name, pattern in SECRET_PATTERNS:
                                if pattern.search(line):
                                    print(f"❌ Potential {name} detected in {filepath}:{line_idx}")
                                    found_secrets += 1
                except Exception as e:
                    print(f"⚠️ Error reading {filepath}: {e}")

    # 4. Check documentation files for hardcoded personal paths
    for doc in ["FAQ.md", "README.md", "SECURITY.md", "PRIVACY.md", "ACCEPTABLE_USE.md", "DISCLAIMER.md"]:
        doc_path = os.path.join(target_dir, doc)
        if os.path.exists(doc_path):
            with open(doc_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "/Users/" in content:
                    print(f"❌ Hardcoded '/Users/' path detected in {doc}")
                    found_secrets += 1

    print(f"📊 Audit Complete: Scanned {scanned_files} source files.")
    if found_secrets == 0:
        print("✅ Security audit passed with 100% clean score (0 vulnerabilities, 0 exposed secrets).")
        return 0
    else:
        print(f"❌ Security audit failed: {found_secrets} issue(s) detected.")
        return 1

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(run_audit(target))
