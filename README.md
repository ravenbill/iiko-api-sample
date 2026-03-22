# iiko-api-sample

Sample Python project for exploring the iiko API.

## Environment configuration

Use named client slugs in `.env` so future commands can target one client or a list of clients.

Example:

```dotenv
IIKO_BASE_URL=https://api-ry.iiko.services/api/1
IIKO_TIMEOUT_SECONDS=10

IIKO_CLIENTS=client_one,client_two

IIKO_CLIENT_CLIENT_ONE_NAME=Client One
IIKO_CLIENT_CLIENT_ONE_API_LOGIN=replace-with-client-one-login

IIKO_CLIENT_CLIENT_TWO_NAME=Client Two
IIKO_CLIENT_CLIENT_TWO_API_LOGIN=replace-with-client-two-login
```

Rules:

- `IIKO_CLIENTS` contains the allowed client slugs as a comma-separated list
- each slug should be lowercase with underscores, for example `client_one`
- each client gets a display name and an API login
- future commands should accept either one slug or a comma-separated list of slugs

Planned command usage:

- one client: `--client client_one`
- several clients: `--clients client_one,client_two`

## Project layout

- `src/iiko_api_sample/` - application package
- `tests/` - lightweight test coverage
- `docs/` - notes and future API findings
- `scripts/` - helper scripts
- `mcp_server/` - reserved for a future MCP server

## Current status

This is a starter scaffold. The live iiko docs at `https://api-ry.iiko.services` were not fetched in this session because `parallel-cli` is not installed yet.

To enable URL extraction later, run `/parallel-setup` and then retry the docs request.

## Next steps

1. Create a real auth flow once we confirm the iiko login/token endpoints.
2. Add one working API example call.
3. Decide whether the future MCP server should live in this repo or a separate one.
