# -*- coding: utf-8 -*-

import pytest

import os
import sys
sys.path.append('..')

from main.slackPost import SlackPost

@pytest.fixture(scope="module", autouse=True)
def set_env_value():
    os.environ['SLACK_URL'] = 'dummy'

def test_post():
    slack = SlackPost()
    slack.post('In', None, None, True)
    assert True
