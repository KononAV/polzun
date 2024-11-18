import copy
from random import randint, choice
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from functools import partial
import time
import os
import re


class Snake:
    __slots__ = 'id', 'vector', 'd', 'count', '_length', 'x', 'y'
    _id = 0

    def __init__(self):
        self.id = self._generate_id_()
        self.vector = 'x'
        self.d = []
        self.count = 0

        self._length = [self.id]
        self.x = 0
        self.y = 0

    @classmethod
    def _generate_id_(cls):
        cls._id+=1
        return cls._id

    def add_length(self):
        self._length.append(self.id)


    def show_length(self):
        return self._length




class Apple:
    __slots__ = 'coords', 'x', 'y'


    def __init__(self):
        self.coords = []
        self.x = 0
        self.y = 0

    def set_apple(self,d, lst):
        self.set_coords(lst[1], lst[2])
        if (self.x, self.y) not in d and (self.x, self.y) not in self.coords:
            lst[0][self.x][self.y] = 8
            self.coords.append((self.x, self.y))

        else:
            self.set_apple(d, lst)

    def set_coords(self, sizey, sizex):
        self.x = randint(0,sizey-1)
        self.y = randint(0,sizex-1)


class Bush:
    __slots__ = 'coords', 'x', 'y'


    def __init__(self):
        self.coords = []
        self.x = 0
        self.y = 0

    def set_bush(self, lst):
        self.x = randint(0,lst[1]-1)
        self.y = randint(0,lst[2]-1)

        lst[0][self.x][self.y] = '7'
        self.coords.append((self.x,self.y))




class Pole:

    __slots__ = 'sizex', 'sizey', 'x', 'y', '_pole', \
    'apple_gen', 'sleep', 'bushcount', 'bushenemy', 'snakeenemy', \
    'forobjects', 'apple', 'bush', 'snake', 'snakes', 'snake2', 'snakefriend'


    def __init__(self,x,y, bushenemy, snakeenemy, snakefriend=True):
        self.sizex = x
        self.sizey = y
        self.x = self.sizey
        self.y = self.sizex
        self._pole = [[0 for _ in range(self.sizex)]for _ in range(self.sizey)]


        self.apple_gen = 0
        self.sleep = 0.1
        self.bushcount = 0

        self.bushenemy = bushenemy
        self.snakeenemy = snakeenemy
        self.snakefriend = snakefriend
        self.forobjects = [self._pole, self.sizey, self.sizex]


        self.apple = Apple()
        self.bush = Bush()
        Snake._id=0
        self.snakes=[]
        if snakefriend:
            self.snake = Snake()
            self.snakes.append(self.snake)
        if self.snakeenemy:
            self.snake2 = Snake()
            for i in range(2):
                self.snake2.add_length()
            self.snake2.x = randint(0,self.x-1)
            self.snake2.y = randint(0,self.y-1)
            self.snakes.append(self.snake2)

        if self.bushenemy:
            while len(self.bush.coords)!=(self.sizex+self.sizey)//2:
                self.bush.set_bush(self.forobjects)

    @staticmethod
    def set_vector_script(i):
        match (i.vector):
            case 'x':
                i.x += 1
                return 1
            case 'y':
                i.y -= 1
                return -1
            case 'x0':
                i.x -= 1
                return -1
            case 'y0':
                i.y += 1
                return 1

    @staticmethod
    def check_decorator(func):
        def wrapper2(arg, *kwargs):
            f = arg
            func(arg, *kwargs)
            if f.snakefriend:
                if len(set(f.snake.d)) != len(f.snake.d) or f.snake.x<0 or f.snake.y<0 \
                        or (f.snake.d[-1][0],f.snake.d[-1][1]) in (f.snake2.d if f.snakeenemy else [])\
                        or (f.snake.d[-1][0],f.snake.d[-1][1]) in (f.bush.coords if f.bushenemy else []) \
                        :
                    raise IndexError
        return wrapper2

    @staticmethod
    def check_pc_decorator(func):
        def wrapper1(arg, *kwargs):
            f = arg
            try:
                func(arg, *kwargs)
            except RecursionError:
                f.snakes.remove(f.snake2)
                return 0
        return wrapper1

    @check_decorator
    def init_pole(self):
        self.set_vector()
        self.put_apple()

        for i in self.snakes:
            self.gen_apple_script(i.d, self.forobjects)
            self._pole[i.x][i.y] = i.show_length()[0]

            i.d.append((i.x, i.y))

            self._pole[i.d[0][0]][i.d[0][1]] = 0

            if i.count == (len(i.show_length())):
                i.d.remove(i.d[0])

            else:
                i.count+=1

    def show_pole(self):
        self.init_pole()
        show = ''
        for i in self._pole:
            show += ' '.join(map(lambda x: str(x), i))
            show += '\n'

        return show


    def gen_apple_script(self,d, forobjects):
        if self.apple_gen%100==0:

            self.sleep = 0.00001
            self.apple.set_apple(d,forobjects)
        if self.apple_gen%50==0:
            self.sleep = 0.0005

            self.apple.set_apple(d,forobjects)
        if self.apple_gen%10==0:
            self.sleep = 0.005
            self.apple.set_apple(d,forobjects)

    def put_apple(self):
        for i in self.snakes:
            if (i.x, i.y) in self.apple.coords:
                i.add_length()
                self.apple.coords.remove((i.x, i.y))

    @check_pc_decorator
    def set_pc_coords(self):
        lst = ['x', 'y', 'x0', 'y0']
        oldchois = self.snake2.vector
        newchois = choice(lst)

        shadowsnake = copy.deepcopy(self.snake2)

        shadowsnake.vector = newchois
        self.set_vector_script(shadowsnake)
        shadowsnake.d.append((shadowsnake.x, shadowsnake.y))

        if (newchois[0] == oldchois[0] and len(newchois) != len(oldchois)) \
                or 0>shadowsnake.x or shadowsnake.x>=self.sizey \
                or 0>shadowsnake.y or shadowsnake.y>=self.sizex \
                or len(set(shadowsnake.d))!=len(shadowsnake.d) \
                or (shadowsnake.d[-1][0], shadowsnake.d[-1][1]) in (self.bush.coords if self.bushenemy else [])\
                or (shadowsnake.d[-1][0], shadowsnake.d[-1][1]) in (self.snake.d if self.snakefriend else [])\
                :


            return self.set_pc_coords()
        else:
            self.snake2.vector = newchois

    def set_vector(self):

        time.sleep(self.sleep)
        self.apple_gen+=1
        if self.snakeenemy:
            if self.snake2 in self.snakes:
                self.set_pc_coords()
        for i in self.snakes:
            self.set_vector_script(i)


class Window:
    __slots__ = 'root', 'style',


    def __init__(self):
        self.root = Tk()
        self.root.iconbitmap(default="favicon_(3).ico")
        self.root["bg"] = "black"
        self.root.resizable(False, False)
        self.style = ttk.Style()
        self.style.configure("My.TLabel", background='black', foreground='green')
        if self.__class__!=MenuWindow:
            self.verch(self.root)


    def verch(self, root):
        main_menu = Menu(root, tearoff=0)
        main_menu.add_cascade(label="leading", command=self.leading)
        if self.__class__ == StartWindow:
            main_menu.add_cascade(label="reset", command=self.reset)
            main_menu.add_cascade(label = 'settings', command=self.settings)
        main_menu.add_cascade(label="exit", command=self.exit)

        root.config(menu=main_menu)

    def leading(self):
        root = Tk()
        root.title("Polzun")
        root.geometry('300x350')
        root.resizable(False, False)
        root["bg"] = "black"

        leading =  open('leading.txt', 'r')

        label = ttk.Label(root, text=leading.read(), background='black', foreground='green')
        label.place(x=0, y =0)

        self.start()

    def exit(self):
        self.root.destroy()

    def reset(self):
        for after_id in self.root.tk.eval('after info').split():
            self.root.after_cancel(after_id)
        self.root.destroy()

        Snake._id = 0
        StartWindow(self.pole.sizex, self.pole.sizey,  self.pole.bushenemy, self.pole.snakeenemy)

    def settings(self):
        for after_id in self.root.tk.eval('after info').split():
            self.root.after_cancel(after_id)
        self.root.destroy()

        Snake._id = 0
        SettingWindow()

    def start_window(self):
        pass

    def start(self):
        self.root.mainloop()


class MenuWindow(Window):
    def __init__(self):
        super().__init__()
        self.pole1 = Pole(20,13, False, True, False)
        for i in range(5):
            self.pole1.snake2.add_length()
        self.start_window()
        self.start()

    def start_window(self):
        self.root.title("Polzun")
        self.root.geometry('600x300')
        self.pole1.show_pole()


        lab0 = ttk.Label(style='My.TLabel')
        lab0.place(x=416, y=100)

        def labelcomfig():
            lab0.config(text=self.pole1.show_pole())
            self.after_id = self.root.after(900, labelcomfig)
        labelcomfig()

        but = Button(self.root, width=40, text= '''█▀▀ ▀▀█▀▀ █▀▀█ █▀▀█ ▀▀█▀▀ 
▀▀█ ░░█░░ █▄▄█ █▄▄▀ ░░█░░ 
▀▀▀ ░░▀░░ ▀░░▀ ▀░▀▀ ░░▀░░''',
                          background ='black',foreground = 'green',activebackground='green1', activeforeground='black',
                          cursor = 'hand2', command = self.click)
        but.place(x=170, y=200)
        text = \
       ['''██████╗░░█████╗░██╗░░░░░███████╗██╗░░░██╗███╗░░██╗''',
        '''██╔══██╗██╔══██╗██║░░░░░╚════██║██║░░░██║████╗░██║''',
        '''██████╔╝██║░░██║██║░░░░░░░███╔═╝██║░░░██║██╔██╗██║''',
        '''██╔═══╝░██║░░██║██║░░░░░██╔══╝░░██║░░░██║██║╚████║''',
        '''██║░░░░░╚█████╔╝███████╗███████╗╚██████╔╝██║░╚███║''',
        '''╚═╝░░░░░░╚════╝░╚══════╝╚══════╝░╚═════╝░╚═╝░░╚══╝''',
        '''▀▀█▀▀ █░░█ █▀▀ 　 █▀▀ █▀▀▄ █▀▀█ █░█ █▀▀''',
        '''░░█░░ █▀▀█ █▀▀ 　 ▀▀█ █░░█ █▄▄█ █▀▄ █▀▀''',
        '''░░▀░░ ▀░░▀ ▀▀▀ 　 ▀▀▀ ▀░░▀ ▀░░▀ ▀░▀ ▀▀▀''']



        dlabel = {}
        for i in range(len(text)):
            dlabel[f'{i}'] = ttk.Label(text = text[i], style="My.TLabel")
            if i<6:
                dlabel.get(f'{i}').place(x=0, y=i*17)
            else:
                dlabel.get(f'{i}').place(x=5, y=5+i * 17)

        c = 0
        def labeconfig():
            nonlocal dlabel, c
            if c<10:
                try:
                    dlabel[f'{c}'].config(foreground = 'green1')
                    dlabel[f'{c+1}'].config(foreground='green1')
                except (AttributeError,KeyError):
                    pass
                try:
                    dlabel.get(f'{c-1}').config(foreground='green')
                    dlabel.get(f'{c - 2}').config(foreground='green')
                except (AttributeError, KeyError):
                    pass
                c+=1
            else:
                c=0
            self.root.after(80, labeconfig)
        labeconfig()

        lab4 = ttk.Label(text='v0.0.1', style="My.TLabel")
        lab4.place(x=1,y=280)



    def click(self):
        for self.after_id in self.root.tk.eval('after info').split():
            self.root.after_cancel(self.after_id)
        self.root.destroy()
        setting = SettingWindow()


class SettingWindow(Window):
    __slots__ = 'bush', 'bush', 'snakeenemy', 'x', 'y'


    def __init__(self):
        super().__init__()
        self.bush = False
        self.snakeenemy = False
        self.x = 10
        self.y = 10
        self.start_window()
        self.start()

    def start_window(self):
        self.root.title("Polzun_settings")
        self.root.geometry('300x290')


        enabledbush, enabledsnake = BooleanVar(), BooleanVar()
        scalemapx = IntVar()
        scalemapy = IntVar()


        mode_label = ttk.Label(self.root, text='>>choose mode', style="My.TLabel")
        mode_label.place(x=10,y=10)

        snakebutton = Checkbutton(text='enemy snake', background = 'black', foreground='green',
                                 activebackground= 'black', activeforeground='green1',selectcolor='black',
                                 variable= enabledsnake, command=partial(self.select_checkbutton, self.snakeenemy, enabledsnake, 0))
        snakebutton.place(x = 10, y=30)

        snake_label = ttk.Label(text='-----  <add pc opponent>', style='My.TLabel')
        snake_label.place(x = 108, y=34)

        bushbutton = Checkbutton(text='bushes', background='black', foreground='green',
                                 activebackground='black', activeforeground='green1', selectcolor='black',
                                 variable=enabledbush, command=partial(self.select_checkbutton, self.bush, enabledbush, 1))

        bushbutton.place(x=10, y=50)

        bush_label = ttk.Label(text='-----  <add barriers>', style='My.TLabel')
        bush_label.place(x=75, y=54)

        pole_label = ttk.Label(self.root, text='>>choose pole size', style="My.TLabel")
        pole_label.place(x=10, y=90)


        scalex = Scale(self.root, orient=VERTICAL, length=100, from_=10, to=30.0,
                      background='black', foreground='green', activebackground='black', highlightthickness=0,
                      troughcolor='black', highlightbackground='black', highlightcolor='black', variable=scalemapx,
                      command=partial(self.select_scale, 0))
        scalex.place(x = 10, y=120 )

        label_scalex = ttk.Label(text='x', style="My.TLabel")
        label_scalex.place(x= 30, y=225)

        scaley = Scale(self.root, orient=VERTICAL, length=100, from_=10, to=30.0,
                       background='black', foreground='green', activebackground='black', highlightthickness=0,
                       troughcolor='black', highlightbackground='black', highlightcolor='black', variable=scalemapy,
                       command=partial(self.select_scale, 1))
        scaley.place(x=65, y=120)

        label_scaley = ttk.Label(text='y', style="My.TLabel")
        label_scaley.place(x=85, y=223)

        press_label = ttk.Label(text=r'''press start after settings
           \/\/\/\/\/\/''', style="My.TLabel")


        press_label.place(x= 150,y = 210)



        final_label = ttk.Label(text='-----------------------------------------------------------------', style="My.TLabel")
        final_label.place(x = 1, y=250)

        complitebutton = Button(self.root, text='-start-', width=4, background='black', foreground='green', \
                            borderwidth=0, activebackground='black', activeforeground='black', command=self.click)
        complitebutton.place(x = 198, y=249)




    def select_checkbutton(self, arg, karg, num):
        if num:
            self.bush = bool(karg.get())

            return 0
        self.snakeenemy = bool(karg.get())

    def select_scale(self, num, k):
        if num:
            self.y = int(k)
            return 0
        self.x = int(k)


    def click(self):
        self.root.destroy()
        StartWindow(self.x, self.y, self.bush, self.snakeenemy)


class StartWindow(Window):
    __slots__ = 'pole', 'after_id', 'shadow'


    def __init__(self, x, y, bush, enemy):

        super().__init__()
        self.pole = Pole(x, y, bush, enemy)
        self.after_id = None
        self.shadow = None
        self.start_window()
        self.start()

    @staticmethod
    def check_window(func):
        def wrapper3():
            try:
                func()

            except UnboundLocalError:
                return 0
        return wrapper3


    def start_window(self):
        self.root.title("Polzun")

        self.root.geometry(f'{self.pole.sizex*(19 if self.pole.sizex in (10,11,12,13,14, 15) else 16)}x{self.pole.sizey*17}')

        def pr(press, key):
            match(press):
                case 'w':
                    self.pole.snake.vector = 'x0'
                case 's':
                    self.pole.snake.vector = 'x'
                case 'a':
                    self.pole.snake.vector = 'y'
                case 'd':
                    self.pole.snake.vector = 'y0'

        ent = ttk.Entry(self.root,width=9)

        ent.bind_all('<KeyPress-w>', partial(pr, 'w'))
        ent.bind_all('<KeyPress-s>', partial(pr, 's'))
        ent.bind_all('<KeyPress-a>', partial(pr, 'a'))
        ent.bind_all('<KeyPress-d>', partial(pr, 'd'))

        text = Text(self.root, state=DISABLED, width=59, height=59)
        text['bg'] = 'black'
        text.pack(anchor = CENTER)

        text.tag_config("green", foreground="green2")
        text.tag_config('green1', foreground='green')
        text.tag_config("red", foreground="red")
        text.tag_config('black', foreground='black', background='black')

        token_to_tag = {
            "1": "green",
            "2": "red",
            '8': 'green',
            '7': 'black',
            '0': 'green1'
        }

        def write(text, writing):
            text.configure(state = NORMAL)
            text.insert('1.0',writing)
            text.configure(state = DISABLED)
            return writing

        def deleting(text):
            text.configure(state = NORMAL)
            text.delete('1.0', END)
            text.configure(state = DISABLED)

        @self.check_window
        def label_showpole_conding():

            try:
                deleting(text)
                self.shadow = write(text, self.pole.show_pole())

                def on_edit(event):

                    for tag in text.tag_names():
                        text.tag_remove(tag, 1.0, END)

                    s = text.get(1.0, END)

                    for i, line in enumerate(s.splitlines(),
                                             start=1):
                        for match in re.finditer('[0-9]', line):
                            token_text = match.group(0).lower()
                            start = match.start()
                            if token_text in token_to_tag:
                                text.tag_add(token_to_tag[token_text], f"{i}.{start}")
                    text.edit_modified(0)

                text.bind('<<Modified>>', on_edit)
                text.bind('<MouseWheel>', lambda event: 'break')

            except IndexError:
                write(text, self.shadow)
                return showinfo('youre looser', f'''your polzun is dead
                    bad job
----------------------------
your length is__{str(len(self.pole.snake.show_length()))}
your score is__{len(self.pole.snake.show_length())*(2 if self.pole.bushenemy else 1)+self.pole.apple_gen\
                + (1000 if self.pole.snakeenemy and len(self.pole.snakes)==1 else 0)}
''')
            self.after_id = self.root.after(900-self.pole.apple_gen,label_showpole_conding )

        label_showpole_conding()








menu = MenuWindow()
#setting = SettingWindow()


#window = StartWindow()

