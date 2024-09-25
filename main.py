import wx, wx.media


class SKFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()

        importVid = wx.MenuItem(fileMenu, 100, text="Import Video", kind=wx.ITEM_NORMAL)
        exportVid = wx.MenuItem(fileMenu, 110, text="Export Video", kind=wx.ITEM_NORMAL)
        fileMenu.Append(importVid)
        fileMenu.Append(exportVid)

        menuBar.Append(fileMenu, "&File")

        self.mediaCtrl = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER, szBackend=wx.media.MEDIABACKEND_GSTREAMER)
        self.media = "C:\\Users\\alexa\\Videos\\HelixSnap3D.mp4"

        self.SetMenuBar(menuBar)
        self.Show(True)


app = wx.App(False)
frame = SKFrame(None, "SK-Track v0.1a")
app.MainLoop()
