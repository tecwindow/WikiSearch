#-*- coding: utf-8 -*-
# import project libraries.
import wx

colourList = ["Aquamarine", "Black", "Blue", "Blue Violet", "Brown", "Cadet Blue", "Coral", "Cornflower Blue", "Cyan", "Dark Grey", "Dark Green", "Brown"]

class ChangeTheme(wx.Dialog):

	def __init__(self):
		super().__init__(None, title = "change theme", size=(200, 200))
		self.Center()
		self.Maximize(False)
		Panel = wx.Panel(self)
		wx.StaticText(Panel, -1, "Choose theme", pos=(20,20), size=(80, 30))
		self.ChangeTheme = wx.ComboBox(Panel, -1, pos=(20, 50), size=(140, 40), style=wx.CB_READONLY+wx.CB_SORT)
		self.ChangeTheme.SetItems(colourList)
		# Create Buttons
		self.Change = wx.Button(Panel, -1, "change", pos=(20,100), size=(60,30))
		self.Change.SetDefault()
		self.Close = wx.Button(Panel, wx.ID_CANCEL, "Cancel", pos=(90,100), size=(60,30))

		self.Change.Bind(wx.EVT_BUTTON, self.OnChangeTheme)

	def OnChangeTheme(self, event):
		self.EndModal(self.ChangeTheme.Selection)

