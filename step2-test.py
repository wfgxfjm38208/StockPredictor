from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import requests
import numpy as np

class Step2App(App):
    def __init__(self):
        super().__init__()
        self.analyzing = False
    
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 标题
        title = Label(
            text='Stock Predictor v2.0 - Linear Regression',
            size_hint_y=None,
            height=40,
            font_size='18sp',
            bold=True
        )
        layout.add_widget(title)
        
        # 股票代码输入
        layout.add_widget(Label(text='Stock Code:', size_hint_y=None, height=25))
        self.code_input = TextInput(text='600519', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.code_input)
        
        # 预测天数
        layout.add_widget(Label(text='Days:', size_hint_y=None, height=25))
        self.days_input = TextInput(text='5', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.days_input)
        
        # 按钮
        self.btn = Button(text='Predict', size_hint_y=None, height=50)
        self.btn.bind(on_press=self.on_predict)
        layout.add_widget(self.btn)
        
        # 结果区域
        self.result_label = Label(
            text='Result...',
            size_hint_y=1,
            valign='top',
            halign='left'
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        return layout
    
    def fetch_data(self, code):
        """获取股票实时数据"""
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
                    return {
                        'name': data[1],
                        'current': float(data[3]),
                        'success': True
                    }
            return {'success': False}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_simulated_history(self, current_price, days=60):
        """生成模拟历史数据"""
        prices = []
        price = current_price * 0.85
        for i in range(days):
            change = np.random.normal(0.001, 0.018)
            price = price * (1 + change)
            prices.append(price)
        prices[-1] = current_price
        return prices
    
    def linear_predict(self, prices, pred_days):
        """线性回归预测"""
        x = np.arange(len(prices))
        y = np.array(prices)
        slope, intercept = np.polyfit(x, y, 1)
        predictions = slope * (len(prices) + np.arange(pred_days)) + intercept
        return predictions, slope, intercept
    
    def on_predict(self, instance):
        code = self.code_input.text.strip()
        try:
            days = int(self.days_input.text.strip())
            days = max(1, min(30, days))
        except:
            days = 5
        
        self.result_label.text = f"Fetching data for {code}..."
        
        data = self.fetch_data(code)
        
        if data['success']:
            current = data['current']
            # 生成模拟历史数据
            prices = self.generate_simulated_history(current)
            
            # 线性预测
            predictions, slope, intercept = self.linear_predict(prices, days)
            
            # 构建结果
            result_text = f"""
========================================
Stock: {data['name']} ({code})
Current Price: {current:.2f}
========================================

[Linear Regression Model]
y = {slope:.4f}x + {intercept:.2f}

[Future Predictions]
"""
            for i, pred in enumerate(predictions):
                change = (pred - current) / current * 100
                arrow = "▲" if change > 0 else "▼" if change < 0 else "→"
                result_text += f"Day {i+1}: {pred:.2f}  {arrow} {change:+.2f}%\n"
            
            result_text += """
========================================
⚠️ Analysis for reference only
    Invest at your own risk
========================================
"""
            self.result_label.text = result_text
        else:
            self.result_label.text = f"""
Failed to fetch data for {code}

Please check:
- Stock code format (600xxx for Shanghai, 000xxx for Shenzhen)
- Network connection
"""

if __name__ == '__main__':
    Step2App().run()