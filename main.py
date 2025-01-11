import random
import string
import shutil
import threading
import re

from datetime import datetime
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

from customtkinter import *
from tkVideoPlayer import TkinterVideo

from utils import commands as cmd
from utils import pipers as pipe
from utils import model

loadedVideo = ""
tempName = ""


def process():
    global tempName

    if not loadedVideo:
        terminalOutput(f"No loaded video to process", error=True)
        return

    print(loadedVideo)

    terminalOutput(f"Processing video '{loadedVideo}'")
    tempName = ''.join(random.choices(string.ascii_letters, k=10))

    inferrer = model.Infer3D(terminalOutput)
    modelThread = threading.Thread(
        target=pipe.visualize_movie,
        name="modelThread",
        args=[
            loadedVideo,
            os.getcwd() + "/generated/" + tempName + "." + loadedVideo[len(loadedVideo) - 3:],
            0,
            inferrer,
            terminalOutput
        ]
    )

    modelThread.start()


def terminalImport(args):
    path = args[0].replace('"', '')
    global loadedVideo

    try:
        open(path, 'r')

        if not os.path.exists(path):
            raise IOError
    except IOError:
        terminalOutput(f"File '{path}' does not exist", error=True)
        return

    loadVideo(path)
    loadedVideo = path
    terminalOutput(f"Imported video {path}")


def terminalExport():
    global tempName, loadedVideo

    if not loadedVideo or not tempName:
        terminalOutput(f"No video available to export!", error=True)
        return

    videoPath = asksaveasfilename(
        title="Export Video File",
        defaultextension=".mp4",
        filetypes=[("Videos", "*.mp4;*.mov;*.avi")]
    )

    shutil.move(os.getcwd() + "/generated/" + tempName + "." + loadedVideo[len(loadedVideo) - 3:], videoPath)

    pathRegex = r"([^\\\/]+)(?=\.[^\\\/]+$)"
    terminalOutput(f"Exported file '{re.search(videoPath, pathRegex)}'")


commandFuncs = {
    "process": process,
    "import": lambda x: terminalImport(x),
    "export": terminalExport
}


def loadTerminalContent():
    ...


def loadVideo(path):
    try:
        videoPlayer.load(path)
    except TypeError:
        print(f"Non-video file supplied '{path}'!")
    except TclError:
        print(f"Failed to load video '{path}'!")


def importVideo():
    global loadedVideo

    videoPath = askopenfilename(
        title="Import Video File",
        filetypes=[("Videos", "*.mp4;*.mov;*.avi")]
    )

    if videoPath:
        try:
            loadVideo(videoPath)
            loadedVideo = videoPath
            terminalOutput(f"Imported video {videoPath}")
        except Exception as e:
            terminalOutput(f"Failed to load & play video {videoPath}", error=True)

    else:
        terminalOutput(f"Failed to import video '{videoPath}'!", error=True)


def exportVideo():
    if not loadedVideo or not tempName:
        terminalOutput(f"No video available to export!", error=True)
        return

    videoPath = asksaveasfilename(
        title="Export Video File",
        defaultextension=".mp4",
        filetypes=[("Videos", "*.mp4;*.mov;*.avi")]
    )

    shutil.move(os.getcwd() + "/generated/" + tempName + "." + loadedVideo[len(loadedVideo) - 3:], videoPath)

    pathRegex = r"([^\\\/]+)(?=\.[^\\\/]+$)"
    terminalOutput(f"Exported file '{re.search(videoPath, pathRegex)}'")


def terminalInput(command):
    if not command.strip():
        return

    if not cmd.matchCommand(command.strip(), terminalOutput):
        return

    print(command.strip().split()[1:])
    terminalOutput(command, True, command=True)
    if len(command.strip().split()) == 1:
        commandFuncs[command.strip().split(' ')[0]]()
        return

    commandFuncs[command.strip().split(' ')[0]](command.strip().split()[1:])


def terminalOutput(text, clearText=True, error=False, command=False):
    if clearText:
        commandInput.delete("1.0", "end")

    text = text.strip()

    if text:
        terminalText.config(state="normal")
        with open("logfile.txt", "a") as f:
            if error:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] ! {text}\n")
                terminalText.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] ", "error")
                terminalText.insert("end", "⚠︎", "symbol-err")
                terminalText.insert("end", f" {text}\n", "error")
            elif command:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] -> {text}\n")
                terminalText.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] ", "command")
                terminalText.insert("end", "➦", "symbol-cmd")
                terminalText.insert("end", f" {text}\n", "command")
            else:
                terminalText.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {text}\n")
            f.close()
        terminalText.config(state="disabled")

    terminalText.see("end")



# Base window setup & styling
app = CTk()
app.geometry("1000x600")
app.title("SKTrack v0.1.a")
set_appearance_mode("light")
app.iconbitmap("assets/vertex_icon.ico")

# Setup logfile
with open("logfile.txt", "w") as f:
    f.write(f"Logging started at {datetime.now()}\n")
    f.close()

# Main menubar & menu setup
menuBar = Menu(app)
fileMenu = Menu(menuBar, tearoff=0)
editMenu = Menu(menuBar, tearoff=0)

fileMenu.add_command(label="Import", command=importVideo)
fileMenu.add_command(label="Export", command=exportVideo)
fileMenu.add_command(label="Exit", command=app.quit)

editMenu.add_command(label="Appearance", command="")
editMenu.add_command(label="Overlay", command="")

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Edit", menu=editMenu)

# Configure grid layout
app.grid_rowconfigure(0, weight=4)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=2)

# Terminal frame
terminalFrame = Frame(app, padx=5, pady=5)
terminalFrame.grid(row=0, column=0, sticky="nsew")
terminalFrame.grid_propagate(False)

# Terminal frame grid configuration
terminalFrame.grid_rowconfigure(0, weight=1)
terminalFrame.grid_rowconfigure(1, weight=0)
terminalFrame.grid_columnconfigure(0, weight=1)

# Displayed terminal text
terminalText = Text(terminalFrame, font=("Consolas", 12), wrap="char")
terminalText.grid(row=0, column=0, sticky="nsew")

# Configure terminal tags
terminalText.tag_configure("bold", font=("Consolas", 12, "bold"))
terminalText.tag_configure("symbol", font=("Consolas", 10, "bold"))
terminalText.tag_configure("symbol-bold", font=("Consolas", 10, "bold"))
terminalText.tag_configure("symbol-err", font=("Consolas", 8, "bold"))
terminalText.tag_configure("symbol-cmd", font=("Consolas", 10, "bold"), foreground="blue")
terminalText.tag_configure("title", font=("Consolas", 14, "bold"), justify="center")
terminalText.tag_configure("error", font=("Consolas", 12, "bold"), foreground="red")
terminalText.tag_configure("command", font=("Consolas", 12, "bold"), foreground="blue")

# Configure starting terminal state
terminalText.insert("1.0", "[SKTrack Terminal v1.0.a]\n", "title")
loadTerminalContent()
terminalText.config(state="disabled")

# Terminal input
commandInput = Text(terminalFrame, bg="white", fg="black", font=("Consolas", 12), height=1)
commandInput.grid(row=1, column=0, sticky="ew")
commandInput.bind("<Return>", lambda event: terminalInput(commandInput.get("1.0", "end-1c")))

# Video frame
videoFrame = Frame(app, padx=5, pady=5)
videoFrame.grid(row=0, column=1, sticky="nsew")

# Add TkinterVideo to videoFrame
videoPlayer = TkinterVideo(master=videoFrame, scaled=True)
videoPlayer.grid(row=0, column=0, sticky="nsew")

# Video frame grid configuration
videoFrame.grid_rowconfigure(0, weight=1)
videoFrame.grid_columnconfigure(0, weight=1)

# Settings frame
settingsFrame = Frame(app, bg="white")
settingsFrame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Clean generated folder
count = 0
for filename in os.listdir(os.getcwd() + "/generated/"):
    file_path = os.path.join(os.getcwd() + "/generated/", filename)
    if os.path.isfile(file_path):
        count += 1
        os.remove(file_path)

terminalOutput(f"Cleaned generated directory of {count} files", command=True)

# App composition and entry point
app.config(menu=menuBar)
app.mainloop()
