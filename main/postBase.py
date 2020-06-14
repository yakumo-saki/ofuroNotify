# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from decimal import *
import math

class PostBase:

    def duration_to_text(self, second):
        delta = timedelta(seconds=int(second) )

        ret = ""
        if (delta.days > 0):
            ret = f'{delta.days}日'

        m, s = divmod(delta.seconds, 60)
        h, m = divmod(m, 60)

        if (h > 0):
            ret = f'{ret} {h}時間'

        ret = f'{ret} {m}分 {s}秒'

        return ret.strip()


    def create_message(self, inOut, lastIn, duration_sec):

        if inOut == 'In':
            message = f'おふろる 🛀'
        else:
            duration = self.duration_to_text(duration_sec)
            message = f'ほかぱい！ ✨ ({duration})'

        return message


    def post(self, inOut, lastIn, duration_sec, dryrun = False):
        raise InvalidOperation("cannnot call post_base.post()")
