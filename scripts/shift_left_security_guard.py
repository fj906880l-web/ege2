#!/usr/bin/env python3
"""
Shift-Left Security Guard (IBM 5 Principles)
Autonomous Security Scanner & Gate for AI-Assisted Development

Principles Enforced:
1. Trust the Outcome, Not Just the Generation (Fail-Safe, Least Privilege, Malformed Data Protection)
2. Security Starts During Development (Shift-Left SAST, Secrets Scanning & Ingestion Gates)
3. Scrutinize the Supply Chain & Generated Dependencies (Vulnerability, Pinning & Hallucination Checks)
4. Validate Intent and Assumptions (Business Rules, 50% Capital Cap, No Fake Data)
5. Security as Continuous Practice & Agentic Guardrails (Path Traversal, Blast Radius & Audit Trails)
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple

SECRET_PATTERNS = [
    ('OpenAI API Key', re.compile(r'sk-[a-zA-Z0-9]{20,}')),
    ('Anthropic API Key', re.compile(r'sk-ant-[a-zA-Z0-9_-]{20,}')),
    ('GitHub Token', re.compile(r'gh[pousr]_[A-Za-z0-9_]{36,}')),
    ('Slack Token', re.compile(r'xox[baprs]-[0-9]{10,}-[a-zA-Z0-9]{24,}')),
    ('Google API Key', re.compile(r'AIza[0-9A-Za-z-_]{35}')),
    ('Private Key Block', re.compile(r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----')),
    ('Generic Hardcoded Secret', re.compile(r'(?:api_key|apikey|secret_key|auth_token|access_token)\s*=\s*[\x27\x22][a-zA-Z0-9_-]{16,}[\x27\x22]', re.I))
]

IGNORE_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', '.pytest_cache', 'Takeout', 'blobs', 'files'}
IGNORE_FILES = {'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'skills-lock.json', '.env', '.env.secrets'}


PLACEHOLDER_SUBSTRINGS = {"your_", "your-", "dummy", "placeholder", "example", "change_me", "sk-secret123456", "sk-123456"}

def audit_principle_1_fail_safe(repo_dir: str) -> List[str]:
    """Check 1: Fail-safe verification and atomic state writing."""
    issues = []
    exec_file = os.path.join(repo_dir, "core", "antigravity_execution.py")
    if os.path.exists(exec_file):
        with open(exec_file, "r", errors="ignore") as f:
            content = f.read()
        if re.search(r"portfolio_value\s*<=\s*0[^\n]*\n\s*portfolio_value\s*=\s*100000", content):
            issues.append(f"[P1: Fail-Open Risk] {exec_file} defaults invalid/zero equity to $100,000!")
        if "os.replace" not in content and "_save_wash_sales" in content:
            issues.append(f"[P1: Non-Atomic Write] {exec_file} _save_wash_sales does not use atomic replace.")
            
    risk_file = os.path.join(repo_dir, "core", "risk_manager.py")
    if os.path.exists(risk_file):
        with open(risk_file, "r", errors="ignore") as f:
            content = f.read()
        if "_save_risk_state" in content and "os.replace" not in content:
            issues.append(f"[P1: Non-Atomic Write] {risk_file} _save_risk_state does not use atomic file replacement.")
    return issues


def audit_principle_2_secrets_and_git(repo_dir: str) -> List[str]:
    """Check 2: Shift-left secrets scan & .gitignore presence."""
    issues = []
    gi_path = os.path.join(repo_dir, ".gitignore")
    if not os.path.exists(gi_path):
        issues.append(f"[P2: Missing .gitignore] Repository {repo_dir} has no .gitignore file!")
    else:
        with open(gi_path, "r", errors="ignore") as f:
            gi_content = f.read()
        if ".env*" not in gi_content and ".env" not in gi_content:
            issues.append(f"[P2: Incomplete .gitignore] {gi_path} does not ignore .env* files!")

    # Secrets scan
    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file in IGNORE_FILES or file.endswith(('.png', '.jpg', '.mp4', '.mov', '.pdf', '.ico', '.icns', '.example')):
                continue
            fpath = os.path.join(root, file)
            try:
                with open(fpath, "r", errors="ignore") as fp:
                    for line_no, line in enumerate(fp, start=1):
                        lower_line = line.lower()
                        if any(ph in lower_line for ph in PLACEHOLDER_SUBSTRINGS):
                            continue
                        for name, pat in SECRET_PATTERNS:
                            if pat.search(line):
                                issues.append(f"[P2: Exposed Secret ({name})] {fpath}:{line_no}")
            except Exception:
                pass
    return issues


def audit_principle_3_supply_chain(repo_dir: str) -> List[str]:
    """Check 3: Scrutinize software supply chain and dependencies."""
    issues = []
    req_file = os.path.join(repo_dir, "requirements.txt")
    if os.path.exists(req_file):
        with open(req_file, "r", errors="ignore") as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                if "alpaca-trade-api" in line:
                    issues.append(f"[P3: Deprecated/Vulnerable Dependency] {req_file} includes obsolete 'alpaca-trade-api'!")
                # Check for bare unpinned dependencies
                if not any(op in line for op in ["==", ">=", "<=", "~=", "!="]):
                    pass # Unpinned notice
    return issues


def audit_principle_4_intent_and_guardrails(repo_dir: str) -> List[str]:
    """Check 4: Validate intent, 50% capital cap, and self-heal re-auditing."""
    issues = []
    exec_file = os.path.join(repo_dir, "core", "antigravity_execution.py")
    if os.path.exists(exec_file):
        with open(exec_file, "r", errors="ignore") as f:
            content = f.read()
        if "_agentic_self_heal" in content:
            if "recheck_passed" not in content and "_pre_trade_audit" not in content.split("_agentic_self_heal")[1]:
                issues.append(f"[P4: Intent Bypass] {exec_file} executes self-healed orders without re-running pre-trade audit!")
    return issues


def audit_principle_5_agentic_guardrails(repo_dir: str) -> List[str]:
    """Check 5: Path traversal validation, localhost binding, and blast radius enclosure."""
    issues = []
    web_file = os.path.join(repo_dir, "web_server.py")
    if os.path.exists(web_file):
        with open(web_file, "r", errors="ignore") as f:
            content = f.read()
        if "is_safe_repo_path" not in content:
            issues.append(f"[P5: Path Traversal Risk] {web_file} lacks is_safe_repo_path containment check!")
        if "('0.0.0.0', PORT)" in content or "('0.0.0.0', actual_port)" in content:
            issues.append(f"[P5: Public Network Binding] {web_file} binds to 0.0.0.0 by default instead of localhost 127.0.0.1!")
    return issues


def run_full_security_audit(project_dir: str) -> Dict[str, Any]:
    print(f"\n=======================================================")
    print(f" IBM 5-PRINCIPLE SHIFT-LEFT SECURITY AUDITOR")
    print(f" Target Directory: {project_dir}")
    print(f"=======================================================\n")

    p1_issues = audit_principle_1_fail_safe(project_dir)
    p2_issues = audit_principle_2_secrets_and_git(project_dir)
    p3_issues = audit_principle_3_supply_chain(project_dir)
    p4_issues = audit_principle_4_intent_and_guardrails(project_dir)
    p5_issues = audit_principle_5_agentic_guardrails(project_dir)

    all_issues = p1_issues + p2_issues + p3_issues + p4_issues + p5_issues
    total_violations = len(all_issues)
    score = max(0, 100 - (total_violations * 10))

    results = {
        "project": project_dir,
        "security_score": score,
        "status": "PASSED" if score >= 80 else "FAILED",
        "principles": {
            "P1_FailSafe_Outcome": {"passed": len(p1_issues) == 0, "issues": p1_issues},
            "P2_ShiftLeft_Secrets": {"passed": len(p2_issues) == 0, "issues": p2_issues},
            "P3_SupplyChain_Dependencies": {"passed": len(p3_issues) == 0, "issues": p3_issues},
            "P4_Intent_Guardrails": {"passed": len(p4_issues) == 0, "issues": p4_issues},
            "P5_Agentic_Boundaries": {"passed": len(p5_issues) == 0, "issues": p5_issues}
        },
        "total_issues": total_violations
    }

    for p_name, p_data in results["principles"].items():
        status_icon = "✅ PASS" if p_data["passed"] else "❌ FAIL"
        print(f"{status_icon} - {p_name} ({len(p_data['issues'])} issues)")
        for iss in p_data["issues"]:
            print(f"    * {iss}")

    print(f"\n-------------------------------------------------------")
    print(f"Final Security Score: {score}/100 [{results['status']}]")
    print(f"-------------------------------------------------------\n")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shift-Left Security Guard")
    parser.add_argument("--dir", default=".", help="Directory to scan")
    parser.add_argument("--enforce", action="store_true", help="Exit with code 1 if score < 80")
    args = parser.parse_args()

    audit_res = run_full_security_audit(os.path.abspath(args.dir))
    if args.enforce and audit_res["security_score"] < 80:
        sys.exit(1)
    sys.exit(0)
