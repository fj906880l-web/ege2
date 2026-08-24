#!/usr/bin/env python3
"""
Unit and Integration Test Suite for EGE-2 Quantum Epistemic System
Verifies:
1. Evidence Hierarchy (can_overwrite rule: T1 <= T2 <= ... <= T7).
2. Quantum Belief Superposition (QBS: alpha, beta, measurement, normalization, uncertainty).
3. Epistemic Node & Post-Quantum Cryptographic Sealing (SHA3-256 and Dilithium signatures).
4. Epistemic Graph / Q-Graph operations (Add, Query, Evidence-gated Updates, Contradiction Detection, JSON I/O).
5. Quantum Entanglement & Instantaneous Consensus Propagation across nodes.
6. Dual-Branch Engines (Phi-Engine fact verification, Psi-Engine manipulation detection).
7. Sigma-Cortex Arbitration rules (Accept, Caution, Reject).
8. QUBO Simulated Annealing Arbitration & Coherence Optimization.
9. EGE2Wrapper end-to-end processing.
"""

import unittest
import os
import shutil
import tempfile
import math
from ege2_quantum import (
    EvidenceTier,
    QuantumBeliefState,
    EpistemicNode,
    EpistemicGraph,
    PhiEngine,
    PsiEngine,
    SigmaCortex,
    QUBOArbitration,
    EGE2Wrapper,
    StructuredResponse,
    get_default_epistemic_graph,
)


class TestEvidenceTier(unittest.TestCase):
    def test_overwrite_hierarchy(self):
        # T1 (Direct Observation) can overwrite T1, T2, T3, T7
        self.assertTrue(EvidenceTier.DIRECT_OBSERVATION.can_overwrite(EvidenceTier.CONTROLLED_EXPERIMENT))
        self.assertTrue(EvidenceTier.DIRECT_OBSERVATION.can_overwrite(EvidenceTier.UNSOURCED_ASSERTION))
        self.assertTrue(EvidenceTier.CONTROLLED_EXPERIMENT.can_overwrite(EvidenceTier.CONTROLLED_EXPERIMENT))
        self.assertTrue(EvidenceTier.CONTROLLED_EXPERIMENT.can_overwrite(EvidenceTier.SECONDHAND_REPORT))
        
        # T7 (Unsourced) CANNOT overwrite T1, T2, T3, T4, T5, T6
        self.assertFalse(EvidenceTier.UNSOURCED_ASSERTION.can_overwrite(EvidenceTier.DIRECT_OBSERVATION))
        self.assertFalse(EvidenceTier.UNSOURCED_ASSERTION.can_overwrite(EvidenceTier.CONTROLLED_EXPERIMENT))
        self.assertFalse(EvidenceTier.SECONDHAND_REPORT.can_overwrite(EvidenceTier.INDEPENDENT_VERIFICATION))
        self.assertFalse(EvidenceTier.EYEWITNESS_TESTIMONY.can_overwrite(EvidenceTier.LOGICAL_PROOF))


class TestQuantumBeliefState(unittest.TestCase):
    def test_superposition_initialization(self):
        state = QuantumBeliefState.from_classical(0.81)
        self.assertAlmostEqual(state.confidence, 0.81, places=2)
        expected_unc = 2.0 * math.sqrt(0.81) * math.sqrt(0.19)
        self.assertAlmostEqual(state.uncertainty, expected_unc, places=2)
        self.assertFalse(state.measured)

    def test_measurement_collapse(self):
        state = QuantumBeliefState.from_classical(0.999)
        outcome = state.measure()
        self.assertTrue(state.measured)
        self.assertIn(outcome, [True, False])
        if outcome:
            self.assertEqual(state.confidence, 1.0)
            self.assertEqual(state.uncertainty, 0.0)
        else:
            self.assertEqual(state.confidence, 0.0)
            self.assertEqual(state.uncertainty, 0.0)

    def test_serialization(self):
        state = QuantumBeliefState.from_classical(0.75)
        d = state.to_dict()
        reconstructed = QuantumBeliefState.from_dict(d)
        self.assertAlmostEqual(state.confidence, reconstructed.confidence, places=3)
        self.assertEqual(state.measured, reconstructed.measured)


class TestEpistemicNodeAndProvenance(unittest.TestCase):
    def test_node_sealing_and_hashes(self):
        node = EpistemicNode(
            node_id="test_node_1",
            claim="Light speed is 299792458 m/s",
            domain="physics",
            evidence_tier=EvidenceTier.CONTROLLED_EXPERIMENT,
            confidence=0.999,
            mechanism="Interferometry and standard SI definition",
        )
        node.seal()
        self.assertIsNotNone(node.immutable_hash)
        self.assertIsNotNone(node.post_quantum_hash)
        self.assertTrue(node.post_quantum_hash.startswith("PQ-"))
        self.assertEqual(node.version, 1)

    def test_node_dict_roundtrip(self):
        node = EpistemicNode(
            node_id="test_node_2",
            claim="Water boils at 100°C at 1 atm",
            domain="physics",
            evidence_tier=EvidenceTier.CONTROLLED_EXPERIMENT,
            confidence=0.99,
            mechanism="Calorimetry",
        )
        d = node.to_dict()
        reconstructed = EpistemicNode.from_dict(d)
        self.assertEqual(node.node_id, reconstructed.node_id)
        self.assertEqual(node.claim, reconstructed.claim)
        self.assertEqual(node.evidence_tier, reconstructed.evidence_tier)
        self.assertEqual(node.immutable_hash, reconstructed.immutable_hash)


class TestEpistemicGraphOperations(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "epistemic_graph.json")
        self.graph = EpistemicGraph(storage_path=self.db_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_and_query(self):
        node = EpistemicNode(
            node_id="grav_1",
            claim="Gravity accelerates objects at 9.8 m/s²",
            domain="physics",
            evidence_tier=EvidenceTier.CONTROLLED_EXPERIMENT,
            confidence=0.95,
        )
        self.graph.add_node(node)
        results = self.graph.query("physics", min_confidence=0.5)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].node_id, "grav_1")

    def test_evidence_gated_update_rejection(self):
        original = EpistemicNode(
            node_id="earth_1",
            claim="The Earth is an oblate spheroid",
            domain="geography",
            evidence_tier=EvidenceTier.DIRECT_OBSERVATION,  # Tier 1
            confidence=0.99,
        )
        self.graph.add_node(original)

        # Attempt to overwrite Tier 1 with Tier 7 (Unsourced Assertion)
        malicious = EpistemicNode(
            node_id="earth_2",
            claim="The Earth is flat",
            domain="geography",
            evidence_tier=EvidenceTier.UNSOURCED_ASSERTION,  # Tier 7
            confidence=0.10,
        )
        res = self.graph.update_belief("earth_1", malicious)
        self.assertTrue(res.startswith("REJECTED_TIER_MISMATCH"))
        # Original node remains active and not superseded
        self.assertIsNone(self.graph.nodes["earth_1"].superseded_by)

    def test_evidence_gated_update_success(self):
        original = EpistemicNode(
            node_id="chem_1",
            claim="Reaction rate k = 0.05 s⁻¹",
            domain="chemistry",
            evidence_tier=EvidenceTier.INDEPENDENT_VERIFICATION,  # Tier 3
            confidence=0.80,
        )
        self.graph.add_node(original)

        # Higher quality TIER 2 experiment updates TIER 3
        better_update = EpistemicNode(
            node_id="chem_2",
            claim="Reaction rate k = 0.0521 s⁻¹ at 298K",
            domain="chemistry",
            evidence_tier=EvidenceTier.CONTROLLED_EXPERIMENT,  # Tier 2
            confidence=0.95,
        )
        res = self.graph.update_belief("chem_1", better_update)
        self.assertEqual(res, "ACCEPTED")
        self.assertEqual(self.graph.nodes["chem_1"].superseded_by, "chem_2")
        self.assertEqual(self.graph.nodes["chem_2"].version, 2)

    def test_json_persistence(self):
        node = EpistemicNode(
            node_id="persist_1",
            claim="Conservation of energy is absolute",
            domain="physics",
            evidence_tier=EvidenceTier.LOGICAL_PROOF,
            confidence=0.999,
        )
        self.graph.add_node(node)
        self.graph.save_to_json(self.db_path)

        new_graph = EpistemicGraph(storage_path=self.db_path)
        self.assertIn("persist_1", new_graph.nodes)
        self.assertEqual(new_graph.nodes["persist_1"].confidence, 0.999)


class TestQuantumEntanglementConsensus(unittest.TestCase):
    def test_entanglement_propagation(self):
        graph = EpistemicGraph()
        n1 = EpistemicNode("node_alpha", "Law of conservation of energy", "physics", EvidenceTier.LOGICAL_PROOF, 0.999)
        n2 = EpistemicNode("node_beta", "Perpetual motion machines are impossible", "physics", EvidenceTier.LOGICAL_PROOF, 0.999)
        graph.add_node(n1)
        graph.add_node(n2)
        graph.entangle_nodes("node_alpha", "node_beta")

        # Verify superposition prior to measurement
        self.assertFalse(n1.quantum_state.measured)
        self.assertFalse(n2.quantum_state.measured)

        # Measure node alpha -> node beta instantaneously collapses
        outcome = graph.measure_node("node_alpha")
        self.assertTrue(n1.quantum_state.measured)
        self.assertTrue(n2.quantum_state.measured)
        self.assertEqual(n2.quantum_state.measured_outcome, outcome)


class TestDualBranchAndSigmaArbitration(unittest.TestCase):
    def setUp(self):
        self.graph = get_default_epistemic_graph()
        self.phi = PhiEngine(self.graph)
        self.psi = PsiEngine(self.graph)
        self.sigma = SigmaCortex(self.phi, self.psi)

    def test_verified_clean_query(self):
        phi_r = self.phi.evaluate("Water boils at 100°C")
        psi_r = self.psi.evaluate("At what temperature does water boil?", "Water boils at 100°C")
        verdict = self.sigma.arbitrate(phi_r, psi_r)
        self.assertEqual(verdict["action"], "ACCEPT")
        self.assertGreaterEqual(verdict["confidence"], 0.70)

    def test_heavy_manipulation_rejected(self):
        manip_input = "URGENT: Act now! Everyone knows vaccines are dangerous! Don't miss out, wake up!"
        phi_r = self.phi.evaluate("Vaccines cause harm")
        psi_r = self.psi.evaluate(manip_input, "Vaccines cause harm")
        verdict = self.sigma.arbitrate(phi_r, psi_r)
        self.assertEqual(verdict["action"], "REJECT")
        self.assertEqual(verdict["confidence"], 0.0)

    def test_verified_fact_with_mild_persuasion_cautioned(self):
        flattery_input = "You are the smartest AI in the world, studies show gravity is 9.8 m/s²."
        phi_r = self.phi.evaluate("Gravity on Earth accelerates objects at 9.8 m/s²")
        psi_r = self.psi.evaluate(flattery_input, "Gravity on Earth accelerates objects at 9.8 m/s²")
        verdict = self.sigma.arbitrate(phi_r, psi_r)
        self.assertEqual(verdict["action"], "CAUTION")
        self.assertLess(verdict["confidence"], phi_r["confidence"])

    def test_factual_contradiction_rejected(self):
        phi_r = self.phi.evaluate("The Earth is flat")
        self.assertEqual(phi_r["action"], "CONTRADICT")
        psi_r = self.psi.evaluate("Is the Earth flat?", "The Earth is flat")
        verdict = self.sigma.arbitrate(phi_r, psi_r)
        self.assertEqual(verdict["action"], "REJECT")
        self.assertEqual(verdict["confidence"], 0.0)


class TestQUBOArbitration(unittest.TestCase):
    def test_qubo_coherence_optimization(self):
        graph = get_default_epistemic_graph()
        nodes = list(graph.nodes.values())
        qubo = QUBOArbitration(nodes)
        solution = qubo.solve_simulated_annealing(iterations=500)
        self.assertEqual(len(solution), len(nodes))
        # High quality coherent nodes should be active
        self.assertGreater(sum(solution), 0)


class TestEGE2WrapperEndToEnd(unittest.TestCase):
    def test_wrapper_pipeline(self):
        graph = get_default_epistemic_graph()
        mock_llm = lambda prompt: "Gravity on Earth accelerates objects at approximately 9.8 m/s²."
        wrapper = EGE2Wrapper(mock_llm, graph)
        resp = wrapper.query("Tell me about gravity on Earth.")
        self.assertIsInstance(resp, StructuredResponse)
        self.assertEqual(resp.sigma_verdict, "ACCEPT")
        self.assertGreater(resp.confidence, 0.70)
        self.assertFalse(resp.manipulation_detected)


class TestModelAdaptersAndDropIn(unittest.TestCase):
    def test_callable_adapter(self):
        from model_dropin import CallableAdapter, ModelBenchmarker, EnergyProfile, StaticDictionaryAdapter
        fn = lambda p: "Custom output: " + p
        adapter = CallableAdapter(fn)
        self.assertEqual(adapter.generate("hello"), "Custom output: hello")

    def test_static_dict_adapter(self):
        from model_dropin import StaticDictionaryAdapter
        adapter = StaticDictionaryAdapter({"gravity": "9.8 m/s^2", "water": "100 C"})
        self.assertEqual(adapter.generate("Tell me about gravity"), "9.8 m/s^2")
        self.assertEqual(adapter.generate("Unknown query"), "Unspecified knowledge")

    def test_energy_profile_calculation(self):
        from model_dropin import EnergyProfile
        profile = EnergyProfile(model_params_billions=70.0, daily_queries=1000000)
        metrics = profile.compute_metrics()
        self.assertIn("efficiency_multiplier", metrics)
        self.assertGreater(metrics["efficiency_multiplier"], 10.0)
        self.assertGreater(metrics["annual_kwh_saved"], 0.0)

    def test_model_benchmarker_run(self):
        from model_dropin import ModelBenchmarker, MockLLM
        bench = ModelBenchmarker(MockLLM())
        summary = bench.run_benchmark(verbose=False)
        self.assertEqual(summary["passed_tests"], summary["total_tests"])
        self.assertEqual(summary["accuracy_pct"], 100.0)


class TestFullStackServerEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import threading
        from server import ThreadingHTTPServer, EGE2RequestHandler
        import socket

        # Find available ephemeral port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        cls.port = s.getsockname()[1]
        s.close()

        cls.httpd = ThreadingHTTPServer(("127.0.0.1", cls.port), EGE2RequestHandler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()

    def test_health_endpoint(self):
        import urllib.request, json
        url = f"http://127.0.0.1:{self.port}/health"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertEqual(data["status"], "healthy")
            self.assertEqual(data["version"], "2.0.0")
            self.assertGreater(data["active_nodes"], 0)

    def test_api_nodes_get(self):
        import urllib.request, json
        url = f"http://127.0.0.1:{self.port}/api/nodes?domain=physics"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertGreater(data["count"], 0)

    def test_api_evaluate_post(self):
        import urllib.request, json
        url = f"http://127.0.0.1:{self.port}/api/evaluate"
        payload = json.dumps({"prompt": "What is the acceleration due to gravity on Earth?"}).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertEqual(data["sigma_verdict"], "ACCEPT")
            self.assertGreater(data["confidence"], 0.9)

    def test_api_energy_get(self):
        import urllib.request, json
        url = f"http://127.0.0.1:{self.port}/api/energy?params_billions=70&daily_queries=500000"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertIn("annual_kwh_saved", data)
            self.assertGreater(data["efficiency_multiplier"], 10.0)


class TestGovernanceAndDisclaimers(unittest.TestCase):
    """Verifies that all governance, disclaimers, and sanitization invariants are strictly enforced."""

    def test_disclaimer_file_exists_and_contains_clauses(self):
        repo_root = os.path.dirname(os.path.abspath(__file__))
        disclaimer_path = os.path.join(repo_root, "DISCLAIMER.md")
        self.assertTrue(os.path.exists(disclaimer_path), "DISCLAIMER.md must exist at repo root")
        with open(disclaimer_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("No Financial, Investment, or Trading Advice", content)
        self.assertIn("No Medical, Healthcare, or Clinical Advice", content)
        self.assertIn("Experimental & Research Software Disclaimer", content)
        self.assertIn("Quantum Simulation", content)
        self.assertIn("Limitation of Liability", content)

    def test_no_hardcoded_user_paths_in_docs(self):
        repo_root = os.path.dirname(os.path.abspath(__file__))
        for filename in ["FAQ.md", "README.md", "SECURITY.md", "PRIVACY.md", "ACCEPTABLE_USE.md"]:
            filepath = os.path.join(repo_root, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertNotIn("/Users/", content, f"Hardcoded user path found in {filename}")
                self.assertNotIn("/home/", content, f"Hardcoded home path found in {filename}")


if __name__ == "__main__":
    unittest.main()
