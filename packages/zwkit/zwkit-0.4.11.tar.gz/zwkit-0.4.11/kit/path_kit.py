import os


def create_dir(path):
    """
    判断文件是否存在
    不存在则创建
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
