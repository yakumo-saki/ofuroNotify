# -*- coding: utf-8 -*-

import pytest

import os
import sys
sys.path.append('..')

from main.webhookPost import WebhookPost

@pytest.fixture(scope="module", autouse=True)
def set_env_value():
    os.environ['WEBHOOK_URL'] = 'dummy'

def test_post():
    post = WebhookPost()
    post.post('In', None, None, True)
    assert True
