#!/bin/sh
# Build the demo site and upload it to Cloudflare Pages.
# Run from anywhere:  ./deploy_site.sh
# First time on this computer:  npx --yes wrangler@4.129.1 login
set -e
cd "$(dirname "$0")"
python3 build_site.py
npx --yes wrangler@4.129.1 pages deploy site --project-name lights-on-musical --branch main
