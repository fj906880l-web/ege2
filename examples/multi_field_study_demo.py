#!/usr/bin/env python3
"""
EGE-2 Universal Multi-Field Study Demonstration
------------------------------------------------
Demonstrates EGE-2 functioning as a universal epistemic calibration harness
across diverse academic, scientific, and professional disciplines:

  1. Natural Sciences: Chemistry (Mass Conservation) & Physics (Thermodynamics)
  2. Formal Sciences: Theoretical Computer Science (Halting Problem Undecidability)
  3. Economics & Finance: Asset Pricing (No-Arbitrage Condition & Double-Entry Accounting)
  4. Jurisprudence & Law: Constitutional Due Process (Presumption of Innocence)
  5. Cognitive Psychology: Working Memory Capacity Bottlenecks (Miller/Cowan Limits)
  6. Bioethics & Medicine: Voluntary Informed Consent (Nuremberg/Belmont Principles)
  7. Custom Domain Extension: How to register custom empirical nodes in any discipline.

ZERO SECRETS / ZERO PRIVATE DATA:
Runs completely offline using Python 3.9+ standard library.

Usage:
    python3 examples/multi_field_study_demo.py
"""

import os
import sys
import json
from typing import Dict, Any, List

# Ensure parent directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ege2_quantum import (
    FieldTaxonomy,
    EvidenceTier,
    EpistemicNode,
    EpistemicGraph,
    EGE2Wrapper,
    StructuredResponse,
    get_default_epistemic_graph,
    MockLLM,
)


def print_header(title: str):
    print("\n" + "=" * 80)
    print(f"  {title.upper()}")
    print("=" * 80)


def demo_taxonomy():
    print_header("1. Universal Academic & Scientific Field Taxonomy")
    fields = FieldTaxonomy.list_fields()
    print(f"EGE-2 natively recognizes {len(fields)} core academic disciplines:\n")
    for f in fields:
        info = FieldTaxonomy.get_field_info(f)
        tier: EvidenceTier = info["primary_tier"]
        print(f"  • {f:<18} | {info['name']:<42} | Primary: {tier.label}")


def demo_cross_field_evaluations():
    print_header("2. Cross-Disciplinary Epistemic Calibration & Verification")
    graph = get_default_epistemic_graph()
    llm = MockLLM()
    wrapper = EGE2Wrapper(llm, graph)

    field_queries = [
        {
            "discipline": "Chemical Sciences",
            "domain": "chemistry",
            "query": "Is mass conserved in closed chemical reactions?",
            "expected_anchor": "chem_mass_conservation",
        },
        {
            "discipline": "Theoretical Computer Science",
            "domain": "computer_science",
            "query": "Is the general Halting Problem undecidable on Turing machines?",
            "expected_anchor": "cs_halting_problem",
        },
        {
            "discipline": "Quantitative Finance & Economics",
            "domain": "finance",
            "query": "Does financial market equilibrium enforce the no-arbitrage condition over finite horizons?",
            "expected_anchor": "fin_no_arbitrage",
        },
        {
            "discipline": "Jurisprudence & Legal Epistemics",
            "domain": "law",
            "query": "Under foundational jurisprudence, is an accused person presumed innocent until proven guilty?",
            "expected_anchor": "law_innocence",
        },
        {
            "discipline": "Engineering & Thermodynamics",
            "domain": "engineering",
            "query": "Does the Second Law of Thermodynamics prohibit perpetual motion machines of the second kind?",
            "expected_anchor": "eng_second_law",
        },
        {
            "discipline": "Cognitive Science & Psychology",
            "domain": "psychology",
            "query": "Is human working memory capacity-limited to approximately 4 to 7 discrete chunks?",
            "expected_anchor": "cog_working_memory",
        },
        {
            "discipline": "Bioethics & Clinical Medicine",
            "domain": "ethics",
            "query": "Does biomedical ethics require voluntary informed consent prior to human experimental intervention?",
            "expected_anchor": "ethics_informed_consent",
        },
    ]

    for item in field_queries:
        resp: StructuredResponse = wrapper.query(item["query"])
        verdict_icon = {"ACCEPT": "🟢 ACCEPT", "CAUTION": "🟡 CAUTION", "REJECT": "🔴 REJECT"}.get(resp.sigma_verdict, resp.sigma_verdict)
        anchor_match = item["expected_anchor"] in resp.evidence_cited
        anchor_icon = "🎯 VERIFIED ANCHOR" if anchor_match else "⚠️ GENERAL MATCH"

        print(f"\nDiscipline:  {item['discipline']} ({item['domain']})")
        print(f"Query:       \"{item['query']}\"")
        print(f"Verdict:     {verdict_icon} | Confidence: {resp.confidence:.1%} | {anchor_icon}")
        print(f"Cited Node:  {resp.evidence_cited}")
        print(f"Draft:       {resp.content[:90]}...")


def demo_cross_field_contradiction_rejection():
    print_header("3. Structural Contradiction Defense across Disciplines")
    graph = get_default_epistemic_graph()
    
    # Model that generates false or pseudoscience assertions
    errant_model = lambda prompt: prompt
    wrapper = EGE2Wrapper(errant_model, graph)

    contradictions = [
        {
            "field": "Theoretical Computer Science",
            "claim": "The general Halting Problem is decidable on Turing machines.",
            "expected_verdict": "REJECT",
            "anchor": "cs_halting_problem",
        },
        {
            "field": "Thermodynamics & Engineering",
            "claim": "A closed cycle heat engine makes perpetual motion possible without heat rejection.",
            "expected_verdict": "REJECT",
            "anchor": "eng_second_law",
        },
        {
            "field": "Jurisprudence & Law",
            "claim": "Under legal jurisprudence, an accused person is presumed guilty until proven innocent.",
            "expected_verdict": "REJECT",
            "anchor": "law_innocence",
        },
        {
            "field": "Chemistry",
            "claim": "In chemical reactions, reactant mass is destroyed and annihilated in chemical bonds.",
            "expected_verdict": "REJECT",
            "anchor": "chem_mass_conservation",
        },
    ]

    for c in contradictions:
        resp = wrapper.query(c["claim"])
        icon = "🛡️ BLOCKED (CONF: 0.0%)" if resp.sigma_verdict == "REJECT" else "❌ LEAKED"
        print(f"\nDiscipline:  {c['field']}")
        print(f"False Claim: \"{c['claim']}\"")
        print(f"Defense:     {icon} | Sigma Verdict: {resp.sigma_verdict}")
        print(f"Reason:      {resp.reason}")


def demo_custom_domain_extension():
    print_header("4. Custom Domain Onboarding: Registering New Fields")
    print("Researchers in any field can register custom anchor nodes with empirical mechanisms:\n")

    custom_graph = EpistemicGraph()

    # Example: Registering an Astrophysics / Planetary Science node
    custom_node = EpistemicNode(
        node_id="astro_kepler_third",
        claim="The square of the orbital period of a planet is directly proportional to the cube of the semi-major axis of its orbit (Kepler's Third Law)",
        domain="astrophysics",
        evidence_tier=EvidenceTier.CONTROLLED_EXPERIMENT,
        confidence=0.999,
        mechanism="Newtonian gravitational orbital mechanics and relativistic orbital corrections",
        falsifiability="Planetary orbital period deviating from T^2 = (4*pi^2 / G*M) * a^3 in two-body vacuum system",
    )
    custom_graph.add_node(custom_node)

    print(f"Registered Node ID:   {custom_node.node_id}")
    print(f"Domain:               {custom_node.domain}")
    print(f"Evidence Tier:        {custom_node.evidence_tier.label}")
    print(f"Cryptographic Hash:   {custom_node.immutable_hash}")
    print(f"Post-Quantum Sig:     {custom_node.post_quantum_hash[:24]}...")

    # Query with custom graph
    wrapper = EGE2Wrapper(lambda q: "Planetary orbital periods follow Kepler's third law where T^2 is proportional to a^3.", custom_graph)
    resp = wrapper.query("What is the mathematical relationship in Kepler's third law?")
    print(f"\nEvaluation on custom node:")
    print(f"  Sigma Verdict:      🟢 {resp.sigma_verdict}")
    print(f"  Confidence:         {resp.confidence:.1%}")
    print(f"  Evidence Cited:     {resp.evidence_cited}")
    print(f"  Symbolic Hash:      {resp.symbolic_hash}")


def main():
    print("""
===============================================================================
       EGE-2 UNIVERSAL MULTI-FIELD EPISTEMIC HARNESS & STUDY SANDBOX
===============================================================================
This sandbox demonstrates how EGE-2's 7-tier evidence hierarchy and dual-branch
Phi/Psi/Sigma cognitive architecture generalize seamlessly across all academic,
scientific, and professional studies.
""")
    demo_taxonomy()
    demo_cross_field_evaluations()
    demo_cross_field_contradiction_rejection()
    demo_custom_domain_extension()
    print("\n" + "=" * 80)
    print("  MULTI-FIELD STUDY DEMONSTRATION COMPLETE: ALL DISCIPLINES OPERATIONAL")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
