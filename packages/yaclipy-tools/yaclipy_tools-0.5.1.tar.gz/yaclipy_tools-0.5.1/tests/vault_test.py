from yaclipy_tools import vault
from yaclipy_tools.orphan_branch import FStat

def test_fstat():
    a = FStat.REM | FStat.GPG
    b = FStat.REM | FStat.GPG | FStat.TRACKED
    print(a in b)
    print((FStat.GPG | FStat.TRACKED) in a)
    