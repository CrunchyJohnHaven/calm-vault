"""Calm Stack — the unified composition of Calm Pact, Calm Witness, and Calm Tenancy.

A Calm Session is a single end-to-end handshake that:
    1. Runs Calm Pact to verify directive equality (Pedersen + Σ-protocol).
    2. Runs Calm Witness to attest the principal's user-state (one bit).
    3. Runs Calm Tenancy to bound the surface on which both parties operate.

This package composes the three primitives without re-implementing any of them.
"""

__version__ = "0.0.1"
