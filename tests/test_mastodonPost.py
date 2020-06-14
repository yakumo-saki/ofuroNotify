# -*- coding: utf-8 -*-

import logging
import pytest

import os
import sys
sys.path.append('..')

from main.mastodonPost import MastodonPost

@pytest.fixture(scope="module", autouse=True)
def set_env_value():
    os.environ['MASTODON_URL'] = 'dummy'
    os.environ['MASTODON_ACC_TOKEN'] = 'dummy'

def test_post(caplog):
    caplog.set_level(logging.INFO)

    post = MastodonPost()
    post.post('In', None, None, True)
    assert True
