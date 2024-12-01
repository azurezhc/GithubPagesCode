#!/bin/bash

set -o pipefail

SITEROOT="$(pwd)"

#if [ -d exampleSite ]; then
#    SITESRC=exampleSite
#fi

if npx html-validate --config .htmlvalidate-minified.json "${SITEROOT}"/public 2>&1 | tee html-validate.log; then
    echo "ok"
else
    echo "not ok"
fi
