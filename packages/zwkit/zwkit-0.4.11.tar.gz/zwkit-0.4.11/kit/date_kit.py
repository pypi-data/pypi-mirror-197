import pandas as pd


def get_before_date(date, days=60):
    """
    取得指定日期前60天的日期
    :param date:
    :param days:
    :return:
    """
    date = pd.to_datetime(date)
    date = date - pd.Timedelta(days=days)
    return date.strftime("%Y-%m-%d")

def now(type="%Y%m%d%H%M%S"):
    """
    获取当前时间
    :return:
    """
    return pd.to_datetime("now").strftime(type)