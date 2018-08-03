#coding=utf-8

from datetime import datetime
from time import strptime
import json
import requests
from model import User


class CheckIn(object):
    """ 当前用户的打卡信息查询
    """

    def _query_check_info(self, user):
        """检查当前的打卡情况
        """
        if user is not None:
            check_in_url = \
                'http://localhost:8081/request?url=http:%2F%2Fm.ehr.sunlands.com%2Fmobile-web%2Fattendance%2FselectAttendanceData.do&params=%7B%22account%22:%22'\
                    + user.phone_number + '%22,%22accountType%22:%221%22%7D'
            print('prepar checkin %s' % user.name)
            r = requests.get(check_in_url)
            if r.status_code == 200:
                key_data = json.loads(r.content)['key']
                json_data = json.loads(key_data)
                print('json_data = %s' % json_data)
                check_in_time = json_data['checkInTime']
                check_out_time = json_data['checkOutTime']
                if check_in_time is None:
                    return u'@%s 请注意 还没打上班卡\n' % user.name
                elif check_in_time == check_out_time:
                    now = datetime.now()
                    # check_out_date = strptime(check_out_time, "%Y-%m-%d %H:%M:%S")
                elif check_in_time == check_out_time:
                    if now.hour >= 19:
                        return u'@%s 请注意 还没打下班卡\n' % user.name
                    else:
                        # return u'还没到打下班卡时间，上班卡已经打 %s' % check_in_time
                        print('还没到打下班卡时间，上班卡已经打 %s' % check_in_time)
        return None

    def check_all_user(self):
        msg = u''
        for user in User.all_users():
            result = self._query_check_info(user)
            if result:
                msg += result
        return msg