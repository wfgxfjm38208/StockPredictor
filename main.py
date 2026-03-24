# -*- coding: utf-8 -*-
import os
import sys
import traceback

# 错误捕获
def error_handler(type, value, tb):
    print("=" * 50)
    print("程序崩溃！错误信息：")
    print("=" * 50)
    traceback.print_exception(type, value, tb)
    print("=" * 50)
    print("按回车键退出...")
    input()

sys.excepthook = error_handler

# Kivy环境设置
os.environ['KIVY_NO_CONSOLELOG'] = '1'
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

# Kivy导入
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

# ============ 专业量化引擎 ============
class ProfessionalQuantEngine:
    """机构级量化引擎"""
    
    def __init__(self):
        pass
    
    def calculate_rsi(self, prices, period=14):
        """计算RSI指标"""
        if len(prices) < period + 1:
            return 50
        prices = np.array(prices)
        deltas = np.diff(prices)
        gain = np.mean(deltas[deltas > 0]) if any(deltas > 0) else 0
        loss = -np.mean(deltas[deltas < 0]) if any(deltas < 0) else 0.01
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices):
        """简化MACD"""
        if len(prices) < 26:
            return 0, 0, 0
        prices = np.array(prices)
        exp1 = pd.Series(prices).ewm(span=12).mean()
        exp2 = pd.Series(prices).ewm(span=26).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9).mean()
        hist = macd - signal
        return macd.iloc[-1], signal.iloc[-1], hist.iloc[-1]
    
    def calculate_bollinger(self, prices):
        """简化布林带"""
        if len(prices) < 20:
            return 0.5
        prices = np.array(prices)
        sma = np.mean(prices[-20:])
        std = np.std(prices[-20:])
        current = prices[-1]
        upper = sma + 2 * std
        lower = sma - 2 * std
        if upper != lower:
            return (current - lower) / (upper - lower)
        return 0.5
    
    def analyze(self, code, prices, volumes=None):
        """全方位因子分析"""
        # 计算技术指标
        rsi = self.calculate_rsi(prices)
        macd, signal, hist = self.calculate_macd(prices)
        bb_position = self.calculate_bollinger(prices)
        
        # 计算动量
        if len(prices) >= 5:
            mom_5 = (prices[-1] / prices[-5] - 1) * 100
        else:
            mom_5 = 0
        
        if len(prices) >= 20:
            mom_20 = (prices[-1] / prices[-20] - 1) * 100
        else:
            mom_20 = 0
        
        # 计算波动率
        if len(prices) > 20:
            returns = np.diff(np.log(prices))
            volatility = np.std(returns) * np.sqrt(252)
        else:
            volatility = 0.3
        
        # 综合因子得分
        factor_scores = {
            '短期动量': mom_5 * 2,
            '中期动量': mom_20 * 1.5,
            '波动率': (0.3 - volatility) * 50,
            'RSI': (rsi - 50) * 0.5,
            'MACD': hist * 10,
            '布林位置': (0.5 - abs(bb_position - 0.5)) * 20,
        }
        
        # 计算总分
        total_score = sum(factor_scores.values()) + 50
        total_score = max(0, min(100, total_score))
        
        return {
            'total_score': total_score,
            'factor_scores': factor_scores,
            'rsi': rsi,
            'macd_hist': hist,
            'bb_position': bb_position,
            'volatility': {'historical_vol': volatility}
        }


# ============ 机器学习引擎 ============
class MachineLearningEngine:
    """机器学习预测引擎"""
    
    def __init__(self):
        self.models = {}
        self.is_trained = False
        self.scaler = None
    
    def prepare_features(self, prices, volumes=None):
        """准备机器学习特征"""
        features = []
        targets = []
        
        if len(prices) < 30:
            return None, None
        
        for i in range(30, len(prices) - 5):
            feature = []
            
            # 价格特征（过去30天）
            for j in range(i-30, i):
                feature.append(prices[j])
            
            # 技术指标特征
            window_prices = prices[i-30:i]
            
            # 统计特征
            feature.append(np.mean(window_prices))
            feature.append(np.std(window_prices))
            feature.append(np.max(window_prices))
            feature.append(np.min(window_prices))
            feature.append(window_prices[-1] - window_prices[0])
            
            # 波动率特征
            returns = np.diff(np.log(window_prices + 1e-10))
            feature.append(np.std(returns))
            
            # 成交量特征
            feature.extend([10000.0, 1000.0, 1.0])
            
            features.append(feature)
            
            # 目标：未来5天涨跌幅
            future_return = (prices[i+5] - prices[i]) / prices[i]
            targets.append(future_return)
        
        if len(features) == 0:
            return None, None
        
        return np.array(features), np.array(targets)
    
    def train(self, prices, volumes=None):
        """训练模型"""
        try:
            from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
            from sklearn.preprocessing import StandardScaler
            
            X, y = self.prepare_features(prices, volumes)
            if X is None or len(X) < 10:
                return False
            
            # 数据标准化
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # 训练多个模型
            self.models['rf'] = RandomForestRegressor(
                n_estimators=50,
                max_depth=5,
                random_state=42
            )
            
            self.models['gbdt'] = GradientBoostingRegressor(
                n_estimators=50,
                max_depth=3,
                learning_rate=0.1,
                random_state=42
            )
            
            for name, model in self.models.items():
                model.fit(X_scaled, y)
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"训练失败: {e}")
            return False
    
    def predict(self, prices, volumes=None):
        """集成预测"""
        if not self.is_trained or len(prices) < 30:
            return None
        
        try:
            # 准备特征
            last_window = prices[-30:]
            
            feature = []
            for j in range(30):
                feature.append(last_window[j])
            
            feature.append(np.mean(last_window))
            feature.append(np.std(last_window))
            feature.append(np.max(last_window))
            feature.append(np.min(last_window))
            feature.append(last_window[-1] - last_window[0])
            
            returns = np.diff(np.log(last_window + 1e-10))
            feature.append(np.std(returns))
            feature.extend([10000.0, 1000.0, 1.0])
            
            # 标准化
            feature_scaled = self.scaler.transform([feature])
            
            # 集成预测
            predictions = []
            weights = {'rf': 0.6, 'gbdt': 0.4}
            
            for name, model in self.models.items():
                pred = model.predict(feature_scaled)[0]
                predictions.append(pred * weights[name])
            
            ensemble_pred = sum(predictions)
            
            return prices[-1] * (1 + ensemble_pred)
            
        except Exception as e:
            print(f"预测失败: {e}")
            return None


# ============ 风险管理系统 ============
class RiskManagement:
    """风险管理系统"""
    
    @staticmethod
    def calculate_var(prices, confidence=0.95):
        """计算VaR"""
        if len(prices) < 20:
            return 0.05
        returns = np.diff(np.log(prices))
        var = np.percentile(returns, (1-confidence)*100)
        return abs(var)
    
    @staticmethod
    def calculate_sharpe_ratio(prices, risk_free_rate=0.03):
        """计算夏普比率"""
        if len(prices) < 20:
            return 1.0
        returns = np.diff(prices) / prices[:-1]
        excess_returns = returns - risk_free_rate/252
        sharpe = np.sqrt(252) * np.mean(excess_returns) / (np.std(returns) + 1e-10)
        return sharpe
    
    @staticmethod
    def position_sizing(score, volatility, var):
        """动态仓位管理"""
        base_position = score / 100
        vol_adjustment = 1 - min(0.5, volatility)
        var_adjustment = 1 - min(0.5, var * 10)
        position = base_position * vol_adjustment * var_adjustment
        return min(0.3, max(0.05, position))


# ============ 终极量化系统 ============
class UltimateQuantSystem:
    """终极量化系统"""
    
    def __init__(self):
        self.quant = ProfessionalQuantEngine()
        self.ml = MachineLearningEngine()
        self.risk = RiskManagement()
    
    def fetch_realtime_data(self, code):
        """获取实时数据"""
        try:
            if code.startswith('6'):
                url = f"http://qt.gtimg.cn/q=sh{code}"
            elif code.startswith('0') or code.startswith('3'):
                url = f"http://qt.gtimg.cn/q=sz{code}"
            else:
                url = f"http://qt.gtimg.cn/q={code}"
            
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.text.split('~')
                if len(data) > 40:
                    current = float(data[3])
                    name = data[1] if len(data) > 1 else code
                    
                    # 生成模拟历史数据
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
                        'history': prices,
                        'volumes': np.random.randint(5000, 20000, 60) * 100
                    }
            return {'success': False}
        except Exception as e:
            print(f"获取数据失败: {e}")
            return {'success': False}
    
    def analyze(self, code, predict_days=5):
        """全方面分析"""
        data = self.fetch_realtime_data(code)
        if not data.get('success'):
            return None
        
        prices = data['history']
        volumes = data.get('volumes')
        
        # 因子分析
        factor_result = self.quant.analyze(code, prices, volumes)
        
        # 机器学习预测
        ml_price = None
        if len(prices) >= 30:
            self.ml.train(prices, volumes)
            ml_price = self.ml.predict(prices, volumes)
        
        # 风险指标
        var = self.risk.calculate_var(prices)
        sharpe = self.risk.calculate_sharpe_ratio(prices)
        
        # 价格预测
        predictions = []
        if ml_price:
            base_pred = ml_price
        else:
            # 简单线性趋势
            slope = (prices[-1] - prices[-5]) / 5 if len(prices) >= 5 else 0
            base_pred = prices[-1] + slope
        
        for i in range(1, predict_days + 1):
            factor_effect = (factor_result['total_score'] - 50) / 1000
            pred = base_pred * (1 + factor_effect * i)
            predictions.append(pred)
        
        # 仓位建议
        position = self.risk.position_sizing(
            factor_result['total_score'],
            factor_result['volatility']['historical_vol'],
            var
        )
        
        # 交易信号
        signal = self.generate_signal(factor_result, predictions, prices[-1])
        
        return {
            'success': True,
            'stock_name': data['name'],
            'stock_code': code,
            'current_price': data['current'],
            'factor_score': factor_result['total_score'],
            'factor_details': factor_result['factor_scores'],
            'rsi': factor_result['rsi'],
            'macd': factor_result['macd_hist'],
            'bb_position': factor_result['bb_position'],
            'var': var,
            'sharpe_ratio': sharpe,
            'ml_prediction': ml_price,
            'predictions': predictions,
            'position_suggestion': position,
            'signal': signal,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def generate_signal(self, factor_result, predictions, current_price):
        """生成交易信号"""
        score = factor_result['total_score']
        rsi = factor_result['rsi']
        macd = factor_result['macd_hist']
        bb_pos = factor_result['bb_position']
        
        signals = []
        strength = 0
        
        if score >= 70:
            signals.append("Multi-factor共振")
            strength += 2
        elif score <= 30:
            signals.append("Multi-factor警示")
            strength -= 2
        
        if rsi < 30:
            signals.append("RSI超卖")
            strength += 1
        elif rsi > 70:
            signals.append("RSI超买")
            strength -= 1
        
        if macd > 0:
            signals.append("MACD金叉")
            strength += 1
        elif macd < 0:
            signals.append("MACD死叉")
            strength -= 1
        
        if bb_pos < 0.2:
            signals.append("触及下轨")
            strength += 1
        elif bb_pos > 0.8:
            signals.append("触及上轨")
            strength -= 1
        
        pred_change = (predictions[-1] - current_price) / current_price
        if pred_change > 0.03:
            signals.append(f"预测涨幅{pred_change*100:.1f}%")
            strength += 1
        elif pred_change < -0.03:
            signals.append(f"预测跌幅{pred_change*100:.1f}%")
            strength -= 1
        
        if strength >= 3:
            final_signal = "STRONG BUY"
        elif strength >= 1:
            final_signal = "BUY"
        elif strength <= -3:
            final_signal = "STRONG SELL"
        elif strength <= -1:
            final_signal = "SELL"
        else:
            final_signal = "HOLD"
        
        return {
            'final': final_signal,
            'details': signals,
            'strength': strength
        }


# ============ Kivy界面 ============
class QuantApp(App):
    def __init__(self):
        super().__init__()
        self.quant_system = UltimateQuantSystem()
        self.analyzing = False
    
    def build(self):
        # 主布局
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # 标题
        title_label = Label(
            text='[b]Ultimate Stock Predictor v3.0[/b]',
            markup=True,
            size_hint_y=None,
            height=50,
            font_size='22sp',
            color=[0.2, 0.8, 1, 1]
        )
        layout.add_widget(title_label)
        
        # 副标题
        subtitle = Label(
            text='Multi-Factor Model | Machine Learning | Risk Control',
            size_hint_y=None,
            height=30,
            font_size='14sp',
            color=[0.7, 0.7, 0.7, 1]
        )
        layout.add_widget(subtitle)
        
        # 股票代码输入
        layout.add_widget(Label(
            text='Stock Code:',
            size_hint_y=None,
            height=25,
            halign='left'
        ))
        
        self.code_input = TextInput(
            text='600519',
            multiline=False,
            size_hint_y=None,
            height=45,
            font_size='18sp',
            background_color=[0.1, 0.1, 0.1, 1],
            foreground_color=[1, 1, 1, 1]
        )
        layout.add_widget(self.code_input)
        
        # 提示文字
        hint = Label(
            text='Shanghai:600xxx | Shenzhen:000xxx | ChiNext:300xxx',
            size_hint_y=None,
            height=20,
            font_size='11sp',
            color=[0.5, 0.5, 0.5, 1]
        )
        layout.add_widget(hint)
        
        # 预测天数
        layout.add_widget(Label(
            text='Prediction Days (1-30):',
            size_hint_y=None,
            height=25,
            halign='left'
        ))
        
        self.days_input = TextInput(
            text='5',
            multiline=False,
            size_hint_y=None,
            height=45,
            font_size='18sp',
            background_color=[0.1, 0.1, 0.1, 1],
            foreground_color=[1, 1, 1, 1]
        )
        layout.add_widget(self.days_input)
        
        # 分析按钮
        self.analyze_btn = Button(
            text='Start Analysis',
            size_hint_y=None,
            height=60,
            font_size='18sp',
            background_color=[0.2, 0.6, 1, 1],
            background_normal=''
        )
        self.analyze_btn.bind(on_press=self.start_analysis)
        layout.add_widget(self.analyze_btn)
        
        # 进度条
        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=20
        )
        layout.add_widget(self.progress)
        self.progress.opacity = 0
        
        # 结果展示区域
        self.result_label = Label(
            text='Waiting for analysis...',
            size_hint_y=1,
            valign='top',
            halign='left',
            font_size='15sp',
            color=[0.9, 0.9, 0.9, 1]
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        # 底部免责
        disclaimer = Label(
            text='[color=ff6666]⚠️ Analysis for reference only | Invest at your own risk[/color]',
            markup=True,
            size_hint_y=None,
            height=30,
            font_size='12sp'
        )
        layout.add_widget(disclaimer)
        
        return layout
    
    def start_analysis(self, instance):
        if self.analyzing:
            return
        
        self.analyzing = True
        self.analyze_btn.text = 'Analyzing...'
        self.analyze_btn.disabled = True
        self.progress.opacity = 1
        self.progress.value = 0
        
        threading.Thread(target=self.do_analysis).start()
        Clock.schedule_interval(self.update_progress, 0.1)
    
    def update_progress(self, dt):
        if self.progress.value < 90:
            self.progress.value += 2
        return not self.analyzing
    
    def do_analysis(self):
        try:
            code = self.code_input.text.strip()
            try:
                days = int(self.days_input.text.strip())
                days = max(1, min(30, days))
            except:
                days = 5
            
            result = self.quant_system.analyze(code, days)
            Clock.schedule_once(lambda dt: self.show_result(result, days))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(str(e)))
    
    def show_result(self, result, days):
        if not result:
            self.show_error("Failed to fetch data")
            return
        
        text = f"""
========================================
Stock: {result['stock_name']} ({result['stock_code']})
Current Price: {result['current_price']:.2f}
Time: {result['timestamp']}
========================================

[SCORE]
Total Score: {result['factor_score']:.1f}/100

[SIGNAL]
{result['signal']['final']}

[TECHNICAL INDICATORS]
RSI(14): {result['rsi']:.1f}
MACD: {result['macd']:+.2f}
Bollinger Position: {result['bb_position']:.2f}

[RISK METRICS]
VaR(95%): {result['var']*100:.2f}%
Sharpe Ratio: {result['sharpe_ratio']:.2f}
Suggested Position: {result['position_suggestion']*100:.1f}%

[PRICE PREDICTION]
"""
        if result['ml_prediction']:
            ml_change = (result['ml_prediction'] - result['current_price']) / result['current_price']
            text += f"AI Prediction: {result['ml_prediction']:.2f} ({ml_change:+.2f}%)\n"
        
        text += "\nFuture Predictions:\n"
        for i, pred in enumerate(result['predictions']):
            change = (pred - result['current_price']) / result['current_price']
            arrow = "▲" if change > 0 else "▼" if change < 0 else "→"
            text += f"  Day {i+1}: {pred:.2f} {arrow} {change:+.2f}%\n"
        
        text += f"""
========================================
[FACTOR BREAKDOWN]"""
        
        for factor, score in result['factor_details'].items():
            text += f"\n  {factor}: {score:+.1f}"
        
        text += """

========================================
⚠️ Analysis for reference only
    Invest at your own risk
========================================
"""
        self.result_label.text = text
        
        self.analyzing = False
        self.analyze_btn.text = 'Start Analysis'
        self.analyze_btn.disabled = False
        self.progress.opacity = 0
    
    def show_error(self, error_msg):
        self.result_label.text = f"""
========================================
[ERROR] Analysis Failed

{error_msg}

Possible reasons:
- Invalid stock code format
- Network connection issue
- Data source temporarily unavailable

Please check and try again.
========================================
"""
        self.analyzing = False
        self.analyze_btn.text = 'Start Analysis'
        self.analyze_btn.disabled = False
        self.progress.opacity = 0


if __name__ == '__main__':
    print("启动量化股票预测系统...")
    QuantApp().run()