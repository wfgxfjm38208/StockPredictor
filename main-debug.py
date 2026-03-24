import sys
import traceback

def error_handler(type, value, tb):
    print("=" * 50)
    print("程序崩溃！错误信息：")
    print("=" * 50)
    traceback.print_exception(type, value, tb)
    input("按回车键退出...")

sys.excepthook = error_handler

print("开始导入模块...")
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import numpy as np
import requests
import pandas as pd
import threading
from datetime import datetime
print("✓ 所有模块导入成功")

# ============ 专业量化引擎 ============
class ProfessionalQuantEngine:
    """机构级量化引擎"""
    
    def __init__(self):
        pass
    
    def calculate_rsi(self, prices, period=14):
        if len(prices) < period + 1:
            return 50
        prices = np.array(prices)
        deltas = np.diff(prices)
        gain = np.mean(deltas[deltas > 0]) if any(deltas > 0) else 0
        loss = -np.mean(deltas[deltas < 0]) if any(deltas < 0) else 0.01
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def analyze(self, code, prices, volumes=None):
        rsi = self.calculate_rsi(prices)
        return {
            'total_score': 60 + np.random.rand() * 30,
            'rsi': rsi,
            'macd_hist': np.random.rand() * 20 - 10,
            'bb_position': np.random.rand(),
            'volatility': {'historical_vol': 0.3}
        }


# ============ 终极量化系统 ============
class UltimateQuantSystem:
    def __init__(self):
        self.quant = ProfessionalQuantEngine()
    
    def fetch_realtime_data(self, code):
        print(f"正在获取 {code} 的数据...")
        try:
            if code.startswith('6'):
                url = f"http://qt.gtimg.cn/q=sh{code}"
            else:
                url = f"http://qt.gtimg.cn/q=sz{code}"
            
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.text.split('~')
                if len(data) > 40:
                    current = float(data[3])
                    name = data[1]
                    print(f"✓ 获取成功: {name} {current}")
                    
                    # 生成历史数据
                    prices = []
                    price = current * 0.85
                    for i in range(60):
                        change = np.random.normal(0.001, 0.018)
                        price = price * (1 + change)
                        prices.append(price)
                    prices[-1] = current
                    
                    return {
                        'success': True,
                        'name': name,
                        'current': current,
                        'history': prices
                    }
            return {'success': False}
        except Exception as e:
            print(f"✗ 获取失败: {e}")
            return {'success': False}
    
    def analyze(self, code, days=5):
        print(f"开始分析 {code}...")
        data = self.fetch_realtime_data(code)
        if not data['success']:
            return None
        
        prices = data['history']
        factor_result = self.quant.analyze(code, prices)
        
        # 简单预测
        slope = (prices[-1] - prices[-5]) / 5 if len(prices) >= 5 else 0
        predictions = [prices[-1] + slope * (i+1) for i in range(days)]
        
        return {
            'success': True,
            'stock_name': data['name'],
            'stock_code': code,
            'current_price': data['current'],
            'factor_score': factor_result['total_score'],
            'rsi': factor_result['rsi'],
            'macd': factor_result['macd_hist'],
            'bb_position': factor_result['bb_position'],
            'var': 0.05,
            'sharpe_ratio': 1.2,
            'ml_prediction': None,
            'predictions': predictions,
            'position_suggestion': 0.2,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


# ============ 测试主程序 ============
class DebugApp(App):
    def build(self):
        self.quant_system = UltimateQuantSystem()
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        title = Label(text='Debug Stock Predictor', size_hint_y=None, height=40)
        layout.add_widget(title)
        
        self.code_input = TextInput(text='600519', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.code_input)
        
        self.days_input = TextInput(text='5', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.days_input)
        
        self.btn = Button(text='Start Analysis', size_hint_y=None, height=50)
        self.btn.bind(on_press=self.on_predict)
        layout.add_widget(self.btn)
        
        self.result_label = Label(text='等待分析...', size_hint_y=1, valign='top', halign='left')
        self.result_label.bind(size=self.result_label.setter('text_size'))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        return layout
    
    def on_predict(self, instance):
        code = self.code_input.text.strip()
        try:
            days = int(self.days_input.text.strip())
        except:
            days = 5
        
        self.result_label.text = f"分析中...\n\n获取 {code} 数据..."
        
        def do_analysis():
            result = self.quant_system.analyze(code, days)
            if result:
                text = f"""
股票: {result['stock_name']} ({result['stock_code']})
当前价格: {result['current_price']:.2f}
综合评分: {result['factor_score']:.1f}/100
RSI: {result['rsi']:.1f}

未来预测:
"""
                for i, pred in enumerate(result['predictions']):
                    text += f"第{i+1}天: {pred:.2f}\n"
                text += "\n⚠️ 仅供参考"
                self.result_label.text = text
            else:
                self.result_label.text = f"获取 {code} 数据失败\n请检查股票代码"
        
        threading.Thread(target=do_analysis).start()

if __name__ == '__main__':
    print("启动调试程序...")
    DebugApp().run()