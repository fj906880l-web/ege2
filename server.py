#!/usr/bin/env python3
"""
EGE-2 Full-Stack REST API & Web Application Server
--------------------------------------------------
Serves the EGE-2 interactive web frontend, REST API endpoints,
and model drop-in evaluation harness.

Zero external dependencies (Python 3.9+ standard library).

Endpoints:
  GET  /                     -> Serves interactive web UI (index.html)
  GET  /health               -> System health, active nodes, quantum metrics
  POST /api/evaluate         -> Evaluate claim/prompt through Phi/Psi/Sigma
  GET  /api/nodes            -> Query Epistemic Q-Graph nodes (filter by domain/tier)
  POST /api/nodes            -> Evidence-gated node insertion / belief update
  POST /api/measure          -> Collapse quantum superposition & propagate entanglement
  POST /api/qubo             -> Run QUBO global coherence Simulated Annealing solver
  POST /api/benchmark        -> Run 10-test model drop-in benchmark suite
  GET  /api/energy           -> Compute data center energy & cost reduction metrics
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
)
from model_dropin import ModelBenchmarker, EnergyProfile, BENCHMARK_PROMPTS


# Global Shared Epistemic State
GRAPH = get_default_epistemic_graph()
MOCK_LLM = MockLLM()
WRAPPER = EGE2Wrapper(MOCK_LLM, GRAPH)


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
                "system": "EGE-2 Quantum Epistemic System",
                "version": "2.0.0",
                "active_nodes": stats["active_nodes"],
                "superposed_nodes": stats["superposed_nodes"],
                "measured_nodes": stats["measured_nodes"],
                "mean_confidence": round(stats["avg_confidence"], 4),
                "domains": stats["domains"],
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

        # 4. Root / Web App
        elif path == "/" or path == "/index.html":
            self.path = "/index.html"
            return super().do_GET()

        # 5. Fallback to static file serving
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
                # Custom model response supplied
                custom_llm = lambda p: custom_output
                eval_wrapper = EGE2Wrapper(custom_llm, GRAPH)
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
                "reason": resp.reason,
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

        return self._send_json(404, {"error": "Endpoint not found"})


def run_server(port: int = 8000, host: str = "0.0.0.0"):
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, EGE2RequestHandler)
    print("=" * 76)
    print(f"  EGE-2 Full-Stack Epistemic Server running on http://localhost:{port}")
    print(f"  Interactive Web UI: http://localhost:{port}/")
    print(f"  Health Endpoint:    http://localhost:{port}/health")
    print(f"  REST API:           http://localhost:{port}/api/evaluate")
    print("=" * 76)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server shutting down gracefully...]")
        httpd.shutdown()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    run_server(port=port)
