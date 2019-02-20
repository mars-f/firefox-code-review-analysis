# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pandas as pd

def bday_duration(start_date, end_date):
    """Duration in business days."""
    duration = end_date - start_date
    if duration.days < 2:
        # We could have start_date or end_date on a weekend.
        return duration

    weeks_to_close = duration.days // 7

    # Falls over X weekends
    weekends = pd.offsets.Day(-2 * weeks_to_close)

    if end_date.weekday() < start_date.weekday():
        # Falls over an extra weekend.  Subtract 2 calendar days.
        offset = pd.offsets.Day(-2)
    else:
        offset = pd.offsets.Day(0)

    return duration + offset + weekends
