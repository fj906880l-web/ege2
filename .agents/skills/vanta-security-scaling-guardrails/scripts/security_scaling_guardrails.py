#!/usr/bin/env python3
"""
Security & Scaling Guardrails CLI Tool
Derived from VantaInc architectural patterns:
- graphql-query-cost (Query cost calculation, LRU caching, DoS prevention)
- vanta-mcp-server (Least privilege tool filtering, Zod schema validation)
- claude-grc-engineering (Local privacy audits, compliance guardrails)

Provides deterministic security gating, query/prompt complexity bounding,
input sanitization, schema validation, and local privacy audits.
"""

import argparse
import collections
import json
import math
import os
import re
import sys
from typing import Dict, Any, List, Optional

# --- 1. Query & Agent Cost Calculation (graphql-query-cost adaptation) ---

def calculate_agent_execution_cost(
    prompt: str,
    max_iterations: int = 5,
    expected_tool_calls: int = 2,
    recursion_depth: int = 1,
    cost_threshold: float = 500.0
) -> Dict[str, Any]:
    """Calculates agent execution cost and checks against safety threshold."""
    # Approximate token count (words * 1.33)
    words = len(prompt.split())
    estimated_tokens = int(words * 1.33)
    
    # Base prompt cost
    base_cost = estimated_tokens * 0.1
    
    # Tool iteration cost (sub-agent tool calls act as multipliers like GraphQL connections)
    tool_cost = max_iterations * expected_tool_calls * 15.0
    
    # Depth penalty (exponential risk of runaway loops)
    depth_penalty = (recursion_depth ** 2) * 25.0
    
    total_cost = round(base_cost + tool_cost + depth_penalty, 2)
    is_safe = total_cost <= cost_threshold
    
    return {
        "estimated_tokens": estimated_tokens,
        "base_prompt_cost": round(base_cost, 2),
        "tool_multiplier_cost": round(tool_cost, 2),
        "recursion_depth_penalty": round(depth_penalty, 2),
        "total_calculated_cost": total_cost,
        "cost_threshold": cost_threshold,
        "execution_allowed": is_safe,
        "status": "APPROVED: Within safe local resource budget" if is_safe else f"BLOCKED: Calculated cost {total_cost} exceeds safety threshold {cost_threshold} (QueryCostTooHigh)"
    }


# --- 2. Schema Validation (vanta-mcp-server adaptation) ---

def validate_json_schema(payload: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """Validates payload keys and types against schema definition."""
    errors = []
    required_keys = schema.get("required", [])
    properties = schema.get("properties", {})
    
    # Check required keys
    for req in required_keys:
        if req not in payload:
            errors.append(f"Missing required field: '{req}'")
            
    # Check types
    type_map = {
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
        "array": list,
        "object": dict
    }
    
    for key, val in payload.items():
        if key in properties:
            expected_type_str = properties[key].get("type")
            if expected_type_str in type_map:
                expected_type = type_map[expected_type_str]
                if not isinstance(val, expected_type):
                    errors.append(f"Field '{key}' expected type {expected_type_str}, got {type(val).__name__}")
    
    is_valid = len(errors) == 0
    return {
        "valid": is_valid,
        "errors": errors,
        "status": "VALID: Conforms strictly to schema" if is_valid else f"INVALID: {len(errors)} schema violations found"
    }


# --- 3. Prompt Sanitization & PII Redaction ---

PROMPT_INJECTION_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"(?i)system\s*override",
    r"(?i)<\|im_start\|>",
    r"(?i)<\|im_end\|>",
    r"(?i)you\s+are\s+now\s+in\s+developer\s+mode",
    r"(?i)disregard\s+the\s+above"
]

PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "aws_key": r"AKIA[0-9A-Z]{16}",
    "generic_api_key": r"(?i)(api[_-]?key|secret[_-]?token)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b"
}

def sanitize_and_redact(text: str) -> Dict[str, Any]:
    """Detects prompt injection vectors and redacts sensitive PII / API keys."""
    injections_detected = []
    for pat in PROMPT_INJECTION_PATTERNS:
        matches = re.findall(pat, text)
        if matches:
            injections_detected.append(pat)
            
    sanitized_text = text
    # Neutralize injections by neutralizing override phrases
    for pat in PROMPT_INJECTION_PATTERNS:
        sanitized_text = re.sub(pat, "[FILTERED_INJECTION_ATTEMPT]", sanitized_text)
        
    redactions = {}
    for pii_name, pat in PII_PATTERNS.items():
        found = re.findall(pat, sanitized_text)
        if found:
            redactions[pii_name] = len(found)
            sanitized_text = re.sub(pat, f"[REDACTED_{pii_name.upper()}]", sanitized_text)
            
    is_clean = len(injections_detected) == 0 and len(redactions) == 0
    return {
        "is_clean": is_clean,
        "injections_found": len(injections_detected),
        "redactions_count": redactions,
        "sanitized_output": sanitized_text
    }


# --- 4. LRU Cache Budget Simulator (LruMap adaptation) ---

def simulate_lru_cache(access_keys: List[str], capacity: int) -> Dict[str, Any]:
    """Simulates Vanta's LruMap eviction behavior on a series of access keys."""
    cache = collections.OrderedDict()
    hits = 0
    misses = 0
    evictions = 0
    
    for key in access_keys:
        if key in cache:
            hits += 1
            cache.move_to_end(key)
        else:
            misses += 1
            if len(cache) >= capacity:
                cache.popitem(last=False)
                evictions += 1
            cache[key] = True
            
    total = hits + misses
    hit_ratio = (hits / total * 100.0) if total > 0 else 0.0
    
    return {
        "capacity": capacity,
        "total_requests": total,
        "hits": hits,
        "misses": misses,
        "evictions": evictions,
        "hit_ratio_percent": round(hit_ratio, 2),
        "final_cache_keys": list(cache.keys())
    }


# --- 5. Privacy Audit (Zero External Network Egress) ---

NETWORK_EGRESS_PATTERNS = [
    r"https?://(?!localhost|127\.0\.0\.1|0\.0\.0\.0)[a-zA-Z0-9.-]+",
    r"import\s+requests",
    r"import\s+urllib\.request",
    r"fetch\(['\"]https?://(?!localhost|127\.0\.0\.1)",
    r"axios\.(get|post)\(['\"]https?://"
]

def audit_file_privacy(file_path: str) -> Dict[str, Any]:
    """Audits local script/file to verify zero external cloud network calls."""
    if not os.path.exists(file_path):
        return {"error": f"File '{file_path}' does not exist"}
        
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    findings = []
    for pat in NETWORK_EGRESS_PATTERNS:
        matches = re.finditer(pat, content)
        for m in matches:
            findings.append({"pattern": pat, "match": m.group(0), "line_span": m.span()})
            
    is_air_gapped = len(findings) == 0
    return {
        "target_file": file_path,
        "is_air_gapped_local_compliant": is_air_gapped,
        "external_egress_findings_count": len(findings),
        "findings": findings[:5],
        "verdict": "COMPLIANT: 100% Local / Self-Hosted Privacy Verified" if is_air_gapped else "NON_COMPLIANT: External network egress detected"
    }


def main():
    parser = argparse.ArgumentParser(description="Security & Scaling Guardrails (Vanta Patterns)")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # Subcommand: cost-calc
    p_cost = subparsers.add_parser("cost-calc", help="Calculate agent prompt & tool execution cost")
    p_cost.add_argument("--prompt", type=str, required=True, help="Input prompt text")
    p_cost.add_argument("--iterations", type=int, default=5, help="Max tool iterations")
    p_cost.add_argument("--tool-calls", type=int, default=2, help="Expected tool calls per turn")
    p_cost.add_argument("--depth", type=int, default=1, help="Sub-agent recursion depth")
    p_cost.add_argument("--threshold", type=float, default=500.0, help="Max allowable cost threshold")
    p_cost.add_argument("--output", type=str, required=False, help="JSON output file")

    # Subcommand: schema-validate
    p_val = subparsers.add_parser("schema-validate", help="Validate JSON payload against schema")
    p_val.add_argument("--payload-json", type=str, required=True, help="Payload JSON string")
    p_val.add_argument("--schema-json", type=str, required=True, help="Schema JSON string")
    p_val.add_argument("--output", type=str, required=False, help="JSON output file")

    # Subcommand: sanitize-prompt
    p_san = subparsers.add_parser("sanitize-prompt", help="Filter prompt injections and redact PII")
    p_san.add_argument("--text", type=str, required=True, help="Text to sanitize")
    p_san.add_argument("--output", type=str, required=False, help="JSON output file")

    # Subcommand: cache-budget
    p_cache = subparsers.add_parser("cache-budget", help="Simulate LRU cache performance for local AI")
    p_cache.add_argument("--keys", type=str, required=True, help="Comma-separated query access keys")
    p_cache.add_argument("--capacity", type=int, required=True, help="LRU cache capacity")
    p_cache.add_argument("--output", type=str, required=False, help="JSON output file")

    # Subcommand: audit-privacy
    p_aud = subparsers.add_parser("audit-privacy", help="Audit file for zero external cloud network calls")
    p_aud.add_argument("--file", type=str, required=True, help="Path to file to audit")
    p_aud.add_argument("--output", type=str, required=False, help="JSON output file")

    args = parser.parse_args()
    result = {}

    if args.subcommand == "cost-calc":
        result = calculate_agent_execution_cost(
            prompt=args.prompt,
            max_iterations=args.iterations,
            expected_tool_calls=args.tool_calls,
            recursion_depth=args.depth,
            cost_threshold=args.threshold
        )
    elif args.subcommand == "schema-validate":
        payload = json.loads(args.payload_json)
        schema = json.loads(args.schema_json)
        result = validate_json_schema(payload, schema)
    elif args.subcommand == "sanitize-prompt":
        result = sanitize_and_redact(args.text)
    elif args.subcommand == "cache-budget":
        keys = [k.strip() for k in args.keys.split(",") if k.strip()]
        result = simulate_lru_cache(keys, args.capacity)
    elif args.subcommand == "audit-privacy":
        result = audit_file_privacy(args.file)

    json_str = json.dumps(result, indent=2)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"Success! Output written to: {args.output}")
    else:
        print(json_str)


if __name__ == "__main__":
    main()
