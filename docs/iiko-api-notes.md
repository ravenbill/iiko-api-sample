# iiko API Notes

## Cloud API basics

- Base URL in current project: `https://api-ry.iiko.services/api/1`
- Authentication starts by requesting an access token
- The token request uses the `apiLogin` field

## What `apiLogin` is

`apiLogin` is the integration login for a specific iiko client account. It is not the same thing as a normal end-user password.

The iiko auth docs surfaced through research describe `apiLogin` as:

> API login. It is set in iikoWeb.

That means our app should store one `apiLogin` per client and use it to get an access token before calling other Cloud API endpoints.

## Where to get `apiLogin`

The iiko help pages indicate that Cloud API settings are managed from iiko's back office / iikoWeb.

Observed setup path:

`Обмен данными -> Настройка iikoTransport`

From there, iiko opens the Cloud API settings page in iikoWeb.

Practical implication:

- the client must have iikoWeb access
- someone with sufficient rights needs to open the Cloud API settings
- the `apiLogin` value for that client is configured or retrieved there

If the restaurant account does not expose those settings, the client may need help from their iiko admin, dealer, or integrator.

## How we plan to model this locally

We keep one named client entry per iiko customer in `.env`.

Example:

```dotenv
IIKO_CLIENTS=client_one,client_two

IIKO_CLIENT_CLIENT_ONE_NAME=Client One
IIKO_CLIENT_CLIENT_ONE_API_LOGIN=replace-with-client-one-login

IIKO_CLIENT_CLIENT_TWO_NAME=Client Two
IIKO_CLIENT_CLIENT_TWO_API_LOGIN=replace-with-client-two-login
```

This lets future commands target:

- one client: `--client client_one`
- multiple clients: `--clients client_one,client_two`

## Open questions

- confirm the exact token endpoint request body against live docs before implementing auth code
- confirm whether any clients require region-specific base URLs
- confirm who on the customer side has permission to view or generate the API login

## Reference links

- `https://api-ry.iiko.services`
- `https://ru.iiko.help/smart/project-iikoweb/iikocloudapi`
- `https://ru.iiko.help/articles/api-documentations/kak-podklyuchit-vneshniy-api`
- `https://api.iiko.ru/`
