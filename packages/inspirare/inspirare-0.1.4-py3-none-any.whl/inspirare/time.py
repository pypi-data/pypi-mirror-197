import arrow 


def get_timestamp_by_date(date_):
    """日期转时间戳"""
    return arrow.get(date_).timestamp


def get_timestamp():
    """获取当前时间戳"""
    now = arrow.now()
    return str(now.timestamp)


def get_today():
    """获取当前日期"""
    now = arrow.now()
    return now.date()


def parse(time_str, *arg, **kwargs):
    """解析日期为datetime格式"""
    return arrow.get(time_str, *arg, **kwargs)


def format(a, fmt='YYYY-MM-DD'):
    """ 日期格式化"""
    if not isinstance(a, arrow.arrow.Arrow):
        a = arrow.get(a) if a else None
    return a.format(fmt) if a else None


def reformat(time_str, fmt1, fmt2):
    if not time_str:
        return ''
    a = arrow.get(time_str, fmt1)
    return a.format(fmt2)


def get_now():
    """获取当前时间"""
    return arrow.now().datetime


def get_now_as_string():
    """获取当前时间字符串"""
    now = arrow.now()
    return now.format('YYYY-MM-DD HH:mm:ss')


def get_days_of_current_month():
    """获取本月日期"""
    now = arrow.now()
    first_day_of_the_month = now.replace(day=1)
    first_day_of_next_month = first_day_of_the_month.shift(months=1)
    last_day_of_the_month = first_day_of_next_month.shift(days=-1)
    return [a.date() for a in arrow.Arrow.range('day', first_day_of_the_month, last_day_of_the_month)]
    

def get_days_of_current_season():
    """获取本季度日期"""
    now = arrow.now()
    month = now.month 
    if month < 4:
        pass 
        start_month = 1
    elif month < 7:
        start_month = 4
    elif month < 10:
        start_month = 7
    else:
        start_month = 10
    first_day_of_the_season = now.replace(month=start_month, day=1)
    first_day_of_next_season = first_day_of_the_season.shift(months=3)
    last_day_of_the_season = first_day_of_next_season.shift(days=-1)
    return [a.date() for a in arrow.Arrow.range('day', first_day_of_the_season, last_day_of_the_season)]
    
    
def get_days_of_current_year():
    """获取本年度日期"""
    now = arrow.now()
    first_day_of_the_year = now.replace(month=1, day=1)
    first_day_of_next_year = first_day_of_the_year.shift(years=1)
    last_day_of_the_year = first_day_of_next_year.shift(days=-1)
    return [a.date() for a in arrow.Arrow.range('day', first_day_of_the_year, last_day_of_the_year)]

    
def get_months_in_between(start_month_str, end_month_str):
    """获取两个月中间月份"""
    start_month = arrow.get(start_month_str) if start_month_str else arrow.get('2000-01')
    end_month = arrow.get(end_month_str) if end_month_str else arrow.now()
    months = []
    next_month = start_month
    while(next_month <= end_month):
        months.append(next_month)
        next_month = next_month.shift(months=1)
    return months

 
def get_last_seven_days():
    """获取过去7天日期"""
    now = arrow.now()
    six_days_ago = now.shift(days=-6)
    return [a.date() for a in arrow.Arrow.range('day', six_days_ago, now)]


def get_last_n_days(n):
    """获取过去n天日期"""
    now = arrow.now()
    n_days_ago = now.shift(days=-(n-1))
    return [a.date() for a in arrow.Arrow.range('day', n_days_ago, now)]
