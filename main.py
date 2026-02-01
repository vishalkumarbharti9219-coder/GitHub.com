from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivmob import KivMob

class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'dashboard'), 3)

class Dashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ads = KivMob("ca-app-pub-8074757676015270~4303323348")
        self.ads.add_rewarded_video_ad("ca-app-pub-8074757676015270/1129540687")
        self.store = JsonStore('wallet.json')
        if not self.store.exists('u'): self.store.put('u', bal=0.0)
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.lbl = Label(text=f"Wallet: INR {self.store.get('u')['bal']:.2f}", font_size='32sp', color=(0,1,0.5,1))
        layout.add_widget(self.lbl)
        
        btns = [("📺 Watch Ad & Earn", (0,0.6,1,1), self.earn), ("🔗 Share", (0.1,0.8,0.1,1), self.share), ("💸 Withdraw", (1,0.2,0.2,1), self.withdraw)]
        for txt, clr, func in btns:
            b = Button(text=txt, background_color=clr, size_hint=(1,0.2))
            b.bind(on_release=func)
            layout.add_widget(b)
        self.add_widget(layout)

    def earn(self, *args):
        self.ads.show_rewarded_video_ad()
        new = round(self.store.get('u')['bal'] + 0.50, 2)
        self.store.put('u', bal=new)
        self.lbl.text = f"Wallet: INR {new:.2f}"
    def share(self, *args): print("Share Clicked")
    def withdraw(self, *args): print("Withdraw Clicked")

class MasterApp(App):
    def build(self):
        sm = ScreenManager()
        sc = Screen(name='welcome'); sc.add_widget(Label(text="WELCOME\nMASTER EARN", font_size='40sp', halign='center'))
        sm.add_widget(sc); sm.add_widget(Dashboard(name='dashboard'))
        return sm

if __name__ == "__main__":
    MasterApp().run()
