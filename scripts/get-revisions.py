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

# The mozilla-central repository object ID in Phabricator.
MOZILLA_CENTRAL_REPO_ID = "PHID-REPO-saax4qdxlbbhahhp2kg5"

AUTHORS_BLACKLIST = [
    # We want to skip all revisions created by the "gfx" user.  The account
    # is used by the Mozilla Graphics team to run scripts that import sourcecode
    # from GitHub.  The reviews created are automated and no good for reporting
    # purposes.
    "PHID-USER-mdjzlkaguw6tdqb256gl",
]

count = 0
skipped_by_blacklist = 0
after = None    # Cursor indicating the start of the next results page.

with open(outfile_name, "w") as fp:
    while True:
        response = phab_client.call_conduit(
            "differential.revision.search",
            attachments={"reviewers": True, "reviewers-extra": True},
            constraints={"repositoryPHIDs": [MOZILLA_CENTRAL_REPO_ID]},
            after=after,
        )
        revisions = response["data"]

        for revision in revisions:
            author = revision["fields"]["authorPHID"]
            if author in AUTHORS_BLACKLIST:
                skipped_by_blacklist += 1
                continue

            count += 1
            fp.write(json.dumps(revision) + '\n')

        cursor = response["cursor"]
        after = cursor["after"]

        if after is None:
            # There are no more records.
            break

print(f"Skipped {skipped_by_blacklist} records by blacklisted authors")
print(f"Wrote {count} records to {outfile_name}")
sys.exit(0)
