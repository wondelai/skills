#!/bin/bash
# Safe email sender - previews before sending to prevent mangled/duplicate emails
# Usage:
#   safe_mail_send.sh --to "user@example.com" --subject "Subject" --body-file /tmp/body.txt
#   safe_mail_send.sh --to "user@example.com" --subject "Subject" --body-file /tmp/body.txt --confirm
#   safe_mail_send.sh --to "user@example.com" --subject "Subject" --body-file /tmp/body.txt --attachment /path/to/file.png --confirm

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GAPI="python3 $SCRIPT_DIR/microsoft_api.py"
TO=""
SUBJECT=""
BODY_FILE=""
ATTACHMENT=""
CONFIRM=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --to) TO="$2"; shift 2 ;;
        --subject) SUBJECT="$2"; shift 2 ;;
        --body-file) BODY_FILE="$2"; shift 2 ;;
        --attachment) ATTACHMENT="$2"; shift 2 ;;
        --confirm) CONFIRM=true; shift ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

if [[ -z "$TO" || -z "$SUBJECT" || -z "$BODY_FILE" ]]; then
    echo "Usage: $0 --to EMAIL --subject SUBJECT --body-file PATH [--attachment FILE] [--confirm]"
    echo ""
    echo "  --to          Recipient email address"
    echo "  --subject     Email subject line"
    echo "  --body-file   Path to file containing email body"
    echo "  --attachment  Optional file to attach (max 3MB)"
    echo "  --confirm     Send without prompting (default: preview only)"
    exit 1
fi

if [[ ! -f "$BODY_FILE" ]]; then
    echo "ERROR: Body file not found: $BODY_FILE"
    exit 1
fi

BODY=$(cat "$BODY_FILE")

echo "=========================================="
echo "EMAIL PREVIEW"
echo "=========================================="
echo "To:      $TO"
echo "Subject: $SUBJECT"
if [[ -n "$ATTACHMENT" ]]; then
    if [[ -f "$ATTACHMENT" ]]; then
        ATTACH_SIZE=$(du -h "$ATTACHMENT" | cut -f1)
        echo "Attachment: $(basename "$ATTACHMENT") ($ATTACH_SIZE)"
    else
        echo "WARNING: Attachment not found: $ATTACHMENT"
    fi
fi
echo "------------------------------------------"
echo "$BODY"
echo "=========================================="

# Check for common issues
ISSUES=0
if echo "$SUBJECT" | grep -qP '\$\d'; then
    echo "WARNING: Subject contains \$ followed by a digit (possible shell variable issue)"
    ISSUES=$((ISSUES + 1))
fi
if echo "$BODY" | grep -qP '\$\d'; then
    echo "WARNING: Body contains \$ followed by a digit (possible shell variable issue)"
    ISSUES=$((ISSUES + 1))
fi

if [[ -n "$ATTACHMENT" && -f "$ATTACHMENT" ]]; then
    ATTACH_BYTES=$(stat -c%s "$ATTACHMENT" 2>/dev/null || stat -f%z "$ATTACHMENT" 2>/dev/null || echo 0)
    if [[ "$ATTACH_BYTES" -gt 3145728 ]]; then
        echo "ERROR: Attachment exceeds 3MB limit ($ATTACH_BYTES bytes)"
        ISSUES=$((ISSUES + 1))
    fi
fi

if [[ "$ISSUES" -gt 0 ]]; then
    echo ""
    echo "Found $ISSUES potential issue(s). Review above warnings before sending."
fi

echo ""

if [[ "$CONFIRM" == true ]]; then
    echo "Sending..."
    ATTACH_ARG=""
    if [[ -n "$ATTACHMENT" ]]; then
        ATTACH_ARG="--attachment $ATTACHMENT"
    fi
    $GAPI mail send --to "$TO" --subject "$SUBJECT" --body "$BODY" $ATTACH_ARG
else
    echo "To send, re-run with --confirm flag:"
    ATTACH_ARG=""
    if [[ -n "$ATTACHMENT" ]]; then
        ATTACH_ARG="--attachment \"$ATTACHMENT\""
    fi
    echo "  $0 --to \"$TO\" --subject \"$SUBJECT\" --body-file \"$BODY_FILE\" $ATTACH_ARG --confirm"
fi
