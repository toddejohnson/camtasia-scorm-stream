#!/usr/bin/python

import re
import tempfile
import os
import zipfile
import shutil

try:
    import wx
except ImportError:
	raise ImportError, "The wxPython module is required to run this program"


class convert_wx(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title)
        self.parent = parent
        self.initialize()

    def initialize(self):
        sizer = wx.GridBagSizer()

        self.fmsbasel = wx.StaticText(self, label="FMS Base:")
        sizer.Add(self.fmsbasel,(0,0),(1,1))
        self.fmsbase = wx.TextCtrl(self,-1,value="")
        sizer.Add(self.fmsbase,(0,1),(1,2),wx.EXPAND)

        self.inputfilel = wx.StaticText(self, label="SCORM File:")
        sizer.Add(self.inputfilel,(1,0),(1,1))
        self.inputfile = wx.TextCtrl(self,-1,value="")
        self.inputfile.SetEditable(False)
        sizer.Add(self.inputfile,(1,1),(1,1),wx.EXPAND)
        inputfileb = wx.Button(self,-1,label="Browse")
        sizer.Add(inputfileb, (1,2))
        self.Bind(wx.EVT_BUTTON, self.OnBrowseClick, inputfileb)
        
        self.outputfolderl = wx.StaticText(self, label="Output Folder:")
        sizer.Add(self.outputfolderl,(2,0),(1,1))
        self.outputfolder = wx.TextCtrl(self,-1,value="")
        #self.outputfolder.SetEditable(False)
        sizer.Add(self.outputfolder,(2,1),(1,1),wx.EXPAND)
        outputfolderb = wx.Button(self,-1,label="Browse")
        sizer.Add(outputfolderb, (2,2))
        self.Bind(wx.EVT_BUTTON, self.OnBrowseClickDir, outputfolderb)

        button = wx.Button(self,-1,label="Go Convert!")
        sizer.Add(button,(3,0))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, button)

        sizer.AddGrowableCol(1)
        self.SetSizer(sizer)
        self.Show(True)

    def OnButtonClick(self,event):
        fmsbase = self.fmsbase.GetValue()
        inputfile = self.inputfile.GetValue()
        outputfolder = self.outputfolder.GetValue()
        outputfile = os.path.join(outputfolder, os.path.basename(inputfile)[:-4]+"_new.zip")
        tempdir = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(inputfile, 'r') as zipread:
                with zipfile.ZipFile(outputfile, 'w') as zipwrite:
                    for item in zipread.infolist():
                        if ".mp4" in item.filename.lower():
                            zipread.extract(item.filename,outputfolder)
                        elif "_player.html" in item.filename.lower():
                            data = zipread.read(item.filename)
                            data=re.sub(r'setMediaSrc\("([^"]+)"',
                                'setMediaSrc("' + fmsbase + '\g<1>"',
                                data)
                            zipwrite.writestr(item,data)  
                        else:
                            data = zipread.read(item.filename)
                            zipwrite.writestr(item,data)
        finally:
            shutil.rmtree(tempdir)
        wx.MessageBox('Conversion Finished!!!', "Info", wx.OK | wx.ICON_INFORMATION)

    def OnBrowseClick(self,event):
        dialog = wx.FileDialog(self, "Choose SCORM ZIP","","","ZIP Files (*.zip)|*.zip", wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.inputfile.SetValue(dialog.GetPath())
        dialog.Destroy()
        
    def OnBrowseClickDir(self,event):
        dialog = wx.FileDialog(self, "Choose a directory",style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.outputfolder.SetValue(dialog.GetPath())
        dialog.Destroy()



if __name__ == "__main__":
    app = wx.App()
    frame = convert_wx(None,-1,"Camtasia Streaming Converter")
    app.MainLoop()
