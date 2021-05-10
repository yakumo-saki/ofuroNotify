# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from decimal import *
import math

class PostBase:

    CLICK_SINGLE = 'SINGLE'
    CLICK_LONG = 'LONG'
    CLICK_DOUBLE = 'DOUBLE'

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


    def create_message(self, inOut, lastIn, duration_sec, clickType):

        if inOut == 'In':
            if clickType == self.CLICK_DOUBLE:
                message = f'シャワる 🛀'
            elif clickType == self.CLICK_LONG:
                message = f'おふろる 📲🛀'
            else:
                message = f'おふろる 🛀'
        else:
            duration = self.duration_to_text(duration_sec)
            message = f'ほかぱい！ ✨ ({duration})'

        return message


    def post(self, inOut, lastIn, duration_sec, clicktype, dryrun = False):
        raise InvalidOperation("can't call post_base.post()")
