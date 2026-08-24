#!/usr/bin/env python3
"""
EGE-2 Full-Stack REST API & Web Application Server (v2.1 Architecture)
---------------------------------------------------------------------
Serves the EGE-2 interactive web frontend, REST API endpoints,
managerial self-supervision (Μ-Engine), hot-swappable parameter graph,
symbolic compression, temporal memory, curriculum engine,
and model drop-in evaluation harness.

Zero external dependencies (Python 3.9+ standard library).

Endpoints:
  GET  /                     -> Serves interactive web UI (index.html)
  GET  /health               -> System health, active nodes, quantum metrics, manager status
  POST /api/evaluate         -> Evaluate claim/prompt through Phi/Psi/Sigma + MuEngine
  GET  /api/nodes            -> Query Epistemic Q-Graph nodes (filter by domain/tier)
  POST /api/nodes            -> Evidence-gated node insertion / belief update
  POST /api/measure          -> Collapse quantum superposition & propagate entanglement
  POST /api/qubo             -> Run QUBO global coherence Simulated Annealing solver
  POST /api/benchmark        -> Run 10-test model drop-in benchmark suite
  GET  /api/energy           -> Compute data center energy & cost reduction metrics
  GET  /api/mu_engine        -> Get Μ-Engine health scorecard and review history
  POST /api/mu_engine/review -> Trigger on-demand managerial review cycle
  GET  /api/parameters       -> Query dynamic ParameterGraph tunables and audit trail
  POST /api/parameters       -> Hot-swap / update runtime parameter
  POST /api/parameters/rollback -> Revert parameter to previous known good value
  GET  /api/curriculum       -> Get curriculum developmental stages and milestone progress
  POST /api/curriculum/advance -> Advance developmental stage
  POST /api/curriculum/heal  -> Trigger milestone gap diagnosis and micro-curriculum injection
  GET  /api/intent           -> Query IntentFoldingTracker divergence metrics
  POST /api/symbolic/compress-> Convert natural language claim to canonical symbolic representation

DISCLAIMER:
Experimental research software provided under the MIT License "AS IS" without warranty.
Not financial, investment, medical, healthcare, legal, or regulatory advice.
See DISCLAIMER.md for complete terms.
"""

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Optional, Any, Tuple, Union
import json
import os
import sys
import time

# Core EGE-2 engine imports
from ege2_quantum import (
    EvidenceTier,
    EpistemicNode,
    EpistemicGraph,
    EGE2Wrapper,
    StructuredResponse,
    get_default_epistemic_graph,
    MockLLM,
    QUBOArbitration,
    ParameterGraph,
    SelfHealingCurriculumEngine,
    IntentFoldingTracker,
    MuEngine,
    SymbolicCompressionEngine,
    SymbolicClaim,
)
from model_dropin import ModelBenchmarker, EnergyProfile, BENCHMARK_PROMPTS


# Global Shared Epistemic State
GRAPH = get_default_epistemic_graph()
PARAM_GRAPH = ParameterGraph()
CURRICULUM = SelfHealingCurriculumEngine(PARAM_GRAPH)
MOCK_LLM = MockLLM()
WRAPPER = EGE2Wrapper(MOCK_LLM, GRAPH, PARAM_GRAPH, CURRICULUM)


class EGE2RequestHandler(SimpleHTTPRequestHandler):
    """Handles EGE-2 REST API and static web requests."""

    def end_headers(self):
        # Enable CORS and disable caching for API development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def _send_json(self, status_code: int, data: Any):
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _read_json_body(self) -> Dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        raw_body = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(raw_body)
        except json.JSONDecodeError:
            return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # 1. Health Endpoint
        if path == "/health":
            stats = GRAPH.stats()
            return self._send_json(200, {
                "status": "healthy",
                "system": "EGE-2 Quantum Epistemic System (v2.1 Architecture)",
                "version": "2.1.0",
                "active_nodes": stats["active_nodes"],
                "superposed_nodes": stats["superposed_nodes"],
                "measured_nodes": stats["measured_nodes"],
                "mean_confidence": round(stats["avg_confidence"], 4),
                "domains": stats["domains"],
                "experience_chains": stats.get("experience_sequences_count", 0),
                "curriculum_stage": CURRICULUM.get_active_stage().stage_name,
                "mu_engine_status": "ONLINE",
                "timestamp": time.time(),
            })

        # 2. Nodes Query Endpoint
        elif path == "/api/nodes":
            domain = query.get("domain", ["general"])[0]
            min_conf = float(query.get("min_confidence", [0.0])[0])
            tier_filter = query.get("tier", [None])[0]

            nodes = GRAPH.query(domain, min_confidence=min_conf)
            if tier_filter:
                nodes = [n for n in nodes if n.evidence_tier.value == int(tier_filter)]

            return self._send_json(200, {
                "count": len(nodes),
                "nodes": [n.to_dict() for n in nodes]
            })

        # 3. Energy Calculator Endpoint
        elif path == "/api/energy":
            params_b = float(query.get("params_billions", [70.0])[0])
            queries = int(query.get("daily_queries", [1000000])[0])
            profile = EnergyProfile(model_params_billions=params_b, daily_queries=queries)
            return self._send_json(200, profile.compute_metrics())

        # 4. Μ-Engine Status & Scorecard
        elif path == "/api/mu_engine":
            return self._send_json(200, WRAPPER.mu_engine.to_dict())

        # 5. Parameter Graph Tunables
        elif path == "/api/parameters":
            return self._send_json(200, PARAM_GRAPH.to_dict())

        # 6. Curriculum Engine
        elif path == "/api/curriculum":
            return self._send_json(200, CURRICULUM.to_dict())

        # 7. Intent Folding Tracker
        elif path == "/api/intent":
            return self._send_json(200, WRAPPER.intent_tracker.to_dict())

        # 8. Root / Web App
        elif path == "/" or path == "/index.html":
            self.path = "/index.html"
            return super().do_GET()

        # 9. Fallback to static file serving
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        # 1. Evaluate Claim / Prompt
        if path == "/api/evaluate":
            prompt = body.get("prompt", "").strip()
            custom_output = body.get("custom_output")

            if not prompt:
                return self._send_json(400, {"error": "Missing 'prompt' parameter in request body"})

            if custom_output:
                custom_llm = lambda p: custom_output
                eval_wrapper = EGE2Wrapper(custom_llm, GRAPH, PARAM_GRAPH, CURRICULUM)
                resp: StructuredResponse = eval_wrapper.query(prompt)
            else:
                resp: StructuredResponse = WRAPPER.query(prompt)

            return self._send_json(200, {
                "prompt": prompt,
                "draft_output": resp.content,
                "sigma_verdict": resp.sigma_verdict,
                "confidence": round(resp.confidence, 4),
                "phi_assessment": resp.phi_assessment,
                "psi_assessment": resp.psi_assessment,
                "manipulation_detected": resp.manipulation_detected,
                "evidence_cited": resp.evidence_cited,
                "quantum_state": resp.quantum_state,
                "symbolic_hash": resp.symbolic_hash,
                "reason": resp.reason,
                "mu_verdict": resp.mu_verdict,
            })

        # 2. Add or Update Belief Node (Evidence-Gated)
        elif path == "/api/nodes":
            node_id = body.get("node_id")
            claim = body.get("claim")
            domain = body.get("domain", "general")
            tier_val = int(body.get("evidence_tier", 7))
            confidence = float(body.get("confidence", 0.5))
            mechanism = body.get("mechanism")
            falsifiability = body.get("falsifiability")

            if not node_id or not claim:
                return self._send_json(400, {"error": "Missing required fields: 'node_id' and 'claim'"})

            new_node = EpistemicNode(
                node_id=node_id,
                claim=claim,
                domain=domain,
                evidence_tier=EvidenceTier(tier_val),
                confidence=confidence,
                mechanism=mechanism,
                falsifiability=falsifiability,
            )

            if node_id in GRAPH.nodes:
                result = GRAPH.update_belief(node_id, new_node)
                status = 200 if "ACCEPTED" in result else 409
                return self._send_json(status, {"status": result, "node": new_node.to_dict()})
            else:
                GRAPH.add_node(new_node)
                return self._send_json(201, {"status": "CREATED", "node": new_node.to_dict()})

        # 3. Collapse Quantum Superposition
        elif path == "/api/measure":
            node_id = body.get("node_id")
            if not node_id:
                return self._send_json(400, {"error": "Missing 'node_id' parameter"})

            if node_id not in GRAPH.nodes:
                return self._send_json(404, {"error": f"Node '{node_id}' not found"})

            outcome = GRAPH.measure_node(node_id)
            node = GRAPH.nodes[node_id]
            return self._send_json(200, {
                "node_id": node_id,
                "measurement_outcome": outcome,
                "quantum_state": node.quantum_state.to_dict() if node.quantum_state else None,
                "confidence": node.confidence,
                "entangled_partners_updated": list(node.entangled_with),
            })

        # 4. QUBO Simulated Annealing Optimization
        elif path == "/api/qubo":
            domain = body.get("domain", "general")
            iterations = int(body.get("iterations", 1000))
            nodes = GRAPH.query(domain, min_confidence=0.0)

            if not nodes:
                return self._send_json(400, {"error": f"No active nodes found in domain '{domain}'"})

            qubo = QUBOArbitration(nodes)
            solution = qubo.solve_simulated_annealing(iterations=iterations)
            active_ids = [nodes[i].node_id for i in range(len(nodes)) if solution[i]]
            pruned_ids = [nodes[i].node_id for i in range(len(nodes)) if not solution[i]]

            return self._send_json(200, {
                "domain": domain,
                "total_nodes_evaluated": len(nodes),
                "active_coherent_nodes": active_ids,
                "pruned_incoherent_nodes": pruned_ids,
                "iterations": iterations,
            })

        # 5. Run Benchmark Suite
        elif path == "/api/benchmark":
            bench = ModelBenchmarker(MOCK_LLM, GRAPH)
            summary = bench.run_benchmark(verbose=False)
            return self._send_json(200, summary)

        # 6. Trigger Μ-Engine Review Cycle
        elif path == "/api/mu_engine/review":
            cycle = int(body.get("cycle", GRAPH.current_cycle))
            reviews = WRAPPER.mu_engine.run_review_cycle(cycle)
            return self._send_json(200, {
                "status": "COMPLETED",
                "reviews_generated": len(reviews),
                "reviews": [r.to_dict() for r in reviews],
            })

        # 7. Hot-Swap Parameter in ParameterGraph
        elif path == "/api/parameters":
            param_id = body.get("param_id")
            value = body.get("value")
            reason = body.get("reason", "Operator update via REST API")

            if not param_id or value is None:
                return self._send_json(400, {"error": "Missing 'param_id' or 'value'"})

            success = PARAM_GRAPH.set(param_id, value, modified_by="api_operator", reason=reason)
            if success:
                return self._send_json(200, {
                    "status": "UPDATED",
                    "param": PARAM_GRAPH.params[param_id].to_dict()
                })
            else:
                return self._send_json(422, {
                    "error": "Parameter update rejected: value outside permissible valid_range"
                })

        # 8. Rollback Parameter
        elif path == "/api/parameters/rollback":
            param_id = body.get("param_id")
            if not param_id:
                return self._send_json(400, {"error": "Missing 'param_id'"})

            success = PARAM_GRAPH.rollback(param_id)
            if success:
                return self._send_json(200, {
                    "status": "ROLLED_BACK",
                    "param": PARAM_GRAPH.params[param_id].to_dict()
                })
            else:
                return self._send_json(404, {"error": "Cannot rollback: parameter not found or no previous rollback value"})

        # 9. Advance Curriculum Stage
        elif path == "/api/curriculum/advance":
            CURRICULUM.advance_stage()
            return self._send_json(200, {
                "status": "ADVANCED",
                "active_stage": CURRICULUM.get_active_stage().to_dict()
            })

        # 10. Self-Healing Curriculum Remediation Trigger
        elif path == "/api/curriculum/heal":
            milestone = body.get("milestone", "MILESTONE_CURRENT")
            gap = body.get("gap", "Missing kinetic energy balance trials")
            remedy = CURRICULUM.handle_milestone_failure(milestone, gap)
            return self._send_json(200, {
                "status": "REMEDIAL_CURRICULUM_INJECTED",
                "remedy": remedy,
                "active_stage": CURRICULUM.get_active_stage().to_dict()
            })

        # 11. Symbolic Compression
        elif path == "/api/symbolic/compress":
            claim = body.get("claim", "")
            domain = body.get("domain", "general")
            tier_val = int(body.get("evidence_tier", 1))
            conf = float(body.get("confidence", 0.99))

            if not claim:
                return self._send_json(400, {"error": "Missing 'claim' parameter"})

            sym = SymbolicCompressionEngine.compress(claim, domain, EvidenceTier(tier_val), conf)
            return self._send_json(200, sym.to_dict())

        return self._send_json(404, {"error": "Endpoint not found"})


def run_server(port: int = 8000, host: str = "0.0.0.0"):
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, EGE2RequestHandler)
    print("=" * 76)
    print(f"  EGE-2 Full-Stack Epistemic Server (v2.1) running on http://localhost:{port}")
    print(f"  Interactive Web UI: http://localhost:{port}/")
    print(f"  Health Endpoint:    http://localhost:{port}/health")
    print(f"  REST API:           http://localhost:{port}/api/evaluate")
    print(f"  Μ-Engine Manager:   http://localhost:{port}/api/mu_engine")
    print("=" * 76)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server shutting down gracefully...]")
        httpd.shutdown()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    run_server(port=port)
