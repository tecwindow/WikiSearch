#-*- coding: utf-8 -*-
# import project libraries.
import wx
import re
from  my_classes import my_threads
import webbrowser
from settings import Settings
from functions import *

#Set language  for Headings List Dialog
_ = SetLanguage(Settings().ReadSettings())

#creating references List Dialog
class ReferencesListDialog(wx.Dialog):
	def __init__(self, parent, *references ):
		wx.Dialog.__init__(self, parent, title=_("Article references"), size=(300, 320))
		self.Center()
		self.references = references

		# Create panel
		Panel = wx.Panel(self)

		# Create ListBox
		self.ReferencesListTitle = wx.StaticText(Panel, -1, _("Article references"), pos=(10,10), size=(380,30))
		self.ReferencesList = wx.ListBox(Panel, -1, pos=(10,30), size=(290,170))

		# Create Buttons
		self.Go = wx.Button(Panel, -1, _("&Open in browser"), pos=(10,235), size=(120,30))
		self.Go.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"), pos=(140,235), size=(120,30))

		self.hotKeys = wx.AcceleratorTable((
(wx.ACCEL_CTRL, ord("W"), self.GoBack.GetId()),
(wx.ACCEL_ALT, ord("O"), self.Go.GetId()),
))
		Panel.SetAcceleratorTable(self.hotKeys)


#Event of go button 
		self.Go.Bind(wx.EVT_BUTTON, self.OnGo)

#Show dialog
		self.Show()

	def OpenThread(self):

		pattern = r'^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)'

		for i in range(len(self.references)):
			res = re.search(pattern, self.references[i])
			link = res.group(0)
			self.ReferencesList.Append(_("Reference {}: {}").format(i+1, link))

		self.ReferencesList.Selection = 0

	def OnGo(self, event):
		SelectedItem = self.references[self.ReferencesList.Selection]
		webbrowser.open_new(SelectedItem)
		self.Destroy()


class HeadingsListDialog(wx.Dialog):
	def __init__(self, parent, content):
		wx.Dialog.__init__(self, parent, title=_("Headings in this article"), size=(300, 320))
		self.Center()
		self.content = content

		# Create panel
		Panel = wx.Panel(self)

		# Create ListBox
		wx.StaticText(Panel, -1, _("Choose a heading"), pos=(10,10), size=(380,30))
		self.HeadingsList = wx.ListBox(Panel, -1, pos=(10,30), size=(290,170))
		self.result = re.findall("==.+==", self.content)
		NewResult = []

		for x in self.result:
			x = x.replace("=", "")
			NewResult.append(x[1:-1])
		self.HeadingsList.SetItems(NewResult)
		self.HeadingsList.Selection = 0

		# Create Buttons
		self.Go = wx.Button(Panel, -1, _("Go"), pos=(10,235), size=(120,30))
		self.Go.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"), pos=(140,235), size=(120,30))

		self.hotKeys = wx.AcceleratorTable((
(wx.ACCEL_CTRL, ord("W"), self.GoBack.GetId()),
(wx.ACCEL_CTRL, ord("H"), self.Go.GetId()),
))
		Panel.SetAcceleratorTable(self.hotKeys)

#Event of go button 
		self.Go.Bind(wx.EVT_BUTTON, self.OnGo)

	def OnGo(self, event):
		position = self.content.find(self.result[self.HeadingsList.Selection])
		self.EndModal(position)

class ViewTablesDialog(wx.Dialog):
	def __init__(self, parent, url, ArticleTitle):
		wx.Dialog.__init__(self, parent, title=_("Tables in {}:").format(ArticleTitle), size=(550, 550))
		self.Center()
		self.url = url
		self.LoadTables = my_threads(target=self.OnViewTable, daemon=True)
		self.LoadTables.start()

	#Creating Panel
		Panel = wx.Panel(self)

	#Creating text ctrl to view article tables
		wx.StaticText(Panel, -1, _("Tables in {}:").format(ArticleTitle), pos=(10,10), size=(380, 30))
		self.ViewArticleTables = wx.TextCtrl(Panel, -1, pos=(10, 50), size=(500, 400), style=wx.TE_RICH2+wx.TE_MULTILINE+wx.TE_READONLY)

	#Creating cancel button
		self.close = wx.Button(Panel, wx.ID_CANCEL, _("&Close"), pos=(200,450), size=(120,30))

		self.hotKeys = wx.AcceleratorTable((
(wx.ACCEL_CTRL, ord("W"), self.close.GetId()),
))
		Panel.SetAcceleratorTable(self.hotKeys)

		#Show dialog
		self.Show()

	def OnViewTable(self):

		tables = GetTables(self.url)

		for table in range(len(tables)):
			self.ViewArticleTables.write(_("Table {}:\n {}").format(table+1,tables[table]))

		self.ViewArticleTables.SetInsertionPoint(0)
