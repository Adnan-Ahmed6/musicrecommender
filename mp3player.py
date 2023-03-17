from http.client import ImproperConnectionState
import tkinter as tk
from tokenize import cookie_re
from pygame import mixer
import os 
import fnmatch 
from tinytag import TinyTag

#import function for notebook
###################################################################################################################################################################

import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit('.', 1)[-1]
    if not path:
        path = ['']
    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path
        
class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""
    def __init__(self, path=None):
        self.shell = InteractiveShell.instance()
        self.path = path

    def load_module(self, fullname):
        """import a notebook as a module"""
        path = find_notebook(fullname, self.path)

        print ("importing Jupyter notebook from %s" % path)

        # load the notebook object
        with io.open(path, 'r', encoding='utf-8') as f:
            nb = read(f, 4)


        # create the module and add it to sys.modules
        # if name in sys.modules:
        #    return sys.modules[name]
        mod = types.ModuleType(fullname)
        mod.__file__ = path
        mod.__loader__ = self
        mod.__dict__['get_ipython'] = get_ipython
        sys.modules[fullname] = mod

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        try:
          for cell in nb.cells:
            if cell.cell_type == 'code':
                # transform the input to executable Python
                code = self.shell.input_transformer_manager.transform_cell(cell.source)
                # run the code in themodule
                exec(code, mod.__dict__)
        finally:
            self.shell.user_ns = save_user_ns
        return mod
    
    class NotebookFinder(object):
        """Module finder that locates Jupyter Notebooks"""
        def __init__(self):
            self.loaders = {}

        def find_module(self, fullname, path=None):
            nb_path = find_notebook(fullname, path)
            if not nb_path:
                return

            key = path
            if path:
                # lists aren't hashable
                key = os.path.sep.join(path)

            if key not in self.loaders:
                self.loaders[key] = NotebookLoader(path)
            return self.loaders[key]
    
    sys.meta_path.append(NotebookFinder())
    
    ###################################################################################################################################################################

import mainmusic as mn

rootpath = "C:\\Users\Haider\Desktop\chip8"
match = "*.mp3"
mixer.init()

canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("600x800")
canvas.config(bg = "black")

prev_img = tk.PhotoImage(file = "prev_img.png")
stop_img = tk.PhotoImage(file = "stop_img.png")
play_img = tk.PhotoImage(file = "play_img.png")
pause_img = tk.PhotoImage(file = "pause_img.png")
next_img = tk.PhotoImage(file = "next_img.png")



listbox = tk.Listbox(canvas, fg= "cyan",bg = "black",width = 100)
listbox.pack(padx = 15, pady = 20)

label = tk.Label(canvas, text = '', fg= 'cyan', bg = 'black')
label.pack(pady = 15)

text=tk.Text(canvas, width=80, height=15)

text.pack()

#label_recomm = tk.Text(canvas, bg = 'black', fg = 'cyan', height = 10, width = 100)
#label_recomm.pack(padx = 15, pady = 20)

def select():
    label.config(text = listbox.get("anchor"))
    mixer.music.load(rootpath + "\\" + listbox.get("anchor"))
    #audio = TinyTag.get(listbox.get(listbox.curselection()))
    #print(audio.title)
    
    mixer.music.play()
    recommender()
   
def stop():
    mixer.music.stop()
    listbox.select_clear('active')
def play_next():
    next_song = listbox.curselection()
    next_song = next_song[0] + 1
    next_song_name = listbox.get(next_song)
    label.config(text = next_song_name)

    mixer.music.load(rootpath + "\\" + next_song_name)
    mixer.music.play()

    label_recomm.config(text="")
    listbox.select_clear(0, 'end')
    listbox.activate(next_song)
    listbox.select_set(next_song)
def play_prev():
    next_song = listbox.curselection()
    next_song = next_song[0] - 1
    label.config(text = listbox.get(next_song))

    mixer.music.load(rootpath + "\\" + listbox.get("anchor"))
    mixer.music.play()
    label_recomm.config(text="")

    listbox.select_clear(0, 'end')
    listbox.activate(next_song)
    listbox.select_set(next_song)
def pause():
    if pauseButton["text"] == "Pause":
         mixer.music.pause()
         pauseButton["text"] = "Play"
    else:
        mixer.music.unpause()
        pauseButton["text"] = "Pause"

def recommender():
    name = listbox.get(listbox.curselection())
    name = name.rsplit('.',1)[0]
    recomm = mn.recommend_songs(name)
    
    main_data = recomm
        #label_recomm = tk.Label(canvas,text = "Here are some of the songs you would like" + " \n "+str(main_data),fg = 'cyan', bg = 'black')

        #label_recomm = tk.Label(canvas,text = "Here are some of the songs you would like" + " \n "+str(main_data),fg = 'cyan', bg = 'black')

        
    #label_recomm.insert(tk.END, recomm)
    #label_recomm.get(1.0, "end-1c")
    #label_recomm.config(text = recomm)
    #label_recomm.pack()
    #text.insert(tk.END, str(recomm))
    
    label_recomm.config(text="Here are some of the songs you would like" + " \n "+str(main_data))
    label_recomm.pack(padx = 25, pady = 50)
    #print(str(recomm))       
        

top = tk.Frame(canvas, bg = 'black')
top.pack(padx = 10,pady = 5, anchor = 'center')

prevButton = tk.Button(canvas, text="Prev",image = prev_img,bg = "black",borderwidth=0, command = play_prev)
prevButton.pack(padx = 15,in_ = top, side = 'left')

nextButton = tk.Button(canvas, text="Next",image = next_img,bg = "black",borderwidth=0,command=play_next)
nextButton.pack(padx = 15,in_ = top, side = 'left')

stopButton = tk.Button(canvas, text="Stop",image = stop_img,bg = "black",borderwidth=0,command = stop)
stopButton.pack(padx = 15,in_ = top, side = 'left')

playButton = tk.Button(canvas, text="Play",image = play_img,bg = "black",borderwidth=0,command = select)
playButton.pack(padx = 15,in_ = top, side = 'left')

pauseButton = tk.Button(canvas, text="Pause",image = pause_img,bg = "black", borderwidth = 0,command = pause)
pauseButton.pack(padx = 15,in_ = top, side = 'left')

label_recomm = tk.Label(canvas,text = "",fg = 'cyan', bg = 'black')

for dirs,root,files in os.walk(rootpath):
    for filename in fnmatch.filter(files, match):
        listbox.insert('end', filename)


canvas.mainloop()
