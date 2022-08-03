#-*- coding: utf-8 -*-
# import project libraries.
import wx
import re
import webbrowser
from settings import Settings
from functions import *

#Set language  for Headings List Dialog
_ = SetLanguage(Settings().ReadSettings())

#creating references List Dialog
class ReferencesListDialog(wx.Dialog):
	def __init__(self, parent, *references ):
		super().__init__(parent, title=_("References of this article"), size=(300, 320))
		self.Center()
		self.references = references

		# Create panel
		Panel = wx.Panel(self)

		# Create ListBox
		self.ReferencesListTitle = wx.StaticText(Panel, -1, _("References of this article"), pos=(10,10), size=(380,30))
		self.ReferencesList = wx.ListBox(Panel, -1, pos=(10,30), size=(290,170))

		# Create Buttons
		self.Go = wx.Button(Panel, -1, _("Go\t(Alt+h)"), pos=(10,235), size=(120,30))
		self.Go.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"), pos=(140,235), size=(120,30))

#Event of go button 
		self.Go.Bind(wx.EVT_BUTTON, self.OnGo)

#Show dialog
		self.Show()

	def OpenThread(self):
		for i in range(len(self.references)):
			self.ReferencesList.Append(_("reference{}").format(i+1))

	def OnGo(self, event):
		SelectedItem = self.references[self.ReferencesList.Selection]
		webbrowser.open_new(SelectedItem)
		self.Destroy()


class HeadingsListDialog(wx.Dialog):
	def __init__(self, parent, content):
		super().__init__(parent, title=_("Headings in this article"), size=(300, 320))
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
				NewResult.append(x.replace("=", ""))
		self.HeadingsList.SetItems(NewResult)
		self.HeadingsList.Selection = 0

		# Create Buttons
		self.Go = wx.Button(Panel, -1, _("Go\t(Alt+h)"), pos=(10,235), size=(120,30))
		self.Go.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"), pos=(140,235), size=(120,30))

#Event of go button 
		self.Go.Bind(wx.EVT_BUTTON, self.OnGo)

	def OnGo(self, event):
		position = self.content.find(self.result[self.HeadingsList.Selection])
		self.EndModal(position)

