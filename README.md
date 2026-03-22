# iiko-api-sample

Sample Python project for exploring the iiko API.

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
