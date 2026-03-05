# PR System Test Project

Minimal FastAPI project used to test the **central PR review service**. Everything runs on **pr_automation_system**; this repo only triggers it from CI.

## Flow: everything on pr_automation_system

From CI you only pass **`repo_id`** and **`pr_number`**. The service then:

1. **Fetches the PR** from GitHub (diff, title, description) using `GITHUB_TOKEN`.
2. **Ensures the KB exists** for this repo (builds it from `guidelines/` and `docs/` on first use).
3. **Runs the RAG review** and **posts the comment** on the PR.

No scripts, no diff generation, and no `call_review_service.py` in this repo. One workflow step that calls the service.

---

## Workflow (this repo)

The workflow in `.github/workflows/call-pr-review-service.yml` does a single step:

- **POST** to `REVIEW_SERVICE_URL/review` with body: `{"repo_id": "owner/repo", "pr_number": 123}`.

That’s it. The service does the rest.

---

## Setup

1. **Deploy pr_automation_system** with:
   - `OPENAI_API_KEY` (or use Ollama)
   - `GITHUB_TOKEN` (to fetch PRs and post comments)
   - Persistent storage for Chroma (`CHROMA_PERSIST_DIR`)

2. **In this repo:** add secret **`REVIEW_SERVICE_URL`** = your service base URL.

3. **Open a PR** – the workflow runs and the service posts the review comment.

You do **not** need to call `/admin/build-kb` first: the service builds the KB for this repo on first use (`ensure_kb: true`). You can still pre-build via `POST /admin/build-kb` if you prefer.

---

## Optional: request review locally (with diff)

If you want to run a review locally and send the diff yourself:

```bash
export REVIEW_SERVICE_URL=https://YOUR-SERVICE-URL
export REPO_ID=YOUR_ORG/pr_system_test_project
git diff main --no-color > pr.diff
python scripts/request_review.py pr.diff
```

---

## Guidelines

Put project-specific review guidelines in **`guidelines/`** and extra docs in **`docs/`**. The service indexes them when it builds the KB (on first PR or via `/admin/build-kb`).
# fast-api-simple-project
