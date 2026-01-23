# Changelog

All notable changes to BitRep will be documented in this file.

## [0.3.0] - Initial Public Release
### Added
- identity module with RSA keypair generation
- attestation issuance and validation
- reputation scoring using modified PageRank
- governance module with quadratic voting
- FastAPI service with modular routers
- full test suite (28/28 passing)
- architecture, security, and protocol documentation

### Changed
- improved input validation across endpoints
- normalized attestation weights for Sybil resistance

### Fixed
- signature verification edge cases
- timestamp skew handling

## [0.2.0] - Pre‑Release
- added attestation storage
- added basic reputation computation
- added initial API endpoints

## [0.1.0] - Prototype
- initial project structure
- identity generation
