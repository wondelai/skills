#!/usr/bin/env python3
"""Microsoft Workspace OAuth2 setup for Hermes Agent.

Commands:
  setup.py --check                    # Is auth valid? Exit 0 = yes, 1 = no
  setup.py --client-secret /path.json # Store app credentials
  setup.py --auth-url                 # Print OAuth URL for user to visit
  setup.py --auth-code CODE           # Exchange auth code for token
  setup.py --revoke                   # Delete stored token
"""

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERMES_HOME = Path.home() / ".hermes"
TOKEN_PATH = HERMES_HOME / "microsoft_token.json"
CLIENT_SECRET_PATH = HERMES_HOME / "microsoft_client_secret.json"
PENDING_AUTH_PATH = HERMES_HOME / "microsoft_oauth_pending.json"

SCOPES = [
    "Calendars.ReadWrite",
    "Mail.ReadWrite",
    "Mail.Send",
    "User.Read",
    "Contacts.Read",
]

AUTHORITY = "https://login.microsoftonline.com/consumers"
REDIRECT_URI = "http://localhost"
REQUIRED_PACKAGES = ["msal"]


def install_deps():
    """Install MSAL if missing."""
    try:
        import msal  # noqa: F401
        return True
    except ImportError:
        pass
    import subprocess
    print("Installing MSAL...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet"] + REQUIRED_PACKAGES,
            stdout=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        print(f"Try manually: {sys.executable} -m pip install {' '.join(REQUIRED_PACKAGES)}")
        return False


def _ensure_deps():
    if not install_deps():
        sys.exit(1)


def _load_client_secret() -> dict:
    if not CLIENT_SECRET_PATH.exists():
        print(f"ERROR: No client secret at {CLIENT_SECRET_PATH}")
        sys.exit(1)
    return json.loads(CLIENT_SECRET_PATH.read_text())


def check_auth():
    """Check if stored token is valid."""
    if not TOKEN_PATH.exists():
        print(f"NOT_AUTHENTICATED: No token at {TOKEN_PATH}")
        return False

    _ensure_deps()
    import msal

    config = _load_client_secret()
    app = msal.PublicClientApplication(
        config["client_id"],
        authority=AUTHORITY,
    )

    token = json.loads(TOKEN_PATH.read_text())
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            TOKEN_PATH.write_text(json.dumps(result, indent=2))
            print(f"AUTHENTICATED: Token valid at {TOKEN_PATH}")
            return True

    # Try refreshing directly
    if "refresh_token" in token:
        result = app.acquire_token_by_refresh_token(
            token["refresh_token"], scopes=SCOPES
        )
        if result and "access_token" in result:
            TOKEN_PATH.write_text(json.dumps(result, indent=2))
            print(f"AUTHENTICATED: Token refreshed at {TOKEN_PATH}")
            return True
        print(f"REFRESH_FAILED: {result.get('error_description', 'Unknown error')}")
        return False

    print("TOKEN_INVALID: Re-run setup.")
    return False


def get_auth_url():
    """Print the OAuth authorization URL."""
    _ensure_deps()
    import msal

    config = _load_client_secret()
    app = msal.ConfidentialClientApplication(
        config["client_id"],
        authority=AUTHORITY,
        client_credential=config["client_secret"],
    )

    auth_url = app.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    # Save pending state
    PENDING_AUTH_PATH.write_text(json.dumps({
        "redirect_uri": REDIRECT_URI,
        "scopes": SCOPES,
    }, indent=2))

    print(auth_url)


def exchange_auth_code(code_or_url: str):
    """Exchange authorization code for token."""
    _ensure_deps()
    import msal

    config = _load_client_secret()
    app = msal.PublicClientApplication(
        config["client_id"],
        authority=AUTHORITY,
    )

    # Extract code from URL if needed
    code = code_or_url
    if code_or_url.startswith("http"):
        parsed = urlparse(code_or_url)
        params = parse_qs(parsed.query)
        if "code" in params:
            code = params["code"][0]
        elif "error" in params:
            print(f"ERROR: {params['error'][0]}: {params.get('error_description', [''])[0]}")
            sys.exit(1)

    result = app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    if "access_token" in result:
        TOKEN_PATH.write_text(json.dumps(result, indent=2))
        PENDING_AUTH_PATH.unlink(missing_ok=True)
        print(f"OK: Authenticated. Token saved to {TOKEN_PATH}")
    else:
        print(f"ERROR: {result.get('error', 'Unknown')}: {result.get('error_description', '')}")
        sys.exit(1)


def revoke():
    """Delete stored token."""
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
        print(f"Deleted {TOKEN_PATH}")
    else:
        print("No token to delete.")
    PENDING_AUTH_PATH.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Microsoft Workspace OAuth setup")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--client-secret", metavar="PATH")
    group.add_argument("--auth-url", action="store_true")
    group.add_argument("--auth-code", metavar="CODE")
    group.add_argument("--revoke", action="store_true")
    args = parser.parse_args()

    if args.check:
        sys.exit(0 if check_auth() else 1)
    elif args.client_secret:
        src = Path(args.client_secret).expanduser().resolve()
        data = json.loads(src.read_text())
        CLIENT_SECRET_PATH.write_text(json.dumps(data, indent=2))
        print(f"OK: Client secret saved to {CLIENT_SECRET_PATH}")
    elif args.auth_url:
        get_auth_url()
    elif args.auth_code:
        exchange_auth_code(args.auth_code)
    elif args.revoke:
        revoke()


if __name__ == "__main__":
    main()
