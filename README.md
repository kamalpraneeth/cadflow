# CADFlow

![CI Status](https://github.com/kamal/CADFlow/actions/workflows/ci.yml/badge.svg)

CADFlow is an enterprise-grade, microservices-based CAD Governance & CI/CD Automation Platform. It automates CAD file validation, conversion, metadata extraction, anomaly detection, and provides AI-powered code (CAD) review comments on GitHub Pull Requests.

## Features & Technologies

- **Microservices Architecture**: 4 independent Python FastAPI services handling validation, conversion, metadata storage, and AI analysis.
- **Orchestration**: Redis and Celery power an event-driven task pipeline reacting to GitHub webhooks.
- **AI & ML Integration**: Anthropic Claude for natural language summaries of CAD diffs, and scikit-learn Isolation Forest for detecting anomalous engineering changes.
- **Governance**: Immutable audit log of all CAD changes, backed by PostgreSQL.
- **Infrastructure**: Fully containerized with Docker and docker-compose.
- **CI/CD Automation**: GitHub Actions workflows for testing, linting, building, and automated PR review comments.

## Setup & Running Locally

1. Create a `.env` file with your `ANTHROPIC_API_KEY` (and optionally `GITHUB_TOKEN`).
2. Run `bash scripts/setup.sh` to initialize the environment and generate mock CAD fixtures.
3. Run `bash scripts/run_all.sh` to spin up the entire stack via Docker Compose.
4. Access the dashboard at `http://localhost:8000`.

## Architecture

See [docs/architecture.md](docs/architecture.md) for a detailed breakdown of the microservices and event flow.

## Job Description Mapping

This project demonstrates the following core skills:
- **Git Fundamentals & GitHub Workflow**: Branch protection, PR templates, and webhook-driven review automation.
- **Python / Bash Scripting**: Microservices in Python, setup/orchestration via Bash.
- **AI Tool Integration**: Direct integration with the Anthropic API for summarization and RAG.
- **Linux/Unix & Infrastructure**: Containerized workloads running cleanly on Ubuntu-based runners, docker-compose orchestration.
- **CAD Infrastructure Exposure**: Manipulation and validation of DXF files using `ezdxf`.
