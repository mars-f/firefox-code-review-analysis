# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import businessdays
from datetime import datetime, timedelta


@pytest.mark.parametrize(
    "start_date, end_date, expected_duration",
    [
        # Dates are a datetime tuple of Year, Month, Day, Hour.
        # Expected duration is in days and hours.
        # One hour
        ((2018, 1, 1, 0), (2018, 1, 1, 1), (0, 1)),
        # M-T
        ((2018, 1, 1, 0), (2018, 1, 2, 0), (1, 0)),
        # M-F
        ((2018, 1, 1, 0), (2018, 1, 6, 0), (5, 0)),
        # Mon @ 12am - Fri @11pm
        ((2018, 1, 1, 0), (2018, 1, 5, 23), (4, 23)),
        # Fri @ 11pm - Sat @ 1am
        ((2018, 1, 5, 23), (2018, 1, 6, 1), (0, 2)),
        # Mon @ 1am - M @ 1am next week
        ((2018, 1, 1, 1), (2018, 1, 8, 1), (5, 0)),
        # Mon @ 1am - Fri @ 1am in two weeks.
        # Spans one weekend.
        ((2018, 1, 1, 1), (2018, 1, 12, 1), (9, 0)),
        # Tue @ 1am - Sat @ 1am in two weeks
        # Assume that if the end date is on a weekend then the weekend
        # days count towards the total days.
        ((2018, 1, 2, 1), (2018, 1, 13, 1), (9, 0)),
        # Wed @ 1am - Sun @ 1am in two weeks
        # Assume that if the end date is on a weekend then the weekend
        # days count towards the total days.
        ((2018, 1, 3, 1), (2018, 1, 14, 1), (9, 0)),
        # Thur @ 1am - Mon @ 1am in two weeks.
        # Spans 2 weekends.
        ((2018, 1, 4, 1), (2018, 1, 15, 1), (7, 0)),
        # Fri @ 1am - Tue @ 1am in two weeks.
        # Spans 2 weekends.
        ((2018, 1, 5, 1), (2018, 1, 16, 1), (7, 0)),
    ],
)
def test_business_days_duration(start_date, end_date, expected_duration):
    start = datetime(*start_date)
    end = datetime(*end_date)
    duration = businessdays.bday_duration(start, end)

    expected_duration = timedelta(days=expected_duration[0], hours=expected_duration[1])
    assert duration == expected_duration
