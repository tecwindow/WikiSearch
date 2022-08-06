#-*- coding: utf-8 -*-
# import project libraries.
import wx
import wx.html2
import nlpia2_wikipedia as wikipedia
import pyperclip
import webbrowser
import accessible_output2.outputs.auto
import os
import shutil
import mouse
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
class WepViewArticle(wx.Frame):
	def __init__(self, parent, GetValues, handle):
		super().__init__(parent, title=_("View article"), size=(560, 600))
		self.Center()
		self.EnableMaximizeButton(False)
		self.GetValues = GetValues
		self.Content = ""
		self.url = ""
		self.title = ""
		self.links = []
		self.references = []
		self.html = "<h1>please wait</h1>"
		self.handle = handle
		self.o = accessible_output2.outputs.auto.Auto()
		self.rand_id = wx.NewIdRef(count=1)
		self.CurrentSettings = Settings().ReadSettings()
		self.temp = os.path.join(os.getenv("temp"), "WikiSearch")
		self.FileName = self.title + ".html"
		self.path = os.path.join(self.temp, self.FileName)
		if not os.path.exists(self.temp):
			os.mkdir(self.temp)

		Panel = wx.Panel(self)
		# Create Menus.
		menubar = wx.MenuBar()
		actions = wx.Menu()
		self.CopyArticleItem = actions.Append(-1, _("Copy article\tctrl+shift+c"))
		self.CopyArticleItem.Enable(enable=False)
		self.CopyArticleLinkItem = actions.Append(-1, _("Copy article link\tctrl+alt+c"))
		self.CopyArticleLinkItem.Enable(enable=False)
		GoToMenu = wx.Menu()
		self.GoToHeading = GoToMenu.Append(-1, _("Go to a &heading \tCtrl+h"))
		self.GoToHeading.Enable(enable=False)
		self.ReferencesItem = GoToMenu.Append(-1, _("&References of article\tCtrl+r"))
		self.ReferencesItem.Enable(enable=False)
		self.LinksItem = GoToMenu.Append(-1, _("&Links of article\tCtrl+l"))
		self.LinksItem.Enable(enable=False)
		actions.AppendSubMenu(GoToMenu, _("&Go To"))
		SaveMenu = wx.Menu()
		self.SaveArticleItem = SaveMenu.Append(-1, _("Save article as &txt\tctrl+s"))
		self.SaveArticleItem.Enable(enable=False)
		self.SaveAsHtmlItem = SaveMenu.Append(-1, _("Save article as &html\tctrl+t"))
		self.SaveAsHtmlItem.Enable(enable=False)
		actions.AppendSubMenu(SaveMenu, _("&Save"))
		self.CloseArticleItem = actions.Append(-1, _("Close article window\tctrl+w"))
		self.CloseProgramItem = actions.Append(-1, _("Close the program\tctrl+F4"))
		ViewMenu = wx.Menu()
		self.FontItem = ViewMenu.Append(-1, _("Change &font\tCtrl+d"))
		self.ChangeThemeItem = ViewMenu.Append(-1, _("Change &theme\tctrl+T"))
		menubar.Append(actions, _("Actions"))
		menubar.Append(ViewMenu, _("View"))
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

		# creating wepviewer
		self.ArticleTitle = wx.StaticText(Panel, -1, "please wait:", pos=(10,10), size=(380,30))
		self.ViewArticle = wx.html2.WebView.New(Panel, -1, pos=(30,40), size=(480,420))
		self.ViewArticle.SetPage(self.html, "")
		self.ViewArticle.EnableContextMenu(False)

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
		self.Bind(wx.EVT_MENU, self.OnLinks, self.LinksItem)
		self.Bind(wx.html2.EVT_WEBVIEW_LOADED, lambda event: self.o.speak(_("Article loaded"), interrupt=True))

	def OpenThread(self):

#mouse click on  wep viewer in order to make it accessible
		robot = wx.UIActionSimulator() 
		self.ViewArticle.SetFocus()
		position = self.ViewArticle.GetPosition() 
		position = self.ViewArticle.ClientToScreen(position) 
		robot.MouseMove(position) 
		robot.MouseClick(True)
		mouse.click('left')
		mouse.move(100, 100, absolute=False, duration=0.5)

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
		self.html = page.html()
		self.html = DisableLink(self.html)
		self.SetTitle(f"View {self.title}")
		with open(self.path, "w", encoding="utf-16") as f:
			f.write(self.html)
		self.ViewArticle.LoadURL(self.path)
		self.url = page.url
		self.Content = page.content

#Enable menu items
		self.GoToHeading.Enable(enable=True)
		self.CopyArticleItem.Enable(enable=True)
		self.CopyArticleLinkItem.Enable(enable=True)
		self.SaveArticleItem.Enable(enable=True)
		self.SaveAsHtmlItem.Enable(enable=True)
		self.CopyArticle.Enable(enable=True)
		self.SaveArticle.Enable(enable=True)
		self.CopyArticleLink.Enable(enable=True)

	def OpenThread2(self):
		page = wikipedia.page(self.GetValues)
		self.links = page.links
		self.LinksItem.Enable(enable=True)
		self.references = page.references
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
		shutil.rmtree(self.temp, ignore_errors=False)
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
				shutil.rmtree(self.temp, ignore_errors=False)
			else:
				return
		else:
			wx.Exit()
			shutil.rmtree(self.temp, ignore_errors=False)

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

	def OnLinks(self, event):

		from view_search_dialog import ViewSearch

		# Show dialog of article links
		ArticleLinksDialog  = ViewSearch(self, None)
		ArticleLinksDialog.SetTitle(_("Article links"))
		ArticleLinksDialog.ListTitle.SetLabel(_("Article links"))
#adding the links to list in the dialog.
		ArticleLinksDialog.ListResults.SetItems(self.links)
#Enable buttons in the dialog.
		ArticleLinksDialog.ViewArticle.Enable(enable=True)
		ArticleLinksDialog.OpenInWebBrowser.Enable(enable=True)
		ArticleLinksDialog.CopyArticleLink.Enable(enable=True)

