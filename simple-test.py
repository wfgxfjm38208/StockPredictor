from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class SimpleApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        label = Label(text='Stock Predictor Test')
        layout.add_widget(label)
        
        code_input = TextInput(text='600519', multiline=False)
        layout.add_widget(code_input)
        
        btn = Button(text='Predict')
        layout.add_widget(btn)
        
        result = Label(text='Result will show here')
        layout.add_widget(result)
        
        def on_press(instance):
            result.text = f'Predicting {code_input.text}...'
        
        btn.bind(on_press=on_press)
        
        return layout

if __name__ == '__main__':
    SimpleApp().run()