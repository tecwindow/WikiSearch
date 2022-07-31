#-*- coding: utf-8 -*-
# import project libraries.
import wx
import threading 
import requests
from urllib.request import urlopen
import os
import json
import subprocess
from settings import Settings
from functions import *

#Set language for update dialog
_ = SetLanguage(Settings().ReadSettings())


#geting what's new and download ling from online info file.
try:
	url = "https://raw.githubusercontent.com/tecwindow/WikiSearch/main/WikiSearch.json"
	response = urlopen(url)
	data_json = json.loads(response.read())
	whatIsNew = data_json["What's new"]
	DownloadLink = data_json["url"]
except:
	pass

#extracting the name file and geting temp path.
try:
	file_name = DownloadLink.split('/')[-1]
	temp = os.getenv("temp")
	path = str(temp+"/"+file_name)
except:
	path = ""

#Delete setup file if is found in temp.
if os.path.exists(path):
	os.remove(path)



#creating update dialog 
class UpdateDialog(wx.Dialog):
	def __init__(self, parent, RecentVersion):
		super().__init__(None, title = _("There is an update"), size=(300, 300))
		self.Center()
		self.Maximize(False)

		#creating panel
		Panel = wx.Panel(self)

		#creating field to show what's new.
		wx.StaticText(Panel, -1, _("What's new in version {}?").format(RecentVersion), pos=(20,20), size=(170, 30))
		self.WhatsNew = wx.TextCtrl(Panel, -1, value=whatIsNew, pos=(10,60), size=(250,90), style=wx.HSCROLL+wx.TE_MULTILINE+wx.TE_READONLY)

		# Creating Buttons
		self.Update = wx.Button(Panel, -1, _("&Update"), pos=(20,200), size=(60,30))
		self.Update.SetDefault()
		self.Close = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"), pos=(90,200), size=(60,30))

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

