from os.path import dirname, basename, isfile, join
import glob

# 将包名显示暴漏在外，这样from api import *就会导入该文件夹下的所有.py文件
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

# 如果这里不导入，当其他文件使用from utils import api时，api.TRON无法找到
# 确保api尽量不调用其他文件，如果其他文件也调用api则会出现循环
from utils.api import *
