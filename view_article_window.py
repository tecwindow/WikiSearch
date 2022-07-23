#-*- coding: utf-8 -*-
# import project libraries.
import wx
import nlpia2_wikipedia as wikipedia
import pyperclip
from change_theme_dialog import ChangeTheme
import os

colourList = ["Aquamarine", "Black", "Blue", "Blue Violet", "Brown", "Cadet Blue", "Coral", "Cornflower Blue", "Cyan", "Dark Grey", "Dark Green", "Brown"]

#View Article window
class ViewArticleWindow(wx.Frame):
	def __init__(self, parent, GetValues, handle):
		super().__init__(parent, title="View Article", size=(560, 600))
		self.Center()
		self.EnableMaximizeButton(False)
		self.GetValues = GetValues
		self.Content = ""
		self.url = ""
		self.title = ""
		self.handle = handle


		Panel = wx.Panel(self)
		# Create Menus.
		menubar = wx.MenuBar()
		actions = wx.Menu()
		self.CopyArticleItem = actions.Append(-1, "Copy article\tctrl+shift+c")
		self.CopyArticleLinkItem = actions.Append(-1, "Copy article link\tctrl+alt+c")
		self.SaveArticleItem = actions.Append(-1, "save article\tctrl+s")
		self.ChangeThemeItem = actions.Append(-1, "change Theme\tctrl+T")
		self.CloseArticleItem = actions.Append(-1, "close article window\tctrl+w")
		self.CloseProgramItem = actions.Append(-1, "Close the program\tctrl+F4")
		menubar.Append(actions, "Actions")
		self.SetMenuBar(menubar)

		self.hotKeys = wx.AcceleratorTable([
			(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("C"), self.CopyArticleItem.GetId()),
			(wx.ACCEL_CTRL+wx.ACCEL_ALT, ord("C"), self.CopyArticleLinkItem.GetId()),
			(wx.ACCEL_CTRL, ord("S"), self.SaveArticleItem.GetId()),
			(wx.ACCEL_CTRL, ord("T"), self.ChangeThemeItem.GetId()),
			(wx.ACCEL_CTRL, ord("W"), self.CloseArticleItem.GetId()),
			(wx.ACCEL_CTRL,wx.WXK_F4, self.CloseProgramItem.GetId()),
		])
		Panel.SetAcceleratorTable(self.hotKeys)

		# Create RichEdit to View Article Content
		self.ArticleTitle = wx.StaticText(Panel, -1, "please wait:", pos=(10,10), size=(380,30))
		self.ViewArticle = wx.TextCtrl(Panel, -1, pos=(30,40), size=(480,420), style=wx.TE_RICH2+wx.TE_MULTILINE+wx.TE_READONLY)


		# Create Buttons
		self.CopyArticle = wx.Button(Panel, -1, "Copy article\t(ctrl+shift+c)", pos=(10,500), size=(120,30))
		self.SaveArticle = wx.Button(Panel, -1, "save article\t(ctrl+s)", pos=(140,500), size=(120,30))
		self.SaveArticle.SetDefault()
		self.CopyArticleLink = wx.Button(Panel, -1, "Copy article link\t(ctrl+alt+c)", pos=(270,500), size=(120,30))
		self.CloseArticle = wx.Button(Panel, -1, "Close Article\t(ctrl+w)", pos=(400,500), size=(120,30))

		# Show Article window
		self.Show()

		# events for buttons
		self.CopyArticle.Bind(wx.EVT_BUTTON, self.OnCopyArticle)
		self.SaveArticle.Bind(wx.EVT_BUTTON, self.OnSaveArticle)
		self.CopyArticleLink.Bind(wx.EVT_BUTTON, self.OnCopyArticleLink)
		self.CloseArticle.Bind(wx.EVT_BUTTON, self.OnCloseArticle)

		# events for Menus
		self.Bind(wx.EVT_MENU, self.OnCopyArticle, self.CopyArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCopyArticleLink, self.CopyArticleLinkItem) 
		self.Bind(wx.EVT_MENU, self.OnSaveArticle, self.SaveArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCloseArticle, self.CloseArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnChangeTheme, self.ChangeThemeItem) 
		self.Bind(wx.EVT_MENU, self.OnCloseProgram, self.CloseProgramItem) 

	def OpenThread(self):
		try:
			self.Content = wikipedia.page(self.GetValues).content
		except wikipedia.exceptions.DisambiguationError as e:
			mgb = wx.MessageDialog(self, """This article is no longer available.
do you want to show similar results for this  article?
""", "warning", style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_QUESTION)
			if mgb.ShowModal() == wx.ID_YES:
				self.Destroy()
#				wx.Window.Close(self.handle)
				self.handle.ListResults.SetItems(e.options)
			else:
				self.Destroy()
			return None
		self.url = wikipedia.page(self.GetValues).url
		self.title = wikipedia.page(self.GetValues).title
		self.ViewArticle.Value = self.Content
		self.SetTitle(f"View {self.title}")
		self.ArticleTitle.SetLabel(self.title)

	# Copy Article Content
	def OnCopyArticle(self, event):
		pyperclip.copy(self.Content)

	# Copy Article Link
	def OnCopyArticleLink(self, event):
		pyperclip.copy(self.url)

	# Save Article On a New File.
	def OnSaveArticle(self, event):
		SaveFile = wx.FileDialog(self, F"Save {self.title}:", "self.FilePath", F"{self.title}", style=wx.FD_SAVE+wx.FD_OVERWRITE_PROMPT)
		SaveFile.Wildcard = "Text files (.txt)|*.txt"
		SaveFileResult = SaveFile.ShowModal()
		if SaveFileResult == wx.ID_OK:
			FilePath = SaveFile.Path
			#FileName = SaveFile.Filename
			file = open(FilePath, "w", encoding="utf-8")
			file.write(self.ViewArticle.Value)
			file.close()
		else:
			return

	def OnChangeTheme(self, event):
		dialog2 = ChangeTheme()
		GetTheme = dialog2.ShowModal()
		self.SetBackgroundColour(wx.Colour(colourList[GetTheme]))
		self.ViewArticle.SetBackgroundColour(wx.Colour(colourList[GetTheme]))
		self.Refresh()

	# Close Article Window
	def OnCloseArticle(self, event):
		self.Destroy()


		# Close Program 
	def OnCloseProgram(self, event):
		wx.Exit()
