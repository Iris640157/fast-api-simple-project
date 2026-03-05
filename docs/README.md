# PR System Test Project

This is a minimal FastAPI project used to test integration with the central PR review service.

## How review works

When you open or update a pull request, a GitHub Action calls the deployed PR review service with the PR diff. The service runs a RAG-based review against this repo's guidelines and posts the result as a comment on the PR.

## Setup

1. Deploy the PR automation system (or use a shared instance).
2. Add the repository's `guidelines/` and `docs/` to the service's knowledge base for this project (using the service's build-from-repo script with your repo and `project_id` = `owner/repo`).
3. In this repo's GitHub Settings → Secrets, add `REVIEW_SERVICE_URL` with the base URL of the review service (e.g. `https://pr-review.example.com`).
4. Open a PR; the workflow will call the service and post the review comment.
