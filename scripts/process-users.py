#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Convert our raw data files to clean parquet data."""
import json
import sys

import pandas as pd

if len(sys.argv) < 3:
    print("Error: missing required arguments")
    print(f"Usage: {sys.argv[0]} [infile] [outfile]")
    sys.exit(1)
else:
    users_filename, outfile_name = sys.argv[1:3]

records = []

for line in open(users_filename):
    data = json.loads(line)
    record = {
        "id": data["id"],
        "phid": data["phid"],
        "username": data["fields"]["username"],
        "realName": data["fields"]["realName"],
        "dateCreated": data["fields"]["dateCreated"],
    }
    records.append(record)

df = pd.DataFrame(records).set_index("id")
df["dateCreated"] = pd.to_datetime(df["dateCreated"], utc=True, unit="s")
df.to_parquet(outfile_name)

print()
print(f"Processed {len(df)} records")
print()
print("Sample row:")
print(df.iloc[0])
print()
print(f"Wrote {outfile_name}")
sys.exit(0)
