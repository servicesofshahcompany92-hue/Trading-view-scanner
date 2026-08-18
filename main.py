import pandas as pd
import random
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

class SignalScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        
        # Header Label
        self.title_label = Label(
            text="TRADINGVIEW RSI + EMA SCANNER",
            font_size='18sp',
            bold=True,
            size_hint_y=0.15
        )
        self.add_widget(self.title_label)
        
        # Signal Output Box
        self.signal_label = Label(
            text="INITIALIZING SCANNER...",
            font_size='22sp',
            bold=True,
            size_hint_y=0.45
        )
        self.add_widget(self.signal_label)
        
        # Stats Output
        self.stats_label = Label(
            text="RSI: -- | EMA 9: -- | EMA 21: --",
            font_size='14sp',
            size_hint_y=0.2
        )
        self.add_widget(self.stats_label)
        
        # Scan Button
        self.scan_btn = Button(
            text="MANUAL REFRESH",
            font_size='16sp',
            bold=True,
            size_hint_y=0.2,
            background_color=(0.1, 0.5, 0.9, 1)
        )
        self.scan_btn.bind(on_press=self.manual_scan)
        self.add_widget(self.scan_btn)
        
        self.prices = []
        Clock.schedule_interval(self.update_analysis, 3)

    def update_analysis(self, dt):
        # Data Stream Simulation
        new_price = 1.0850 + random.uniform(-0.0025, 0.0025)
        self.prices.append(new_price)
        if len(self.prices) > 60:
            self.prices.pop(0)
            
        if len(self.prices) < 25:
            self.signal_label.text = f"Building Price Buffer... ({len(self.prices)}/25)"
            return

        df = pd.DataFrame({'close': self.prices})
        df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()
        df['ema_fast'] = EMAIndicator(close=df['close'], window=9).ema_indicator()
        df['ema_slow'] = EMAIndicator(close=df['close'], window=21).ema_indicator()
        
        rsi_val = df['rsi'].iloc[-1]
        ema_f = df['ema_fast'].iloc[-1]
        ema_s = df['ema_slow'].iloc[-1]
        
        self.stats_label.text = f"RSI: {rsi_val:.1f} | EMA9: {ema_f:.4f} | EMA21: {ema_s:.4f}"
        
        # Confluence Signals
        if rsi_val < 35 and ema_f > ema_s:
            self.signal_label.text = "CALL (BUY) CONFIRMED"
            self.signal_label.color = (0, 1, 0, 1)
        elif rsi_val > 65 and ema_f < ema_s:
            self.signal_label.text = "PUT (SELL) CONFIRMED"
            self.signal_label.color = (1, 0, 0, 1)
        else:
            self.signal_label.text = "WAITING FOR CONFLUENCE..."
            self.signal_label.color = (0.7, 0.7, 0.7, 1)

    def manual_scan(self, instance):
        self.update_analysis(0)

class TradingApp(App):
    def build(self):
        return SignalScreen()

if __name__ == '__main__':
    TradingApp().run()
