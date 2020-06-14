# -*- coding: utf-8 -*-

import logging
import pytest

import os
import sys
sys.path.append('..')

from main.webhookPost import WebhookPost

@pytest.fixture(scope="module", autouse=True)
def set_env_value():
    os.environ['WEBHOOK_URL'] = 'dummy'

def test_post(caplog):
    caplog.set_level(logging.INFO)
    post = WebhookPost()
    post.post('In', None, None, True)
    assert True
