# BitRep Threat Model

This document outlines the threat model for BitRep’s identity, attestation, reputation, and governance layers. It defines what the system defends against, what it does not, and the assumptions underlying the protocol.

## Security Goals
- ensure identities cannot be forged
- ensure attestations cannot be tampered with
- ensure reputation scores are deterministic and auditable
- limit the impact of Sybil attacks
- prevent unauthorized modification of proposals, votes, or tallies
- avoid leaking sensitive graph structure where possible

## Out-of-Scope Goals
BitRep does not attempt to:
- guarantee privacy of raw reputation scores
- prevent metadata leakage from network traffic
- secure client devices or key storage
- enforce honest behavior from issuers
- prevent denial-of-service attacks
- provide production-grade zero-knowledge privacy

## Assets
- identity keypairs
- attestation records
- trust graph structure
- reputation scores and caches
- governance proposals and votes
- API request/response integrity

## Adversary Capabilities
Attackers may:
- create unlimited identities (Sybil capability)
- issue arbitrary attestations
- attempt to manipulate reputation scores
- observe network traffic
- compromise storage or logs
- submit malicious API payloads
- attempt to dominate governance proposals

Attackers are *not* assumed to:
- break RSA-2048
- compromise the server runtime environment
- intercept private keys stored securely by users
- control a majority of all identities globally

## Threats and Mitigations

### Identity Forgery
**Threat:** attacker attempts to impersonate another identity.  
**Mitigation:** RSA signatures; deterministic verification; no shared secrets.

### Attestation Manipulation
**Threat:** attacker modifies or injects forged attestations.  
**Mitigation:** signatures on all attestations; strict validation; timestamp checks.

### Sybil Amplification
**Threat:** attacker creates many identities to inflate reputation.  
**Mitigation:** issuer-weight normalization; cluster detection; propagation damping.

### Graph Poisoning
**Threat:** attacker issues malicious attestations to distort trust graph.  
**Mitigation:** weighted propagation; issuer credibility; bounded influence.

### Governance Capture
**Threat:** attacker attempts to dominate voting.  
**Mitigation:** quadratic voting; reputation-weighted power; deterministic tallies.

### Privacy Leakage
**Threat:** attacker infers sensitive relationships from graph structure.  
**Mitigation:** coarse-grained score bands; optional ZK threshold proofs.

## Residual Risks
- large, coordinated Sybil clusters may still influence outcomes
- metadata leakage from API usage patterns
- ZK framework is experimental and not suitable for high-assurance privacy
- compromised client devices undermine identity security

## Assumptions
- cryptographic primitives remain secure
- server environment is not compromised
- contributors act in good faith unless proven otherwise
- users manage their private keys responsibly

## Summary
BitRep is designed to resist identity forgery, attestation tampering, graph manipulation, and governance capture. It does not attempt to solve client-side security, metadata privacy, or advanced adversarial coordination. The system is secure when used within these boundaries.
