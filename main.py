# This qivy app include 3 levels of difficulty and offers to solve
# arithmetic tasks. It has timer, which shows your time executing.
# Beside it has a tab with best results on every level and scroll-tab
# with total results and date executing.


import os, sys
from kivy.resources import resource_add_path, resource_find
from kivy.config import Config
Config.set('graphics', 'resizable', 0)
Config.set("graphics", "width", 500)
Config.set("graphics", "height", 670)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from kivy.clock import Clock
from kivy.properties import NumericProperty
import random
from datetime import date

Window.clearcolor = [0, 1, 1, 1]


def math_light():
    string, space, sign = '-1', ' ', ''
    while eval(string) not in range(0, 21):
        a, b, sign = random.randint(0, 20), random.randint(0, 20), random.choice(['+', '-'])
        string = str(a) + sign + str(b)
    if len(str(a)) == 2:
        if len(str(b)) == 2:
            string = str(a) + space*2 + sign + space*2 + str(b) + ' = '
        if len(str(b)) == 1:
            string = str(a) + space*2 + sign + space * 2 + str(b) + '   = '
    if len(str(a)) == 1:
        if len(str(b)) == 2:
            string = str(a) + space * 3 + sign + space * 2 + str(b) + '  = '
        if len(str(b)) == 1:
            string = str(a) + space * 3 + sign + space * 3 + str(b) + '   = '
    return string


def math_middle():
    string = '-1'
    while eval(string) not in range(0, 200):
        string = f"{random.randint(10, 99)}  {random.choice(['+','-'])}  {random.randint(10, 99)} "
    return string + ' ='


def math_hard():
    string = '-1'
    while eval(string) < 0:
        string = f"{random.randint(100, 999)} {random.choice(['+','-'])} {random.randint(100, 999)}"
    return string + ' ='


class MainApp(App):
    examples, decisions, images = {}, {}, {}
    time, lev = 0, 1

    def build(self):
        fl = FloatLayout(size=(500, 670))
        dropdown = DropDown()
        self.mainbutton = Button(text='МЕНЮ', size_hint=(1, 0.06), pos_hint={"left": 1, "top": 1},
                                 background_color=[0, 8/255, 128/255, .6], background_normal='yellow')
        self.mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=self.on_select_dropdown)
        fl.add_widget(self.mainbutton)
        self.gl = GridLayout(cols=3, padding=[60, 30, 30, 30], spacing=15)
        self.buildup(self.gl)
        fl.add_widget(self.gl)
        return fl

    def build_popup(self):
        box = BoxLayout()
        box.add_widget(Label(text='УРОВЕНЬ 1:' + ' ' * 35 + f'{self.read_records()[0]} \n'
                                  + ' ' * 56 + f'{self.read_records()[1]}'))
        btn_call_light_res = Button(text=f'все результаты', font_size=16, height=20, width=130,
                                    background_color=(192, 192, 192, 1), size_hint_x=None,
                                    pos_hint={'right': 1}, color='black', outline_width=.1)
        btn_call_light_res.id = '1'
        btn_call_light_res.bind(on_press=self.read_results_light)
        box.add_widget(btn_call_light_res)
        box.add_widget(Label(text='УРОВЕНЬ 2:' + ' ' * 35 + f'{self.read_records()[2]} \n'
                                  + ' ' * 56 + f'{self.read_records()[3]}'))
        btn_call_middle_res = Button(text=f'все результаты', font_size=16, height=20, width=130,
                                     background_color=(192, 192, 192, 1), size_hint_x=None,
                                     pos_hint={'right': 1}, color='black', outline_width=.1)
        btn_call_middle_res.id = '2'
        btn_call_middle_res.bind(on_press=self.read_results_light)
        box.add_widget(btn_call_middle_res)
        box.add_widget(Label(text='УРОВЕНЬ 3:' + ' ' * 35 + f'{self.read_records()[4]} \n'
                                  + ' ' * 56 + f'{self.read_records()[5]}'))
        btn_call_difficult_res = Button(text=f'все результаты', font_size=16, height=20, width=130,
                                        background_color=(192, 192, 192, 1), size_hint_x=None,
                                        pos_hint={'right': 1}, color='black', outline_width=.1)
        btn_call_difficult_res.id = '3'
        btn_call_difficult_res.bind(on_press=self.read_results_light)
        box.add_widget(btn_call_difficult_res)
        but = Button(text='OK', size_hint_x=None, width='80', pos_hint={'left': 1}, height=30,
                     background_color=(192, 192, 192, 1), color='black', outline_width=.8)
        box.add_widget(but)
        popup = Popup(title='Ваши рекорды', content=box, size_hint=(None, None),
                      size=(400, 600), auto_dismiss=False)
        but.bind(on_release=popup.dismiss)
        return popup

    def read_results_light(self, instance):
        file = 'result_light.txt'
        gl = GridLayout(cols=1, spacing=25, size_hint_y=None)
        gl.bind(minimum_height=gl.setter('height'))
        if instance.id == '2':
            file = 'result_middle.txt'
        elif instance.id == '3':
            file = 'result_hard.txt'
        with open(file, 'r') as f:
            for line in f.readlines():
                gl.add_widget(Label(text=line))
        root = FloatLayout(size=(500, 670))
        scrv = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * .7), bar_margin=15,
                          pos_hint={'center_x': 0.5, 'center_y': 0.55},
                          bar_width=5, bar_color='white', scroll_type=['content', 'bars'])
        scrv.add_widget(gl)
        root.add_widget(scrv)
        btn = Button(pos_hint={'center_x': 0.5, 'center_y': 0}, text='OK', width='80', height=30,
                     background_color=(192, 192, 192, 1), color='black', outline_width=.8)
        root.add_widget(btn)
        popup = Popup(title=f'УРОВЕНЬ {instance.id}', title_size='24sp', title_align='center', content=root,
                      background_color='black', size_hint=(None, None), size=(400, 600), separator_color='white',
                      auto_dismiss=False)
        btn.bind(on_press=popup.dismiss)
        return popup.open()

    def read_records(self):
        with open('records.txt', 'r') as records:
            data = records.readlines()
        return data

    def buildup(self, layout):
        for i in range(3):
            layout.add_widget(Label(text=''))
        for i in range(10):
            answer = MyTextInput()
            answer.bind(text=self.on_text)
            label = Label(text=self.level(self.lev),
                          halign='left',
                          size_hint_x=None,
                          width=130,
                          font_size=30,
                          bold='True',
                          color=[1, 0, 0, 1],
                          outline_color=[0, 0, 0],
                          outline_width=1.5,
                          )
            img = Image(source='./empty.png', size_hint=(1, .1))
            self.examples[answer] = label.text
            self.decisions[answer] = -1
            self.images[answer] = img
            layout.add_widget(label)
            layout.add_widget(answer)
            layout.add_widget(img)
        self.lbl = Label(text='00:00', color=[1, 1, 1, 1], font_size=30, bold=True, outline_width=1.5)
        layout.add_widget(self.lbl)
        layout.add_widget(Label(text=''))
        btn = Button(on_release=self.on_release_button)
        layout.add_widget(btn)
        self.event = Clock.schedule_interval(self.my_callback, 1)

    def on_text(self, value, any):
        self.decisions[value] = value.text

    def on_release_button(self, instance):
        count = 0
        if instance.text == 'Еще раз?':
            self.examples, self.decisions, self.images = {}, {}, {}
            self.time = 0
            self.gl.clear_widgets()
            self.buildup(self.gl)
        else:
            for key, val in self.examples.items():
                if eval(' '.join(self.examples[key].split()[:-1])) == int(self.decisions[key]):
                    count += 1
                    self.images[key].source = 'tick.png'
                else:
                    self.images[key].source = 'cross.png'
            if count == 10:
                Clock.unschedule(self.event)
                with open('records.txt', 'r') as f:
                    list_records = [string for string in f.readlines()]
                if self.lev == 1:
                    file, num = 'result_light.txt', 0
                elif self.lev == 2:
                    file, num = 'result_middle.txt', 2
                elif self.lev == 3:
                    file, num = 'result_hard.txt', 4
                with open(file, 'a') as f:
                    f.write(f'{date.today().strftime("%d.%m.%y")}  -->  результат: {self.lbl.text}\n')
                    if list_records[num][-2] == '_' or float(self.lbl.text[:2] + '.' + self.lbl.text[3:]) \
                            < float(list_records[num + 1][7:9] + '.' + list_records[num + 1][10:]):
                        list_records[num] = f'Дата {date.today().strftime("%d.%m.%y")}\n'
                        list_records[num + 1] = f'время: {self.lbl.text}\n'
                with open('records.txt', 'w') as f:
                    for line in list_records:
                        f.write(line)
                self.build_popup()
                instance.text = 'Еще раз?'

    def my_callback(self, dt):
        y = self.time // 60
        x = self.time % 60
        if x < 10 and y < 10:
            self.lbl.text = f'0{y}:0{x}'
        elif x >= 10 and y < 10:
            self.lbl.text = f'0{y}:{x}'
        elif x < 10 and y >= 10:
            self.lbl.text = f'{y}:0{x}'
        elif x >= 10 and y >= 10:
            self.lbl.text = f'{y}:{x}'
        self.time += 1

    def on_select_dropdown(self, instance, x):
        word = self.mainbutton.text
        setattr(self.mainbutton, 'text', x)
        if self.mainbutton.text == 'РЕЗУЛЬТАТЫ':
            self.build_popup().open()
            self.mainbutton.text = word
        else:
            self.select_drop(self.mainbutton.text)

    def select_drop(self, text):
        self.lev = int(text[0])
        Clock.unschedule(self.event)
        self.examples, self.decisions = {}, {}
        self.time, self.images = 0, {}
        self.gl.clear_widgets()
        self.buildup(self.gl)

    def level(self, lev):
        if lev == 1:
            return math_light()
        elif lev == 2:
            return math_middle()
        elif lev == 3:
            return math_hard()
        else:
            pass


class MyTextInput(TextInput):
    max_characters = NumericProperty(0)

    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters > 0:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()

