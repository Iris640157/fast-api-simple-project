# Coding Standards for PR System Test Project

Use this document when reviewing pull requests for this project.

## General

- Prefer small, focused PRs. One logical change per PR.
- Include a clear description. New code should have tests where applicable.

## Code Quality

- Follow PEP 8 for Python. Use type hints for public APIs.
- No commented-out code blocks; remove or explain in a comment.
- Prefer descriptive names; keep functions reasonably short.

## FastAPI / API

- Use Pydantic models for request/response where applicable.
- Document endpoints with summary and response_model.
- Return appropriate HTTP status codes.

## Security

- Do not log or expose secrets or API keys.
- Validate and sanitize user input.
