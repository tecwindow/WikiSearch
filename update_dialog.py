#-*- coding: utf-8 -*-
# import project libraries.
import wx
import threading 
import requests
import os
import shutil
import json
import subprocess
from settings import Settings
from functions import *

#Set language for update dialog
_ = SetLanguage(Settings().ReadSettings())

#Delete setup file if is found in temp.
temp = os.path.join(os.getenv("temp"), "WikiSearch")
if os.path.exists(temp):
	shutil.rmtree(temp, ignore_errors=True)

#creating update dialog 
class UpdateDialog(wx.Dialog):
	def __init__(self, parent, RecentVersion, whatIsNew):
		wx.Dialog.__init__(self, parent, title = _("Update found"), size=(500, 500))
		self.Center()

		#creating panel
		Panel = wx.Panel(self)

		#creating field to show what's new.
		wx.StaticText(Panel, -1, _("Version {} is available.").format(RecentVersion), pos=(20,20), size=(170, 30))
		self.WhatsNew = wx.TextCtrl(Panel, -1, value=whatIsNew, pos=(10,60), size=(450,320), style=wx.HSCROLL+wx.TE_MULTILINE+wx.TE_READONLY)

		# Creating Buttons
		self.Update = wx.Button(Panel, -1, _("&Update"), pos=(20,400), size=(60,30))
		self.Update.SetDefault()
		self.Close = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"), pos=(90,400), size=(60,30))

		self.hotKeys = wx.AcceleratorTable([
			(wx.ACCEL_ALT, ord("U"), self.Update.GetId()),
			(wx.ACCEL_CTRL, ord("W"), self.Close.GetId()),
		])
		Panel.SetAcceleratorTable(self.hotKeys)


		#show the dialog
		self.Show()

		#event for update button
		self.Update.Bind(wx.EVT_BUTTON, self.OnDownloadUpdate)

	#creating OnDownloadUpdate function  to show progress dialog.
	def OnDownloadUpdate(self,  event):
		ProgressDialog = progress_dialog(_("Downloading update"), _("Please wait."), maximum=100, parent=self, style=wx.PD_CAN_ABORT)


#creating progress dialog
class progress_dialog(wx.ProgressDialog):
	def __init__(self, *args, **kwargs):
		wx.ProgressDialog.__init__(self, *args, **kwargs)

		self.handle = kwargs["parent"]

		#making downloading function in thread to download update.
		threading.Thread(target=self.downloading, daemon=True).start()

	#creating downloading function
	def downloading(self):

#geting download ling from online info file.
		DownloadLink = GetOnlineInfo()["url"]

#extracting the name file and geting temp path.
		if not os.path.exists(temp):
			os.mkdir(temp)

		file_name = DownloadLink.split('/')[-1]
		path = os.path.join(temp, file_name)

		f = open(path, 'wb')
		with requests.get(DownloadLink, stream=True) as r:
			downloaded=0
			total =  int(r.headers['content-length'])
			for i in r.iter_content(chunk_size=1024):
				if self.WasCancelled():
					self.Destroy()
					f.close()
					os.remove(path)
					self.handle.Destroy()
					return None
				downloaded+=len(i)
				progress = int((downloaded/total)*100)
				f.write(i)
				if progress == 100:
					f.close()
					subprocess.run([path, "/SILENT", "/VERYSILENT", "/SUPPRESSMSGBOXES"])
				self.Update(progress)

