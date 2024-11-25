from customtkinter import *
from tkinter import *
from tkVideoPlayer import TkinterVideo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import datetime
from utils import model, commands as cmd


loadedVideo = ""


def process():
    if not loadedVideo:
        terminalOutput(f"No loaded video to process", error=True)
        return

    terminalOutput(f"Processing video '{loadedVideo}'...")
    inferModel = model.Infer3D(terminalOutput)
    results = inferModel.infer_video(loadedVideo, return_vis=True, show_vis=True)


commandFuncs = {
    "process": process
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

    video_path = askopenfilename(
        title="Import Video File",
        filetypes=[("Videos", "*.mp4;*.mov;*.avi")]
    )

    if video_path:
        try:
            loadVideo(video_path)
            videoPlayer.seek(1)
            loadedVideo = video_path
            terminalOutput(f"Imported video {video_path}")
        except Exception as e:
            terminalOutput(f"Failed to load & play video {video_path}", error=True)

    else:
        terminalOutput(f"Failed to import video '{video_path}'!", error=True)


def exportVideo():
    asksaveasfilename(
        title="Export Video File",
        defaultextension=".mp4",
        filetypes=[("Videos", "*.mp4;*.mov;*.avi")]
    )


def terminalInput(command):
    if not command.strip():
        return

    if not cmd.matchCommand(command.strip(), terminalOutput):
        return

    terminalOutput(command, True)
    commandFuncs[command.strip().split(' ')[0]]()


def terminalOutput(text, clearText=True, error=False):
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
                terminalText.insert("end", " " + text + "\n", "error")
            else:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {text}\n")
                terminalText.insert("end", "[" + datetime.now().strftime("%H:%M:%S") + "] " + text + "\n")
            f.close()
        terminalText.config(state="disabled")


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

# Displayed terminal text
terminalText = Text(terminalFrame, font=("Consolas", 12), wrap="char")
terminalText.place(relx=0, rely=0, relwidth=1, relheight=1)

# Configure terminal tags
terminalText.tag_configure("bold", font=("Consolas", 12, "bold"))
terminalText.tag_configure("symbol", font=("Consolas", 10, "bold"))
terminalText.tag_configure("symbol-bold", font=("Consolas", 10, "bold"))
terminalText.tag_configure("symbol-err", font=("Consolas", 8, "bold"))
terminalText.tag_configure("title", font=("Consolas", 14, "bold"), justify="center")
terminalText.tag_configure("error", font=("Consolas", 12, "bold"), foreground="red")

# Configure starting terminal state
terminalText.insert("1.0", "[SKTrack Terminal v1.0.a]\n", "title")
loadTerminalContent()
terminalText.config(state="disabled")

# Terminal input
commandInput = Text(terminalFrame, bg="white", fg="black", font=("Consolas", 12))
commandInput.place(relx=0, rely=1, relwidth=1, height=20, anchor="sw")
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

# App composition and entry point
app.config(menu=menuBar)
app.mainloop()
