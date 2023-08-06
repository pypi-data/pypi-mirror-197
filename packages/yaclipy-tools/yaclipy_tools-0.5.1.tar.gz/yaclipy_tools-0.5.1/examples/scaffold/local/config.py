from config import test
from pyutil.some_tool import SomeTool
from yaclipy_tools.config import Config

@test.override()
def test():
    SomeTool.data_path('local/data2')


