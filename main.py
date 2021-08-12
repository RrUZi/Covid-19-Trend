import urllib.request
from urllib import parse
import json
import sqlite3


provinces: list = [
        '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '甘肃', '青海', \
        '内蒙古', '陕西', '广西', '西藏', '宁夏', '新疆', \
        '北京', '天津', '上海', '重庆', \
        '香港', '澳门', '台湾']
url: str = "https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province="
database_path = 'covid.db'


def create_table():
    field: str = ''
    for pro in provinces:
        if pro != provinces[-1]:
            field += pro + ' integer,'
        else:
            field += pro + ' integer'
    return 'create table if not exists history(date text primary key,' + field + ')'


if __name__ == '__main__':
    print('loading...')
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute(create_table())

    for pro in provinces:
        jsdata = urllib.request.urlopen(url + parse.quote(pro)).read()
        data = json.loads(jsdata)['data']

        for daily in data:
            date = str(daily['year']) + '.' + str(daily['date'])
            cur.execute("select date from history where date='" + date + "'")

            if cur.fetchone():  # if exist
                cur.execute("update history set " + pro + "=" + str(daily['newConfirm']) + " where date='" + date + "'")
            else:
                cur.execute("insert into history(date," + pro + ") values ('" + date + "'," + str(daily['newConfirm']) + ")")
            con.commit()
    print('finish')