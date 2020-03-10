import requests

from bs4 import BeautifulSoup
from terminaltables import AsciiTable

URL = 'http://140.131.110.76/JMobile_STD/AjaxPage/SRHCUR_Schedule_ajax.aspx'
HEADERS = {'X-Requested-With': 'com.hanglong.NTUBStdApp'}
CLASS_INFO_KEY = ('name', 'teacher', 'room')
COURSES_TABLE_HEADS = ['時間 / 日期', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
COURSES_TABLE_SIDES = [
    '第一節(08:10-09:00)',
    '第二節(09:10-10:00)',
    '第三節(10:10-11:00)',
    '第四節(11:10-12:00)',
    '第五節(13:30-14:20)',
    '第六節(14:25-15:15)',
    '第七節(15:25-16:15)',
    '第八節(16:20-17:10)',
    '第九節(17:15-18:05)',
    '十一節(18:30-19:15)',
    '十二節(19:20-20:05)',
    '十三節(20:15-21:00)',
    '十四節(21:05-21:50)',
]


def get_soup(url, data, headers):
    response = requests.post(url, data, headers)
    if response.status_code != 200:
        print('Http error {}'.format(res.status_code))
        exit()
    
    return BeautifulSoup(response.text, 'html.parser')


def main():
    StdNo = input('學號：')
    # StdNo = '10546009'
    data = {'StdNo': StdNo}
    result = [COURSES_TABLE_SIDES]

    for today in range(1, 5):
        data['today'] = today
        soup = get_soup(URL, data, HEADERS)
        _class = []

        for i in soup.find_all('td', 'Stdtd001'):
            # 抓取課表資訊
            if list(i.strings):
                c = ' '.join(list(i.strings))
                # c = dict(zip(CLASS_INFO_KEY, i.strings))
            else:
                c = ''

            _class.append(c)
        
        result.append(_class)
    
    # 矩陣行列互換
    result = map(list,zip(*result))
    table = AsciiTable([COURSES_TABLE_HEADS, *result])
    print(table.table)

if __name__ == '__main__':
    main()
