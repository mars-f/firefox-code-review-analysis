#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Fetch a series of revision transactions from Phabricator and save them to disk."""
import json
import sys

import tqdm

from helpers import phab_client

if len(sys.argv) < 3:
    print("Error: missing required arguments")
    print(f"Usage: {sys.argv[0]} [infile] [outfile]")
    sys.exit(1)
else:
    revisions_filename, outfile_name = sys.argv[1:3]

# The mozilla-central repository object ID in Phabricator.
MOZILLA_CENTRAL_REPO_ID = "PHID-REPO-saax4qdxlbbhahhp2kg5"

lines = open(revisions_filename).readlines()
txncount = 0

with open(outfile_name, "w") as txnfile:
    for line in tqdm.tqdm(lines, desc="revisions fetched", total=len(lines)):
        revision = json.loads(line)
        response = phab_client.call_conduit(
            "transaction.search", objectIdentifier=revision["phid"]
        )
        transactions = response["data"]
        txncount += len(transactions)
        txnfile.writelines(json.dumps(t) + "\n" for t in transactions)

print(f"Wrote {txncount} records to {outfile_name}")
sys.exit(0)
