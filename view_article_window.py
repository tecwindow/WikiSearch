#-*- coding: utf-8 -*-
# import project libraries.
import wx
import nlpia2_wikipedia as wikipedia
import pyperclip
import webbrowser
import accessible_output2.outputs.auto
import os
import re
import threading 
import requests
from bs4 import BeautifulSoup
from change_theme_dialog import ChangeTheme
from dialogs import *
from settings import Settings
from functions import *

#Set language for View Article window
_ = SetLanguage(Settings().ReadSettings())

colourList = ["Aquamarine", "Black", "Blue", "Blue Violet", "Brown", "Cadet Blue", "Coral", "Cornflower Blue", "Cyan", "Dark Grey", "Dark Green", "Brown"]

#View Article window
class ViewArticleWindow(wx.Frame):
	def __init__(self, parent, GetValues, handle):
		super().__init__(parent, title=_("View article"), size=(560, 600))
		self.Center()
		self.EnableMaximizeButton(False)
		self.GetValues = GetValues
		self.Content = ""
		self.url = ""
		self.title = ""
		self.links = ""
		self.references = ""
		self.html = ""
		self.handle = handle
		self.o = accessible_output2.outputs.auto.Auto()
		self.rand_id = wx.NewIdRef(count=1)
		self.CurrentSettings = Settings().ReadSettings()


		Panel = wx.Panel(self)
		# Create Menus.
		menubar = wx.MenuBar()
		actions = wx.Menu()
		self.CopyArticleItem = actions.Append(-1, _("Copy article\tctrl+shift+c"))
		self.CopyArticleItem.Enable(enable=False)
		self.CopyArticleLinkItem = actions.Append(-1, _("Copy article link\tctrl+alt+c"))
		self.CopyArticleLinkItem.Enable(enable=False)
		self.SaveArticleItem = actions.Append(-1, _("Save article\tctrl+s"))
		self.SaveArticleItem.Enable(enable=False)
		self.SaveAsHtmlItem = actions.Append(-1, _("Save article as html\tctrl+t"))
		self.SaveAsHtmlItem.Enable(enable=False)
		self.GoToHeading = actions.Append(-1, _("Go to a &heading \tCtrl+h"))
		self.GoToHeading.Enable(enable=False)
		self.ReferencesItem = actions.Append(-1, _("R&eferences of article\tCtrl+r"))
		self.ReferencesItem.Enable(enable=False)
		self.FontItem = actions.Append(-1, _("Change font \tCtrl+d"))
		self.ChangeThemeItem = actions.Append(-1, _("Change theme\tctrl+T"))
		self.CloseArticleItem = actions.Append(-1, _("Close article window\tctrl+w"))
		self.CloseProgramItem = actions.Append(-1, _("Close the program\tctrl+F4"))
		menubar.Append(actions, _("Actions"))
		self.SetMenuBar(menubar)

		self.hotKeys = wx.AcceleratorTable([
			(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("C"), self.CopyArticleItem.GetId()),
			(wx.ACCEL_CTRL+wx.ACCEL_ALT, ord("C"), self.CopyArticleLinkItem.GetId()),
			(wx.ACCEL_CTRL, ord("S"), self.SaveArticleItem.GetId()),
(wx.ACCEL_CTRL, ord("H"), self.GoToHeading.GetId()),
			(wx.ACCEL_CTRL, ord("T"), self.ChangeThemeItem.GetId()),
			(wx.ACCEL_CTRL, ord("W"), self.CloseArticleItem.GetId()),
			(wx.ACCEL_CTRL,wx.WXK_F4, self.CloseProgramItem.GetId()),
			(0, wx.WXK_ESCAPE, self.rand_id),
		])
		Panel.SetAcceleratorTable(self.hotKeys)

		# Create RichEdit to View Article Content
		self.ArticleTitle = wx.StaticText(Panel, -1, _("Please wait."), pos=(10,10), size=(380,30))
		self.ViewArticle = wx.TextCtrl(Panel, -1, pos=(30,40), size=(480,420), style=wx.TE_RICH2+wx.TE_MULTILINE+wx.TE_READONLY)
		#Getting current font and colour for text
		self.font = self.ViewArticle.GetFont()
		self.colour  = self.ViewArticle.GetForegroundColour()

		# Create Buttons
		self.CopyArticle = wx.Button(Panel, -1, _("Copy article\t(ctrl+shift+c)"), pos=(10,500), size=(120,30))
		self.CopyArticle.Enable(enable=False)
		self.SaveArticle = wx.Button(Panel, -1, _("Save article\t(ctrl+s)"), pos=(140,500), size=(120,30))
		self.SaveArticle.Enable(enable=False)
		self.SaveArticle.SetDefault()
		self.CopyArticleLink = wx.Button(Panel, -1, _("Copy article link\t(ctrl+alt+c)"), pos=(270,500), size=(120,30))
		self.CopyArticleLink.Enable(enable=False)
		self.CloseArticle = wx.Button(Panel, -1, _("Close article\t(ctrl+w)"), pos=(400,500), size=(120,30))


		# Show Article window
		self.Show()



		# events for buttons
		self.CopyArticle.Bind(wx.EVT_BUTTON, self.OnCopyArticle)
		self.SaveArticle.Bind(wx.EVT_BUTTON, self.OnSaveArticle)
		self.CopyArticleLink.Bind(wx.EVT_BUTTON, self.OnCopyArticleLink)
		self.CloseArticle.Bind(wx.EVT_BUTTON, self.OnCloseArticle)
		self.Bind(wx.EVT_CLOSE, self.OnCloseArticle)

		# events for Menus
		self.Bind(wx.EVT_MENU, self.OnCopyArticle, self.CopyArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCopyArticleLink, self.CopyArticleLinkItem) 
		self.Bind(wx.EVT_MENU, self.OnSaveArticle, self.SaveArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCloseArticle, self.CloseArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnChangeTheme, self.ChangeThemeItem) 
		self.Bind(wx.EVT_MENU, self.OnCloseProgram, self.CloseProgramItem) 
		self.Bind(wx.EVT_MENU, self.OnGoToheading, self.GoToHeading)
		self.Bind(wx.EVT_MENU, self.OnEscape, id=self.rand_id)
		self.Bind(wx.EVT_MENU, self.OnFont, self.FontItem)
		self.Bind(wx.EVT_MENU, self.OnReferencesItem, self.ReferencesItem)
		self.Bind(wx.EVT_MENU, self.OnSaveAsHtml, self.SaveAsHtmlItem)

	def OpenThread(self):

		try:
			page = wikipedia.page(self.GetValues)
			self.o.speak(_("Loading article:"), interrupt=True)

		#In case the article is no longer available.
		except wikipedia.exceptions.DisambiguationError as e:
			mgb = wx.MessageDialog(self, _("""This article is no longer available.
do you want to show similar results for this  article?
"""), _("Warning"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_QUESTION+wx.ICON_WARNING)
			if mgb.ShowModal() == wx.ID_YES:
				self.Destroy()
				self.handle.ListResults.SetItems(e.options)
			else:
				self.Destroy()
			self.handle.NumberArticle -=1
			return None

		#In case There is no internet connection.
		except :
			wx.MessageBox("There is no internet connection.", "Connection error", style=wx.ICON_ERROR)
			self.Destroy()
			self.handle.NumberArticle -=1
			return None

		#Getting information of article, and show The title and content of it.
		self.title = page.title
		self.Content = page.content
		self.ViewArticle.Value = self.Content
		self.o.speak(_("Article loaded"), interrupt=True)
		self.SetTitle(_("View {}").format(self.title))
		self.ArticleTitle.SetLabel(self.title)
		self.url = page.url
		self.links = page.links
		self.references = page.references
		self.html = page.html()

#Enable menu items
		self.GoToHeading.Enable(enable=True)
		self.CopyArticleItem.Enable(enable=True)
		self.CopyArticleLinkItem.Enable(enable=True)
		self.SaveArticleItem.Enable(enable=True)
		self.CopyArticle.Enable(enable=True)
		self.SaveArticle.Enable(enable=True)
		self.CopyArticleLink.Enable(enable=True)
		self.SaveAsHtmlItem.Enable(enable=True)
		self.ReferencesItem.Enable(enable=True)

	# Copy Article Content
	def OnCopyArticle(self, event):
		pyperclip.copy(self.Content)
		self.o.speak(_("Article copied."), interrupt=False)


	# Copy Article Link
	def OnCopyArticleLink(self, event):
		pyperclip.copy(self.url)
		self.o.speak(_("Article link copied."), interrupt=False)

		# Save Article On a New File.
	def OnSaveArticle(self, event):
		SaveFile = wx.FileDialog(self, _("Save {}:").format(self.title), "self.FilePath", F"{self.title}", style=wx.FD_SAVE+wx.FD_OVERWRITE_PROMPT)
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
		self.handle.NumberArticle -= 1
		self.Destroy()


		# Close Program 
	def OnCloseProgram(self, event):

		state = self.CurrentSettings["close message"]

		if self.handle.NumberArticle == 1:
			ArticleCounte = _("There is 1 open article.")
		elif self.handle.NumberArticle > 1:
			ArticleCounte = _("There are {} open articles.").format(self.handle.NumberArticle)
		if (self.handle.NumberArticle >= 1) and (state == "True"):
			ConfirmClosProgram = wx.MessageDialog(self, _("""{}
Do you want to close the program anyway?""").format(ArticleCounte), "Confirm", style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
			if ConfirmClosProgram.ShowModal() == wx.ID_YES:
								wx.Exit()
			else:
				return
		else:
			wx.Exit()

	def OnGoToheading(self, event):
		position = HeadingsListDialog(self, self.Content).ShowModal()
		if position == wx.ID_CANCEL:
			return None
		self.ViewArticle.SetInsertionPoint(position)
		self.ViewArticle.SetFocus()

	def OnReferencesItem(self, event):
		ReferencesDialog = ReferencesListDialog(self, *self.references)
		threading.Thread(target=ReferencesDialog.OpenThread, daemon=True).start()

	def OnEscape(self, event):

		state = self.CurrentSettings["activ escape"]

		if state == "True":
			self.handle.NumberArticle -= 1
			self.Destroy()
		else:
			pass

#creating OnFont function to change font
	def OnFont(self, event):

		#Set current font and colour in font dialog.
		data = wx.FontData()
		data.EnableEffects(True)
		data.SetInitialFont(self.font)
		data.SetColour(self.colour)

		#Creating font dialog.
		FontDialog = wx.FontDialog(self, data)

		#Getting font and colour information that user will choose.
		if FontDialog.ShowModal() == wx.ID_OK:
			data = FontDialog.GetFontData()
			self.font = data.GetChosenFont()
			self.colour = data.GetColour()

		#Set new font and colour.
			self.ViewArticle.SetFont(self.font)
			self.ViewArticle.SetForegroundColour(self.colour)

	def OnSaveAsHtml(self, event):
		SaveFile = wx.FileDialog(self, _("Save {}:").format(self.title), "self.FilePath", F"{self.title}", style=wx.FD_SAVE+wx.FD_OVERWRITE_PROMPT)
		SaveFile.Wildcard = "Html files (.html)|*.html"
		SaveFileResult = SaveFile.ShowModal()
		if SaveFileResult == wx.ID_OK:
			FilePath = SaveFile.Path
			#FileName = SaveFile.Filename
			file = open(FilePath, "w", encoding="utf-8")
			self.html = DisableLink(self.html)
			file.write(self.html)
			file.close()
		else:
			return
