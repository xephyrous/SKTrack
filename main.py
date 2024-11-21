from customtkinter import *
from tkinter import *
from tkVideoPlayer import TkinterVideo

# Base window setup & styling
app = CTk()
app.geometry("1000x600")
app.title("SKTrack v0.1.a")
set_appearance_mode("light")
app.iconbitmap("assets/vertex_icon.ico")
# We have to use light mode for now due to the lack
# of menubar and other widgets' customization

# Main menubar & menu setup
menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
editmenu = Menu(menubar, tearoff=0)

filemenu.add_command(label="Import", command="")
filemenu.add_command(label="Export", command="")
filemenu.add_command(label="Exit", command=app.quit)

editmenu.add_command(label="Appearance", command="")
editmenu.add_command(label="Overlay", command="")

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)

# Video player
videoplayer = TkinterVideo(master=app, scaled=True)
videoplayer.pack(expand=True, fill='both')

# App composition and entrypoint
app.config(menu=menubar)
app.mainloop()

def loadVideo(path):
    try:
        videoplayer.load(path)
    except TypeError:
        print(f"Non-video file supplied '{path}'!")
    except TclError:
        print(f"Failed to load video '{path}'!")
