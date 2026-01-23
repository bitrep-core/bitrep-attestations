# Developer Setup

This guide describes how to set up a local development environment for BitRep.  
The project uses FastAPI, Python 3.10+, and a modular service layout.

## Requirements
- Python 3.10 or newer
- pip or uv
- Git
- OpenSSL (for key generation tests)
- Optional: Docker (for containerized runs)

## Clone the Repository
git clone https://github.com/bitrep-core/bitrep-attestations.git
cd bitrep-attestations

## Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate
# Windows:
# venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt
# or, if using uv:
# uv pip install -r requirements.txt

## Run the FastAPI Server
uvicorn app.main:app --reload

The API will be available at:
http://localhost:8000

Interactive docs:
http://localhost:8000/docs

## Run Tests
pytest -q

All tests should pass (28/28).

## Code Quality Tools
- ruff for linting
- mypy for type checking
- CodeQL for security scanning

Run lint:
ruff check .

Run type checks:
mypy app/

## Environment Variables
Create a `.env` file if needed:

BITREP_ENV=development
BITREP_LOG_LEVEL=info

## Project Structure
app/
  identity/        # key generation, verification
  attestations/    # signed statements, validation
  reputation/      # graph scoring, propagation
  governance/      # proposals, voting
  privacy/         # ZK framework (experimental)
  api/             # FastAPI routers
  core/            # shared utilities
tests/
  ...              # full test suite

## Optional: Docker
docker build -t bitrep .
docker run -p 8000:8000 bitrep

## Making Changes
- keep commits small
- include tests for new functionality
- follow FastAPI conventions
- avoid adding unnecessary dependencies

This setup provides a complete environment for developing, testing, and extending BitRep.
