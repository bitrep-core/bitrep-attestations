# BitRep — Verifiable, Portable Reputation

BitRep is a protocol and reference implementation for **verifiable reputation** built on cryptographic identity, attestations, trust propagation, and decentralized governance. It provides a reputation layer that is **portable**, **auditable**, and **independent** of any single platform.

## Features
- **[self‑sovereign identity](guide://action?prefill=Tell%20me%20more%20about%3A%20self%E2%80%91sovereign%20identity)** — RSA keypairs with verification endpoints  
- **[signed attestations](guide://action?prefill=Tell%20me%20more%20about%3A%20signed%20attestations)** — weighted, verifiable, Sybil‑resistant trust links  
- **[reputation scoring](guide://action?prefill=Tell%20me%20more%20about%3A%20reputation%20scoring)** — trust propagation using a modified PageRank model  
- **[governance](guide://action?prefill=Tell%20me%20more%20about%3A%20governance)** — reputation‑weighted voting with quadratic scaling  
- **[privacy layer](guide://action?prefill=Tell%20me%20more%20about%3A%20privacy%20layer)** — ZK framework and selective disclosure of reputation bands  
- **[integrations](guide://action?prefill=Tell%20me%20more%20about%3A%20integrations)** — import attestations from GitHub, eBay, LinkedIn, StackOverflow  
- **[security](guide://action?prefill=Tell%20me%20more%20about%3A%20security)** — RSA signatures, validation, CodeQL clean  
- **[testing](guide://action?prefill=Tell%20me%20more%20about%3A%20testing)** — full FastAPI suite (28/28 passing)

## Why BitRep Exists
Online reputation is fragmented across platforms. BitRep provides a **shared reputation layer** that applications can adopt without centralizing trust or locking users into a single ecosystem.

## How It Works
- **[Identity](guide://action?prefill=Tell%20me%20more%20about%3A%20Identity):** users generate RSA keypairs; public keys act as decentralized identifiers.  
- **[Attestations](guide://action?prefill=Tell%20me%20more%20about%3A%20Attestations):** identities issue signed statements about others.  
- **[Reputation](guide://action?prefill=Tell%20me%20more%20about%3A%20Reputation):** a trust graph is built from attestations and scored via propagation.  
- **[Governance](guide://action?prefill=Tell%20me%20more%20about%3A%20Governance):** proposals use reputation‑weighted voting rather than tokens.  
- **[Privacy](guide://action?prefill=Tell%20me%20more%20about%3A%20Privacy):** users can prove they meet thresholds without revealing raw scores.

## Quick Start
- **[install dependencies](guide://action?prefill=Tell%20me%20more%20about%3A%20install%20dependencies)**  
- **[run the FastAPI server](guide://action?prefill=Tell%20me%20more%20about%3A%20run%20the%20FastAPI%20server)**  
- **[generate an identity](guide://action?prefill=Tell%20me%20more%20about%3A%20generate%20an%20identity)**  
- **[issue an attestation](guide://action?prefill=Tell%20me%20more%20about%3A%20issue%20an%20attestation)**  
- **[query reputation](guide://action?prefill=Tell%20me%20more%20about%3A%20query%20reputation)**  

## API Overview
- **[identity endpoints](guide://action?prefill=Tell%20me%20more%20about%3A%20identity%20endpoints)** — create, verify, rotate keys  
- **[attestation endpoints](guide://action?prefill=Tell%20me%20more%20about%3A%20attestation%20endpoints)** — issue, validate, list  
- **[reputation endpoints](guide://action?prefill=Tell%20me%20more%20about%3A%20reputation%20endpoints)** — compute, query, inspect trust graph  
- **[governance endpoints](guide://action?prefill=Tell%20me%20more%20about%3A%20governance%20endpoints)** — proposals, votes, tallies  

## Security Notes
- **[RSA signatures](guide://action?prefill=Tell%20me%20more%20about%3A%20RSA%20signatures)**  
- **[input validation](guide://action?prefill=Tell%20me%20more%20about%3A%20input%20validation)**  
- **[documented threat model](guide://action?prefill=Tell%20me%20more%20about%3A%20documented%20threat%20model)**  
- **[experimental ZK framework](guide://action?prefill=Tell%20me%20more%20about%3A%20experimental%20ZK%20framework)** (not production‑grade)

## Contributing
Contributions are welcome in:
- **[cryptography](guide://action?prefill=Tell%20me%20more%20about%3A%20cryptography)**  
- **[backend engineering](guide://action?prefill=Tell%20me%20more%20about%3A%20backend%20engineering)**  
- **[graph algorithms](guide://action?prefill=Tell%20me%20more%20about%3A%20graph%20algorithms)**  
- **[governance design](guide://action?prefill=Tell%20me%20more%20about%3A%20governance%20design)**  
- **[privacy systems](guide://action?prefill=Tell%20me%20more%20about%3A%20privacy%20systems)**  

Open an issue, start a discussion, or submit a PR.
