import sys
import traceback

def error_handler(type, value, tb):
    print("=" * 50)
    print("错误信息：")
    print("=" * 50)
    traceback.print_exception(type, value, tb)
    input("按回车键退出...")

sys.excepthook = error_handler

print("开始导入模块...")

try:
    from kivy.app import App
    print("✓ Kivy.app 导入成功")
except Exception as e:
    print("✗ Kivy.app 导入失败:", e)

try:
    import numpy as np
    print("✓ numpy 导入成功")
except Exception as e:
    print("✗ numpy 导入失败:", e)

try:
    import requests
    print("✓ requests 导入成功")
except Exception as e:
    print("✗ requests 导入失败:", e)

try:
    from sklearn.ensemble import RandomForestRegressor
    print("✓ sklearn 导入成功")
except Exception as e:
    print("✗ sklearn 导入失败:", e)

try:
    import pandas as pd
    print("✓ pandas 导入成功")
except Exception as e:
    print("✗ pandas 导入失败:", e)

print("\n所有模块导入完成！")