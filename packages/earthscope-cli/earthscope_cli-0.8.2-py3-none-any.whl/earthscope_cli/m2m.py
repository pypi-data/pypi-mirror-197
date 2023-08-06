import json
import typer

from os import environ
from rich import print

from earthscope_cli.util import APP_DIR, AUTH0_AUDIENCE, AUTH0_DOMAIN, ES_CLI_PREFIX
from earthscope_sdk.auth.auth_flow import (
    NoTokensError,
    UnauthorizedError,
    ValidTokens,
)
from earthscope_sdk.auth.client_credentials_flow import (
    ClientCredentialsFlowError,
    ClientCredentialsFlowSimple
)

app = typer.Typer()

AUTH_TOKENS_PATH = APP_DIR / "m2m_tokens.json"
AUTH_CREDS_PATH = APP_DIR / "m2m_credentials.json"

M2M_CLIENT_ID_CONFIG = f"{ES_CLI_PREFIX}_M2M_CLIENT_ID"
M2M_CLIENT_SECRET_CONFIG = f"{ES_CLI_PREFIX}_M2M_CLIENT_SECRET"
M2M_CLIENT_ID = environ.get(M2M_CLIENT_ID_CONFIG)
M2M_CLIENT_SECRET = environ.get(M2M_CLIENT_SECRET_CONFIG)


class CliClientCredentialsFlow(ClientCredentialsFlowSimple):
    @classmethod
    def get(cls,
            client_id: str = M2M_CLIENT_ID,
            client_secret: str = M2M_CLIENT_SECRET,
            audience: str = AUTH0_AUDIENCE,
            domain: str = AUTH0_DOMAIN,
            path: str = AUTH_TOKENS_PATH

            ):
        if not M2M_CLIENT_ID or not M2M_CLIENT_SECRET:
            print("[red]Missing required environment variables for M2M authentication:")
            print(f"[red]{M2M_CLIENT_ID_CONFIG}=")
            print(f"[red]{M2M_CLIENT_SECRET_CONFIG}=")
            raise typer.Exit(1)

        instance = cls(
            audience=audience,
            client_id=client_id,
            client_secret=client_secret,
            domain=domain,
            path=path,
        )

        return instance


@app.command(help="Login to Earthscope API with machine-to-machine (m2m) credentials")
def login(
    token: bool = typer.Option(
        False, help="Return only the token after successful login"
    )
):
    m2m_flow = CliClientCredentialsFlow.get()
    try:
        m2m_flow.request_tokens()
    except UnauthorizedError:
        print("[red]Unauthorized. Verify client ID and secret")
        raise typer.Exit(1)
    except ClientCredentialsFlowError:
        print("[red]Failed to get device code")
        raise typer.Exit(1)
    except Exception as e:
        print(f"[red]Device flow failed for unknown reason: {e}")
        raise typer.Exit(1)

    if token:
        m2m_flow.load_tokens()
        typer.echo(m2m_flow.access_token)
    else:
        print(f"[green]Successful login! Access token expires at {m2m_flow.expires_at}")


@app.command(help="Clear your local m2m tokens")
def logout():
    try:
        AUTH_TOKENS_PATH.unlink()
    except FileNotFoundError:
        print("Not logged in")
    else:
        print("[green]Logged out")


@app.command(help="Print all m2m state information stored locally on this machine")
def state(
    only_path: bool = typer.Option(
        False,
        "--path",
        "-p",
        help="Print the full path to where the state is stored on this machine",
    )
):
    if only_path:
        typer.echo(AUTH_TOKENS_PATH)
        raise typer.Exit(0)
    m2m_flow = CliClientCredentialsFlow.get()
    m2m_flow.load_tokens()
    print(vars(m2m_flow.tokens))


@app.command(help="Print the access token body (or token)")
def access(
    token: bool = typer.Option(
        False,
        "--token",
        "-t",
        help="Get access token",
    )
):
    m2m_flow = CliClientCredentialsFlow.get()
    try:
        m2m_flow.load_tokens()
        if token:
            typer.echo(m2m_flow.access_token)
        else:
            print(m2m_flow.access_token_body)
    except NoTokensError:
        print("[red]No access token present")
        raise typer.Exit(1)


@app.command(help="Print the date & time at which the access token was issued")
def issued():
    m2m_flow = CliClientCredentialsFlow.get()
    m2m_flow.load_tokens()
    print(m2m_flow.issued_at)


@app.command(help="Print the date & time at which the access token expires")
def expires():
    m2m_flow = CliClientCredentialsFlow.get()
    m2m_flow.load_tokens()
    print(m2m_flow.expires_at)


@app.command(help="Print the access token's scope")
def scope():
    m2m_flow = CliClientCredentialsFlow.get()
    m2m_flow.load_tokens()
    print(m2m_flow.tokens.scope.split())


@app.command(help="Print the access token's time-to-live (TTL)")
def ttl():
    m2m_flow = CliClientCredentialsFlow.get()
    m2m_flow.load_tokens()
    if m2m_flow.ttl.total_seconds() > 0:
        print(m2m_flow.ttl)
        return

    print("[red]The access token is expired")
    raise typer.Exit(1)


if __name__ == "__main__":
    expires()
