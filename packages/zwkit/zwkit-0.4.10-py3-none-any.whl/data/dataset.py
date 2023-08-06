import pandas as pd
import pywencai as wc
import tushare as ts
import os
from kit import num_kit, path_kit

'''
数据函数
'''


# 导入工程
class base_data_loader:
    """
    数据加载器
    通过问财获得股票列表
    通过tushare获得股票数据
    """

    def __init__(self, path="../data/", module="data/", file_name="base_data.csv"):
        self.path = path
        self.module = module
        self.file_name = file_name
        self.module_path = path + module
        self.question = None
        self.start = None
        self.end = None
        self.token = None
        self.symbol_index = dict()  # 股票时间索引
        self.filter = set()  # 股票的过滤集
        self.data = pd.DataFrame()
        path_kit.create_dir(self.module_path)

    def __daily_data(self, symbol, start, end, token):
        """
        获取日线数据
        :param symbol:
        :param start:
        :param end:
        :return:
        """
        api = ts.pro_api(token)
        df = ts.pro_bar(
            ts_code=symbol,
            api=api,
            start_date=str(start) + "0101",
            end_date=str(end) + "1231",
            adjfactor=True,
            asset="E",  # 证券类型 E:股票和交易所基金，I:沪深指数,C:数字货币,FT:期货 FD:基金/O期权/H港股/CB可转债
            freq="D",  # D:日线 W:周 M:月
            adj="hfq",  # 不复权:None 前复权:qfq 后复权:hfq
            retry_count=99  # 重试次数
        )
        return df[::-1]

    def __daily(self, start_date, end_date, token, symbols: list):
        """
        获取日线数据
        :param start_date:
        :param end_date:
        :param symbols:
        :return:
        """
        result = pd.DataFrame()
        if len(symbols) == 0:
            return pd.DataFrame()
        for symbol in symbols:
            df = self.__daily_data(symbol, start_date, end_date, token)
            result = pd.concat([result, df])
        return result

    def filter_symbols(self, symbols: list):
        """
        过滤数据列表
        :param symbols: 以列表的形式填入股票代码
        :return:
        """
        symbols_set = set(symbols)
        self.filter.update(symbols_set)

    def __get_symbols_by_wc(self, question, columns: list):
        """
        股票列表
        通过问财获得股票列表
        """
        result = pd.DataFrame()
        for i in range(self.start, self.end + 1):
            quest = question % (i, i - 1)
            data = wc.get(question=quest, loop=True)
            data = data[columns]
            data = data[~data['股票代码'].isin(self.filter)]
            data['trade_date'] = i
            result = pd.concat([result, data])
        return result

    def get_data(self, question, start, end, token):
        """
        获取总数据集
        优先在本地读取，如果本地没有从互联网获取
        :param token:
        :param end:
        :param start:
        :param question:
        :param data_path: 默认的数据集路径
        :return:
        """

        self.question = question
        self.start = start
        self.end = end

        if os.path.exists(self.module_path + self.file_name):
            print("读取本地数据集")
            self.data = pd.read_csv(self.module_path + self.file_name)
        else:
            print("从互联网获取数据集")
            symbols_list = self.__get_symbols_by_wc(self.question, columns=['股票代码'])
            print("开始遍历")
            for index, symbol in enumerate(symbols_list['股票代码'].unique()):
                print("数据进度百分比:%s" % (index / len(symbols_list['股票代码'].unique()) * 100), end='\r', flush=True)
                self.data = pd.concat([self.data, self.__daily_data(symbol, self.start, self.end, token)])
        # 重置索引
        self.data = self.data.reset_index(drop=True)
        # 将日期转换为字符串
        self.data['trade_date'] = self.data['trade_date'].apply(lambda x: str(x))
        # 将数据里的数字类型转换为float
        self.data = self.data.applymap(lambda x: float(x) if isinstance(x, (int, float)) else x)
        return self.data

    def observe(self, mlflow):
        """
        观察数据集
        :return:
        """
        # 数据报告
        mlflow.log_text("\n".join(self.__data_report()), self.module + "data_report.txt")
        # 获取每个股票的时间个数
        mlflow.log_dict(self.data.groupby('ts_code')['trade_date'].count().to_dict(), self.module + "data_count.txt")
        # 每个数据的缺失日期情况
        mlflow.log_text(self.__row_nan_trade_date(), self.module + "data_trade_nan.txt")

    def save(self, path=None, name=None):
        """
        保存数据集
        :param name:
        :param path:
        :return:
        """
        file_path = self.module_path if path is None else path
        file_name = self.file_name if name is None else name
        self.data.to_csv(file_path + file_name, index=False, encoding='utf-8', )

    def __data_report(self):
        """
        数据报告
        常规基础数据
        :return:
        """
        data = []
        # stringbuffer的数据报告
        data.append("开始日期:%s" % self.start)
        data.append("结束日期:%s" % self.end)
        data.append("数据总量:%s" % len(self.data))
        data.append("数据列数:%s" % len(self.data.columns))
        data.append("数据列名:%s" % self.data.columns.tolist())
        data.append("数据集缺失值:%s" % self.data.isnull().sum())
        return data

    def __row_nan_trade_date(self):
        text = ''
        symbols = self.data["ts_code"].unique()
        trades = self.data["trade_date"].unique()
        for symbol in symbols:
            trade_list = pd.DataFrame(trades)
            trade_list.columns = ['trade_date']
            trade_data = pd.merge(trade_list, self.data[self.data['ts_code'] == symbol], on='trade_date', how='left')
            trade_data = trade_data[trade_data['ts_code'].isnull()]
            if len(trade_data) != 0:
                text = text + symbol + ','
                text = text + ",".join(trade_data['trade_date'].astype('str').tolist()) + '\n'
        return text


# 特征工程
class feature_data_loader:
    """
    数据特征工程
    1.添加特征
    2.观察数据集
    3.保存数据集
    """

    def __init__(self, base_data=None, path="../data/", module="data/", file_name="feature_data.csv"):
        self.data = base_data
        self.features_list = []
        self.result = pd.DataFrame()
        self.path = path
        self.module = module
        self.file_name = file_name
        self.module_path = path + module

    def add_feature(self, feature):
        """
        添加特征
        :param feature:
        :return:
        """
        for func in feature:
            self.features_list.append(func)
        # 添加特征后，重新初始化数据集

    def obverse(self):
        """
        观察数据集
        :return:
        """
        pass

    def save(self, path=None, name=None):
        """
        保存数据集
        :param name:
        :param path:
        :return:
        """
        file_path = self.module_path if path is None else path
        file_name = self.file_name if name is None else name
        self.result.to_csv(file_path + file_name, index=False, encoding='utf-8')

    def execute(self):
        """
        执行特征工程
        :return:
        """
        symbol_list = self.data['ts_code'].unique()
        columns = self.data.columns
        for index,symbol in enumerate(symbol_list):
            print("数据进度百分比:%s" % (index / len(symbol_list) * 100))
            symbol_data = pd.DataFrame(self.data[self.data['ts_code'] == symbol])
            symbol_data.reset_index(drop=True, inplace=True)
            for func in self.features_list:
                func(symbol_data)
            # 将symbol_data 按照旧列和新列分成2个数据集
            symbol_data_left = symbol_data[columns]
            symbol_data_right = symbol_data[symbol_data.columns[~symbol_data.columns.isin(symbol_data_left.columns)]]
            symbol_data_right.applymap(lambda x: round(float(x), 2) if isinstance(x, (int, float)) else x)
            # 将新列数据集和旧列数据集合并
            data = pd.merge(symbol_data_left, symbol_data_right, left_index=True, right_index=True)
            self.result = pd.concat([self.result, data])
        return self.result


# 训练测试工程
class trains_data_loader:

    def __init__(self, base_data=None, path="../data/", module="data/"):
        self.base = base_data
        self.path = path
        self.module = module
        self.module_path = path + module
        self.train_X = pd.DataFrame()
        self.train_y = pd.DataFrame()
        self.test_X = pd.DataFrame()
        self.test_y = pd.DataFrame()
        self.drop_column = []

    def drop_columns(self, columns):
        """
        删除指定列
        :param columns:
        :return:
        """
        for column in columns:
            self.drop_column.append(column)

    def train_split_by_time(self, start, end):
        """
        :param start:
        :param end:
        :return:
        """
        self.train_X = self.base[(self.base['trade_date'] > start) & (self.base['trade_date'] < end)]
        self.train_X = self.train_X.drop(self.drop_column, axis=1)
        self.train_y = self.base[(self.base['trade_date'] > start) & (self.base['trade_date'] < end)]
        self.train_y = self.train_y['flag']
        return self.train_X, self.train_y

    def test_split_by_time(self, start, end):
        """
        :param start:
        :param end:
        :return:
        """
        self.test_X = self.base[(self.base['trade_date'] > start) & (self.base['trade_date'] < end)]
        self.test_X = self.test_X.drop(self.drop_column, axis=1)
        self.test_y = self.base[(self.base['trade_date'] > start) & (self.base['trade_date'] < end)]
        self.test_y = self.test_y['flag']
        return self.test_X, self.test_y

    def obverse(self, mlflow):
        mlflow.log_metric("train_label_1", len(self.train_X[self.train_X['flag'] == 1]) / len(self.train_X) * 100)
        mlflow.log_metric("train_label_0", len(self.train_X[self.train_X['flag'] == 1]) / len(self.train_X) * 100)
        mlflow.log_metric("train_label_-1", len(self.train_X[self.train_X['flag'] == 1]) / len(self.train_X) * 100)

    def save(self, path=None):
        """
        保存数据集
        :param path:
        :return:
        """
        file_path = self.module_path if path is None else path
        self.train_X.to_csv(file_path + 'train_X.csv', index=False, encoding='utf-8')
        self.train_y.to_csv(file_path + 'train_y.csv', index=False, encoding='utf-8')
        self.test_X.to_csv(file_path + 'test_X.csv', index=False, encoding='utf-8')
        self.test_y.to_csv(file_path + 'test_y.csv', index=False, encoding='utf-8')


class backtrader_data_loader:

    def __init__(self, path='../data/', module='data/', csv_data='dataset.csv'):
        self.path = path
        self.module = module
        self.data_path = self.path + self.module
        self.csv_data = csv_data
        self.data = pd.DataFrame()

    def get_data(self, start, end):
        """
        复权前的数据+ 复权后的指标
        :param start:
        :param end:
        :return:
        """
        data = pd.read_csv(self.path + self.csv_data)
        self.data = data[(data['trade_date'] > start) & (data['trade_date'] < end)]
        self.data['open'] = round(self.data['open'] / self.data['adj_factor'], 2)
        self.data['high'] = round(self.data['high'] / self.data['adj_factor'], 2)
        self.data['low'] = round(self.data['low'] / self.data['adj_factor'], 2)
        self.data['close'] = round(self.data['close'] / self.data['adj_factor'], 2)
        self.data['amount'] = round(self.data['amount'] / self.data['adj_factor'], 2)
        self.data.drop(['pre_close', 'change', 'pct_chg', 'flag'], axis=1, inplace=True)
        self.data['trade_date'] = self.data['trade_date'].apply(lambda x: pd.to_datetime(x, format='%Y%m%d'))
        self.data = self.data.rename(columns={'trade_date': 'datetime',
                                              'vol': 'volume'
                                              })
        return self.data

    def save(self, module, name):
        path = self.path + module
        if not os.path.exists(path):
            os.mkdir(path)
        self.data.to_csv(path + name, index=False, encoding='utf-8')
