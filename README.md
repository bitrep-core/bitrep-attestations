# BitRep Attestations

A peer-to-peer reputation system based on behavioral attestations with cryptographic signatures, weighted reputation propagation, governance mechanisms, and privacy features.

## Overview

BitRep is a decentralized reputation system that allows users to attest to each other's behavior directly without requiring a central authority. The system uses cryptographic signatures, weighted reputation calculations (modified PageRank), and privacy-preserving zero-knowledge proofs.

## Features

### 1. **Attestation System**
- Create behavioral attestations between users
- Cryptographic signatures for authenticity
- Mutual validation support
- Weighted attestations based on attester reputation

### 2. **Weighted Reputation**
- Modified PageRank algorithm for reputation calculation
- High-reputation attesters have more influence
- Sybil resistance through isolated cluster detection
- Time decay for recent behavior emphasis

### 3. **Identity Verification**
- Self-sovereign cryptographic identities
- RSA 2048-bit key pair generation
- Persistent identity verification
- Public/private key management

### 4. **Governance**
- Reputation-weighted voting system
- Quadratic scaling to prevent plutocratic capture
- Proposal creation and management
- Democratic decision-making based on demonstrated trustworthiness

### 5. **Privacy Features**
- Zero-knowledge proofs for reputation thresholds
- Selective attestation disclosure
- Reputation bands for privacy preservation
- Merkle proofs for selective disclosure

### 6. **Third-Party Integration**
- Import attestations from external platforms
- Support for GitHub, eBay, LinkedIn, Stack Overflow
- Validation layer for platform attestations
- User-controlled reputation bootstrapping

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies (for testing)
pip install -r requirements-dev.txt
```

### Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

Interactive API documentation: http://localhost:8000/docs

### Running Tests

```bash
pytest tests/ -v
```

## API Endpoints

### Attestations
- `POST /attest` - Create a new attestation

### User Reputation
- `GET /user/{username}` - Get user reputation and attestations

### Identity Management
- `POST /identity/create` - Create new identity with key pair
- `GET /identity/{username}` - Get identity information
- `POST /identity/{username}/verify` - Verify identity

### Governance
- `POST /governance/proposal` - Create governance proposal
- `GET /governance/proposals` - List proposals
- `POST /governance/vote` - Cast weighted vote
- `POST /governance/proposal/{id}/finalize` - Finalize proposal

### Privacy
- `POST /privacy/prove-threshold` - Generate ZK proof for reputation threshold
- `POST /privacy/verify-threshold` - Verify ZK proof
- `GET /privacy/reputation-bands/{username}` - Get reputation band
- `POST /privacy/selective-disclosure` - Create selective disclosure proof

### Integration
- `GET /integration/platforms` - List supported platforms
- `POST /integration/import` - Import third-party attestation
- `POST /integration/verify/{id}` - Verify third-party attestation
- `POST /integration/github/import` - Import GitHub profile

## Architecture

### Technology Stack
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM and database management
- **SQLite** - Database (easily replaceable with PostgreSQL)
- **Cryptography** - RSA signatures and key management
- **Pydantic** - Data validation

### Key Components

#### Models
- `AttestationModel` - Behavioral attestations with signatures
- `UserIdentityModel` - User identities with cryptographic keys
- `GovernanceProposalModel` - Governance proposals
- `VoteModel` - Reputation-weighted votes
- `ThirdPartyAttestationModel` - External platform attestations

#### Utilities
- `crypto.py` - Key generation, signing, verification
- `reputation.py` - Modified PageRank algorithm
- `zkproof.py` - Zero-knowledge proofs

#### API Routers
- `attestations.py` - Attestation endpoints
- `users.py` - User reputation endpoints
- `identity.py` - Identity management
- `governance.py` - Governance and voting
- `privacy.py` - Privacy features
- `integration.py` - Third-party integrations

## Reputation Algorithm

BitRep uses a modified PageRank algorithm with the following features:

1. **Weighted Propagation**: Attestations from high-reputation users carry more weight
2. **Sybil Resistance**: Isolated clusters of mutual attestation are discounted
3. **Time Decay**: Recent attestations matter more (365-day half-life)
4. **Damping Factor**: 0.85 damping for reputation propagation

### Weight Calculation
```python
weight = log2(1 + attester_reputation) * cluster_discount
```

### Time Decay
```python
decay = exp(-age_days * ln(2) / 365)
```

## Security

### Cryptographic Signatures
- RSA 2048-bit keys
- PSS padding with SHA-256
- Signature verification for all attestations

### Privacy
- Zero-knowledge proofs for threshold verification
- Selective disclosure with Merkle proofs
- Reputation bands instead of exact scores

### Identity
- Self-sovereign identity model
- Private keys never stored on server
- Multi-channel verification support

## Testing

The project includes comprehensive tests:

- **Cryptographic utilities**: Key generation, signing, verification
- **Reputation algorithms**: PageRank, weighting, Sybil detection, time decay
- **Zero-knowledge proofs**: Threshold proofs, selective disclosure
- **API endpoints**: Integration tests for all major endpoints

Run tests with:
```bash
pytest tests/ -v --cov=.
```

## Documentation

- [API Documentation](API_DOCUMENTATION.md) - Detailed API reference
- [BitRep Whitepaper](BitRep_Whitepaper.md) - Theoretical foundation

## Roadmap

### Completed ✅
- Attestation system with cryptographic signatures
- Weighted reputation calculation (PageRank)
- Identity management with key pairs
- Governance and voting
- Privacy features (ZK proofs)
- Third-party integration framework
- Comprehensive test suite

### Future Enhancements
- Blockchain integration for immutability
- Advanced ZK-SNARK implementations
- Real-time reputation updates
- Mobile SDK
- Decentralized storage (IPFS)
- Cross-chain reputation bridges

## Contributing

Contributions are welcome! Please ensure:
1. All tests pass
2. New features include tests
3. Code follows existing style
4. Security best practices are maintained

## License

See [LICENSE](LICENSE) file for details.

## Citation

If you use BitRep in research, please cite:
```
BitRep: A Peer-to-Peer Reputation System
Based on cryptographic attestations and weighted reputation propagation
```

## Contact

For questions or support, please open an issue on GitHub.
