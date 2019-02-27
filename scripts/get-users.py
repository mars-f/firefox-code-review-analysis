#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Fetch a series of revisions from Phabricator and save them to disk."""
import json
import sys

from helpers import phab_client

if len(sys.argv) < 2:
    print("Error: missing required argument [outfile]")
    print(f"Usage: {sys.argv[0]} [outfile]")
    sys.exit(1)
else:
    outfile_name = sys.argv[1]

count = 0
after = None    # Cursor indicating the start of the next results page.

with open(outfile_name, "w") as fp:
    while True:
        response = phab_client.call_conduit(
            "user.search",
            attachments={},
            constraints={"isAdmin": False, "isBot": False, "isMailingList": False},
            after=after,
        )
        revisions = response["data"]
        count += len(revisions)
        fp.writelines(json.dumps(r) + "\n" for r in revisions)

        cursor = response["cursor"]
        after = cursor["after"]

        if after is None:
            # There are no more records.
            break

print(f"Wrote {count} records to {outfile_name}")
sys.exit(0)
