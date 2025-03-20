import json
import time


def read_license_json():
    with open('../sources/License_json/license.json', 'r') as f:
        license = json.load(f)
    license_dict = dict(license)

    return license_dict


def license_check(licnese):
    license_dict = read_license_json()
    if licnese in license_dict:
        time_now = time.time()
        start_time = license_dict[licnese]['start']
        end_time = license_dict[licnese]['end']
        if time_now <= time.mktime(time.strptime(end_time, '%Y-%m-%d')):
            return (True, (start_time, end_time))
        elif time_now > time.mktime(time.strptime(end_time, '%Y-%m-%d')):
            return (False, f'最后可用日期 {end_time}，许可证已过期，请联系管理员。')
    else:
        return (False, '许可证不存在')
