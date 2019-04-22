from pytz import timezone
from datetime import datetime

class ChinaTime():
    def __init__(self):
        self.day = None
        self.time = None
        self.minute = None
        self.second = None


    def getChinaTime(self):
        utc_tz = timezone('UTC')
        utcnow = datetime.utcnow().replace( tzinfo=utc_tz )
        cst_tz = timezone('Asia/Shanghai')
        self.day = utcnow.astimezone( cst_tz ).strftime( '%Y-%m-%d' )
        self.time = utcnow.astimezone(cst_tz).strftime('%H:%M:%S')
        self.minute = utcnow.astimezone(cst_tz).strftime('%M')
        self.second = utcnow.astimezone(cst_tz).strftime('%S')
        return self.day+' '+self.time

if __name__ == '__main__':
    chinatime = ChinaTime()
    time = chinatime.getChinaTime()
    print( '获取中国时间：',time)
    print('获取日期：',chinatime.day)
    print('获取时间：',chinatime.time)
    print('获取分：', chinatime.minute)
    print('获取秒：', chinatime.second)