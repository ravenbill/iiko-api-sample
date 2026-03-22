# iiko CLI Tools Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable Python foundation for iiko-backed CLI tools, then ship two first-class tools: create guest and check balance by track number.

**Architecture:** The project will grow around a shared library that owns configuration loading, client selection, authentication, HTTP transport, error handling, and common domain helpers. Each user-facing tool will be a thin CLI command that delegates to shared library modules, gets its own unit tests, and gets its own skill document describing how the tool works and how we developed it. The design should make later MCP publication straightforward by reusing the same service layer instead of duplicating logic inside the future server.

**Tech Stack:** Python 3.11+, `httpx`, `python-dotenv`, `pytest`, console scripts from `pyproject.toml`

---

## Planned file structure

**Create:**
- `docs/plans/2026-03-22-iiko-cli-tools-foundation.md`
- `skills/create-guest/SKILL.md`
- `skills/check-balance/SKILL.md`
- `src/iiko_api_sample/shared/__init__.py`
- `src/iiko_api_sample/shared/accounts.py`
- `src/iiko_api_sample/shared/auth.py`
- `src/iiko_api_sample/shared/errors.py`
- `src/iiko_api_sample/shared/http.py`
- `src/iiko_api_sample/commands/__init__.py`
- `src/iiko_api_sample/commands/create_guest.py`
- `src/iiko_api_sample/commands/check_balance.py`
- `tests/shared/test_accounts.py`
- `tests/shared/test_auth.py`
- `tests/commands/test_create_guest.py`
- `tests/commands/test_check_balance.py`

**Modify:**
- `pyproject.toml`
- `README.md`
- `src/iiko_api_sample/config.py`
- `src/iiko_api_sample/main.py`
- `src/iiko_api_sample/client.py`
- `src/iiko_api_sample/__init__.py`
- `docs/iiko-api-notes.md`
- `.env.example`

## Scope and assumptions

- Each new script is treated as a feature.
- The first implementation target is CLI tooling, not MCP transport.
- The future MCP server should call shared services directly instead of shelling out to CLI commands.
- Guest existence must be checked before create, but the exact uniqueness rule is still an open API-level question. The plan assumes we will confirm whether iiko expects lookup by phone, card, or another guest identifier before finalizing the create-guest flow.
- The balance tool depends on the exact track-number endpoint and payload shape, which must be confirmed against the live docs before code is written.
- Any user-facing strings should be ready for Russian and English.

## Test plan

- Unit-test account selection and validation for single and multiple client names.
- Unit-test auth token acquisition and error mapping using stubbed HTTP responses.
- Unit-test create-guest flow for:
  - existing guest found
  - guest not found and created successfully
  - invalid input
  - upstream API error
- Unit-test check-balance flow for:
  - valid track number with returned balance
  - unknown track number
  - malformed track number
  - upstream API error
- Unit-test CLI argument parsing for one-client and multi-client modes where relevant.
- Keep tests isolated from live iiko services by faking HTTP at the transport boundary.
- Run targeted tests while implementing each task, then run the full suite before declaring the feature complete.

### Task 1: Establish project conventions inside the repo

**Files:**
- Create: `AGENTS.md`, `prompts.md`
- Modify: `README.md`

- [ ] **Step 1: Verify the project-local instruction files are present**

Run: `ls AGENTS.md prompts.md`
Expected: both files exist in the repo root

- [ ] **Step 2: Document that this repo is now the working directory for the project**

Add a short note to `README.md` if needed so future work happens inside this repo rather than the parent workspace.

- [ ] **Step 3: Re-read the repo instructions before implementing later tasks**

Expected: future steps follow `docs/plans`, unit test, i18n, and review-pass requirements.

### Task 2: Refactor shared configuration and client selection

**Files:**
- Create: `src/iiko_api_sample/shared/__init__.py`, `src/iiko_api_sample/shared/accounts.py`, `tests/shared/test_accounts.py`
- Modify: `src/iiko_api_sample/config.py`, `.env.example`, `src/iiko_api_sample/__init__.py`

- [ ] **Step 1: Write the failing tests for account loading**

```python
def test_get_account_by_name_returns_named_client_settings():
    ...

def test_get_accounts_rejects_unknown_client_name():
    ...
```

- [ ] **Step 2: Run the targeted tests to verify they fail**

Run: `python3 -m pytest tests/shared/test_accounts.py -v`
Expected: FAIL because the account-loading helpers do not exist yet

- [ ] **Step 3: Implement minimal account parsing and validation**

Build helpers that:
- read `IIKO_CLIENTS`
- normalize client slugs
- return one or more account records with `name`, `api_login`, and resolved base URL

- [ ] **Step 4: Re-run the targeted tests to verify they pass**

Run: `python3 -m pytest tests/shared/test_accounts.py -v`
Expected: PASS

- [ ] **Step 5: Commit the account-selection slice**

```bash
git add .env.example src/iiko_api_sample/config.py src/iiko_api_sample/shared/__init__.py src/iiko_api_sample/shared/accounts.py tests/shared/test_accounts.py src/iiko_api_sample/__init__.py
git commit -m "feat: add client account loading"
```

### Task 3: Build the shared auth and HTTP layer

**Files:**
- Create: `src/iiko_api_sample/shared/auth.py`, `src/iiko_api_sample/shared/errors.py`, `src/iiko_api_sample/shared/http.py`, `tests/shared/test_auth.py`
- Modify: `src/iiko_api_sample/client.py`, `docs/iiko-api-notes.md`

- [ ] **Step 1: Write the failing tests for token acquisition and API error handling**

```python
def test_get_access_token_posts_api_login():
    ...

def test_get_access_token_maps_iiko_error_response():
    ...
```

- [ ] **Step 2: Run the targeted tests to verify they fail**

Run: `python3 -m pytest tests/shared/test_auth.py -v`
Expected: FAIL because the auth layer does not exist yet

- [ ] **Step 3: Implement minimal shared auth and transport helpers**

Required behavior:
- build the access-token request from a selected client account
- isolate `httpx` calls behind a small shared transport
- centralize API error parsing so CLI commands do not duplicate it

- [ ] **Step 4: Re-run the targeted tests**

Run: `python3 -m pytest tests/shared/test_auth.py -v`
Expected: PASS

- [ ] **Step 5: Commit the auth slice**

```bash
git add src/iiko_api_sample/client.py src/iiko_api_sample/shared/auth.py src/iiko_api_sample/shared/errors.py src/iiko_api_sample/shared/http.py tests/shared/test_auth.py docs/iiko-api-notes.md
git commit -m "feat: add shared iiko auth layer"
```

### Task 4: Add the create-guest command and its skill

**Files:**
- Create: `src/iiko_api_sample/commands/__init__.py`, `src/iiko_api_sample/commands/create_guest.py`, `tests/commands/test_create_guest.py`, `skills/create-guest/SKILL.md`
- Modify: `pyproject.toml`, `README.md`, `src/iiko_api_sample/main.py`

- [ ] **Step 1: Write the failing tests for guest lookup and conditional create**

```python
def test_create_guest_returns_existing_guest_when_match_found():
    ...

def test_create_guest_creates_guest_when_no_match_exists():
    ...
```

- [ ] **Step 2: Run the targeted tests to verify they fail**

Run: `python3 -m pytest tests/commands/test_create_guest.py -v`
Expected: FAIL because the command module does not exist yet

- [ ] **Step 3: Implement the minimal create-guest command**

Required behavior:
- accept a client slug
- accept guest input fields
- check whether the guest already exists using the agreed lookup key
- create the guest only when the lookup returns no match
- return a structured result suitable for both CLI output and future MCP tool output

- [ ] **Step 4: Add the console entry point**

Expose a command such as `iiko-create-guest` in `pyproject.toml`.

- [ ] **Step 5: Write the skill for this tool**

`skills/create-guest/SKILL.md` should explain:
- what the tool does
- required inputs
- the existence-check rule
- typical debugging flow
- which shared library pieces it uses

- [ ] **Step 6: Re-run the targeted tests**

Run: `python3 -m pytest tests/commands/test_create_guest.py -v`
Expected: PASS

- [ ] **Step 7: Commit the create-guest feature**

```bash
git add pyproject.toml README.md src/iiko_api_sample/main.py src/iiko_api_sample/commands/__init__.py src/iiko_api_sample/commands/create_guest.py tests/commands/test_create_guest.py skills/create-guest/SKILL.md
git commit -m "feat: add create guest command"
```

### Task 5: Add the check-balance-by-track-number command and its skill

**Files:**
- Create: `src/iiko_api_sample/commands/check_balance.py`, `tests/commands/test_check_balance.py`, `skills/check-balance/SKILL.md`
- Modify: `pyproject.toml`, `README.md`, `src/iiko_api_sample/main.py`

- [ ] **Step 1: Write the failing tests for balance lookup**

```python
def test_check_balance_returns_balance_for_track_number():
    ...

def test_check_balance_returns_not_found_for_unknown_track():
    ...
```

- [ ] **Step 2: Run the targeted tests to verify they fail**

Run: `python3 -m pytest tests/commands/test_check_balance.py -v`
Expected: FAIL because the command module does not exist yet

- [ ] **Step 3: Implement the minimal balance command**

Required behavior:
- accept a client slug
- accept a track number
- call the correct iiko endpoint through the shared auth/transport layer
- return a structured result that can later map cleanly into an MCP tool result

- [ ] **Step 4: Add the console entry point**

Expose a command such as `iiko-check-balance` in `pyproject.toml`.

- [ ] **Step 5: Write the skill for this tool**

`skills/check-balance/SKILL.md` should explain:
- what the tool does
- expected inputs
- common failure modes
- how we validated the request and response flow

- [ ] **Step 6: Re-run the targeted tests**

Run: `python3 -m pytest tests/commands/test_check_balance.py -v`
Expected: PASS

- [ ] **Step 7: Commit the balance feature**

```bash
git add pyproject.toml README.md src/iiko_api_sample/main.py src/iiko_api_sample/commands/check_balance.py tests/commands/test_check_balance.py skills/check-balance/SKILL.md
git commit -m "feat: add balance lookup command"
```

### Task 6: Verify the combined toolchain

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add usage examples for both commands**

Document example invocations using named clients.

- [ ] **Step 2: Run the full test suite**

Run: `python3 -m pytest -v`
Expected: all shared and command tests pass

- [ ] **Step 3: Run a lightweight import/CLI smoke check**

Run:
```bash
PYTHONPATH=src python3 -m iiko_api_sample.main
```
Expected: the CLI entry module imports cleanly

- [ ] **Step 4: Commit the verification/docs slice if needed**

```bash
git add README.md
git commit -m "docs: add CLI usage examples"
```

## Final review pass

This section must be completed after implementation, not before.

### Code and test review checklist

- [ ] Confirm each command is thin and delegates business logic into shared modules.
- [ ] Confirm no auth, account parsing, or HTTP error handling is duplicated between commands.
- [ ] Confirm unit tests focus on behavior, not mocks for their own sake.
- [ ] Confirm both tools are safe to reuse from a future MCP server without shelling out.
- [ ] Confirm CLI outputs are understandable and ready for Russian and English localization.
- [ ] Confirm the test plan was actually executed and not only written.
- [ ] Confirm open API assumptions were resolved and reflected in docs.

### Review notes

Fill this section at the end of implementation with:
- what is strong in the code
- what is weak or still risky
- test coverage gaps
- readability concerns
- reliability concerns
- recommended cleanup before adding more tools

## Open questions to resolve before coding

- What field defines guest uniqueness for the create-guest tool?
- Which exact iiko endpoint and payload should be used for track-number balance lookup?
- Should the first CLI output format be human-readable text, JSON, or both?
- Do we want one command per tool or a grouped CLI such as `iiko-tool create-guest`?
