# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
from dotenv import load_dotenv

import phabricator

import os

PHABRICATOR_URL = "https://phabricator.services.mozilla.com/"

session = requests.Session()
session.headers.update({"User-Agent": "phabricator-metrics mars@mozilla.com"})

load_dotenv()

phab_client = phabricator.PhabricatorClient(
    PHABRICATOR_URL, os.getenv("CONDUIT_TOKEN"), session=session
)

phab_client.verify_api_token()
