
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        
        self.add_widget(Label(text="User:"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        
        self.add_widget(Label(text="Password:"))
        self.password = TextInput(
                multiline=False, password=True)
        self.add_widget(self.password)
        
class MyClass(App):
    def build(self):
        return LoginScreen()
        # return Button(text="mine")

if __name__ == "__main__":
    MyClass().run()
