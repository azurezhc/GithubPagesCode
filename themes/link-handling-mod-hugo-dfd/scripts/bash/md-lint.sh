#!/bin/bash

set -o pipefail

SITEROOT="$(pwd)"

if [ -d "$(pwd)"/exampleSite ]; then
    SITEROOT="$(pwd)"/exampleSite
fi

if npx markdownlint-cli2 README.md "${SITEROOT}/content/*.md" "${SITEROOT}/content/**/*.md" 2>&1 | tee md-lint.log; then
    echo "ok"
else
    echo "not ok"
fi
