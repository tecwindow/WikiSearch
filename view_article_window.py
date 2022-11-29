#-*- coding: utf-8 -*-
# import project libraries.
import wx
import wx.adv
import nlpia2_wikipedia as wikipedia
import pyperclip
import webbrowser
import accessible_output2.outputs.auto
import os
import re
import threading 
import requests
from dialogs import *
from settings import Settings
from functions import *
from my_classes import my_threads
from globals import *

#Set language for View Article window
_ = SetLanguage(Settings().ReadSettings())


#View Article window
class ViewArticleWindow(wx.Frame):
	def __init__(self, parent, GetValues, handle):
		wx.Frame.__init__(self, parent, title=_("View article"), size=(900, 720))
		self.Center()
		self.EnableMaximizeButton(False)
		self.GetValues = GetValues
		self.Content = ""
		self.url = ""
		self.title = ""
		self.links = []
		self.references = []
		self.html = ""
		self.handle = handle
		self.o = accessible_output2.outputs.auto.Auto()
		self.rand_id = wx.NewIdRef(count=1)
		self.CurrentSettings = Settings().ReadSettings()
		self.LoadArticle = my_threads(target=self.OpenThread, daemon=True)
		self.LoadArticle.start()
		self.LoadArticle2 = my_threads(target=self.OpenThread2, daemon=True)
		self.LoadArticle2.start()
		self.hotKeys = wx.AcceleratorTable([
			(0, wx.WXK_ESCAPE, self.rand_id)])
		self.SetAcceleratorTable(self.hotKeys)

		self.colour = self.GetBackgroundColour()

		global NumberArticle
		NumberArticle += 1

#Creating panel
		Panel = wx.Panel(self, -1)
		# Create Menus.
		menubar = wx.MenuBar()
		actions = wx.Menu()
		self.CopyArticleItem = actions.Append(-1, _("Copy article\tCtrl+shift+c"))
		self.CopyArticleItem.Enable(False)
		self.CopyArticleLinkItem = actions.Append(-1, _("Copy article link\tAlt+c"))
		self.CopyArticleLinkItem.Enable(False)
		self.AddToFavouritesItem = actions.Append(-1, _("Add to favourites\tAlt+D"))
		self.AddToFavouritesItem.Enable(False)
		GoToMenu = wx.Menu()
		self.GoToHeading = GoToMenu.Append(-1, _("Go to a &heading\tCtrl+h"))
		self.GoToHeading.Enable(False)
		self.LinksItem = GoToMenu.Append(-1, _("&Linked articles\tCtrl+l"))
		self.LinksItem.Enable(False)
		self.ReferencesItem = GoToMenu.Append(-1, _("&References in article\tCtrl+r"))
		self.ReferencesItem.Enable(False)
		self.TablesItem = GoToMenu.Append(-1, _("&Tables in article\tCtrl+t"))
		self.TablesItem.Enable(False)
		actions.AppendSubMenu(GoToMenu, _("Go to"))
		SaveMenu = wx.Menu()
		self.SaveArticleItem = SaveMenu.Append(-1, _("Save article as &txt\tctrl+shift+T"))
		self.SaveArticleItem.Enable(False)
		self.SaveAsHtmlItem = SaveMenu.Append(-1, _("Save article as &html\tctrl+shift+H"))
		self.SaveAsHtmlItem.Enable(False)
		actions.AppendSubMenu(SaveMenu, _("Save article"))
		self.CloseArticleItem = actions.Append(-1, _("Close article window\tctrl+w"))
		self.CloseProgramItem = actions.Append(-1, _("Close the program\tctrl+F4"))
		ViewMenu = wx.Menu()
		self.FontItem = ViewMenu.Append(-1, _("Change &font\tCtrl+d"))
		self.ChangeThemeItem = ViewMenu.Append(-1, _("&Change color\tctrl+shift+d"))
		menubar.Append(actions, _("Actions"))
		menubar.Append(ViewMenu, _("View"))
		self.SetMenuBar(menubar)



		# Create RichEdit to View Article Content
		self.ArticleTitle = wx.StaticText(Panel, -1, _("Please wait."), pos=(10,10), size=(380,30))
		self.ViewArticle = wx.TextCtrl(Panel, -1, pos=(30,40), size=(840,530), style=wx.TE_RICH2+wx.TE_MULTILINE+wx.TE_READONLY)
		#Getting current font and colour for text
		self.font = self.ViewArticle.GetFont()
		self.colour  = self.ViewArticle.GetForegroundColour()

		# Create Buttons
		self.CopyArticle = wx.Button(Panel, -1, _("Copy article"), pos=(10,610), size=(120,30))
		self.CopyArticle.Enable(False)
		self.SaveArticle = wx.Button(Panel, -1, _("Save article"), pos=(140,610), size=(120,30))
		self.SaveArticle.Enable(False)
		self.SaveArticle.SetDefault()
		self.CopyArticleLink = wx.Button(Panel, -1, _("Copy article link"), pos=(270,610), size=(120,30))
		self.CopyArticleLink.Enable(False)
		self.GoTo = wx.Button(Panel, -1, _("Go to"), pos=(400,610), size=(70,30))
		self.GoTo.Enable(False)
		self.CloseArticle = wx.Button(Panel, -1, _("Close article"), pos=(480,610), size=(120,30))

		# events for buttons
		self.CopyArticle.Bind(wx.EVT_BUTTON, self.OnCopyArticle)
		self.SaveArticle.Bind(wx.EVT_BUTTON, self.OnSaveArticleMenu)
		self.CopyArticleLink.Bind(wx.EVT_BUTTON, self.OnCopyArticleLink)
		self.GoTo.Bind(wx.EVT_BUTTON, self.OnGoToMenu)
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
		self.Bind(wx.EVT_MENU, self.OnTablesItem, self.TablesItem)
		self.Bind(wx.EVT_MENU, self.OnFavourites, self.AddToFavouritesItem)

		self.hotKeys = wx.AcceleratorTable((
(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("C"), self.CopyArticleItem.GetId()),
(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("H"), self.SaveAsHtmlItem.GetId()),
(0+wx.ACCEL_ALT, ord("C"), self.CopyArticleLinkItem.GetId()),
(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("T"), self.SaveArticleItem.GetId()),
(wx.ACCEL_CTRL, ord("H"), self.GoToHeading.GetId()),
(wx.ACCEL_CTRL, ord("R"), self.ReferencesItem.GetId()),
(wx.ACCEL_CTRL, ord("L"), self.LinksItem.GetId()),
(wx.ACCEL_CTRL, ord("S"), self.SaveArticle.GetId()),
(wx.ACCEL_CTRL, ord("G"), self.GoTo.GetId()),
(wx.ACCEL_CTRL, ord("T"), self.TablesItem.GetId()),
(wx.ACCEL_CTRL, ord("D"), self.FontItem.GetId()),
(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("D"), self.ChangeThemeItem.GetId()),
(wx.ACCEL_CTRL, ord("W"), self.CloseArticleItem.GetId()),
(wx.ACCEL_CTRL,wx.WXK_F4, self.CloseProgramItem.GetId()),
(0, wx.WXK_ESCAPE, self.rand_id)
))
		self.SetAcceleratorTable(self.hotKeys)

		# Show Article window
		self.Show()


	def OpenThread(self):

		global NumberArticle, ArticleLanguageCode
		try:
			page = wikipedia.page(self.GetValues, auto_suggest=False)
			if not self.o.is_system_output():
				self.o.speak(_("Loading article:"), interrupt=True)

		#In case the article is no longer available.
		except wikipedia.exceptions.DisambiguationError as e:
			mgb = wx.MessageDialog(self, _("""This article is no longer available.
do you want to show similar results for this  article?
"""), _("Warning"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_QUESTION+wx.ICON_WARNING)
			mgb.SetYesNoLabels(_("&Yes"), _("&No"))
			if mgb.ShowModal() == wx.ID_YES:
				self.Destroy()
				self.handle.ListResults.SetItems(e.options)
			else:
				self.Destroy()
			NumberArticle -=1
			return None

		#In case There is no internet connection.
		except :
			if self.LoadArticle.is_stopped():
				return None
			ConnectionError = wx.MessageDialog(self, _("There is no internet connection."), _("Connection error"), style=wx.ICON_ERROR+wx.OK)
			ConnectionError.SetOKLabel(_("&Ok"))
			ConnectionError.ShowModal()
			self.Destroy()
			NumberArticle -=1
			return None

		#Getting title and content of article and show it.
		self.title = page.title
		self.Content = page.content
		try:
			self.ViewArticle.Value = self.Content
		except RuntimeError:
			return None
		self.SetTitle(_("View {}").format(self.title))
		self.ArticleTitle.SetLabel(self.title)
		if not self.o.is_system_output():
			self.o.speak(_("Article loaded."), interrupt=True)
		self.GoToHeading.Enable(True)
		self.CopyArticleItem.Enable(True)
		self.CopyArticle.Enable(True)
		self.SaveArticle.Enable(True)
		self.SaveArticleItem.Enable(True)
	#Getting link of article
		self.url = page.url
		self.CopyArticleLinkItem.Enable(True)
		self.CopyArticleLink.Enable(True)
		self.AddToFavouritesItem.Enable(True)
		self.TablesItem.Enable(True)
	#Getting the Links associated with the article.
		self.links = page.links
		self.LinksItem.Enable(True)
		self.GoTo.Enable(True)


	def OpenThread2(self):
		page = wikipedia.page(self.GetValues, auto_suggest=False)
	#Getting references of article
		self.references = page.references
		self.ReferencesItem.Enable(True)
	#Getting article as html.
		self.html = page.html()
		self.SaveAsHtmlItem.Enable(True)


	# Copy Article Content
	def OnCopyArticle(self, event):
		pyperclip.copy(self.Content)
		if not self.o.is_system_output():
			self.o.speak(_("Article copied."), interrupt=False)


	# Copy Article Link
	def OnCopyArticleLink(self, event):
		pyperclip.copy(self.url)
		if not self.o.is_system_output():
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

		data = wx.ColourData()
		data.SetChooseAlpha(True)
		data.SetColour(self.colour)

		ColourDialog = wx.ColourDialog(self, data )

		if ColourDialog.ShowModal() == wx.ID_OK:
			data = ColourDialog.GetColourData()
			self.colour = data.GetColour()
			self.SetBackgroundColour(self.colour)
			self.Refresh()

	# Close Article Window
	def OnCloseArticle(self, event):
		global NumberArticle
		NumberArticle -= 1
		self.LoadArticle.stop()
		self.LoadArticle2.stop()
		self.Destroy()



		# Close Program 
	def OnCloseProgram(self, event):

		state = self.CurrentSettings["close message"]

		global Data, NumberArticle
		if NumberArticle == 1:
			ArticleCounte = _("There is 1 open article.")
		elif NumberArticle > 1:
			ArticleCounte = _("There are {} open articles.").format(NumberArticle)
		if (NumberArticle >= 1) and (state == "True"):
			ConfirmClosProgram = wx.MessageDialog(self, _("""{}
Do you want to close the program anyway?""").format(ArticleCounte), _("Confirm"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
			ConfirmClosProgram.SetYesNoLabels(_("&Yes"), _("&No"))
			if ConfirmClosProgram.ShowModal() == wx.ID_YES:
								wx.Exit()
								Data.CloseConnection()
			else:
				return
		else:
			wx.Exit()
			Data.CloseConnection()

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

		global NumberArticle
		if state == "True":
			NumberArticle -= 1
			self.LoadArticle.stop()
			self.LoadArticle2.stop()
			self.Destroy()
		else:
			pass

	def OnGoToMenu(self, event):

		GoToMenu = wx.Menu()

		GoToHeadingItem = GoToMenu.Append(-1, _("Go to a &heading\tCtrl+h"))
		if self.Content == "":
			GoToHeadingItem.Enable(False)

		ArticlesLinkedItem = GoToMenu.Append(-1, _("&Linked articles\tCtrl+l"))
		if self.links == []:
			ArticlesLinkedItem.Enable(False)

		ArticleReferencesItem = GoToMenu.Append(-1, _("&References in article\tCtrl+r"))
		if self.references == []:
			ArticleReferencesItem.Enable(False)

		ArticleTablesItem = GoToMenu.Append(-1, _("&Tables in article\tCtrl+t"))
		if self.url == "":
			ArticleTablesItem.Enable(False)

		self.Bind(wx.EVT_MENU, self.OnGoToheading, GoToHeadingItem)
		self.Bind(wx.EVT_MENU, self.OnReferencesItem, ArticleReferencesItem)
		self.Bind(wx.EVT_MENU, self.OnLinks, ArticlesLinkedItem)
		self.Bind(wx.EVT_MENU, self.OnTablesItem, ArticleTablesItem)
		self.PopupMenu(GoToMenu)


	def OnSaveArticleMenu(self, event):

		SaveMenu = wx.Menu()

		SaveArticleItem = SaveMenu.Append(-1, _("Save article as &txt\tctrl+shift+T"))
		if self.Content == "":
			SaveArticleItem.Enable(False)

		SaveAsHtmlItem = SaveMenu.Append(-1, _("Save article as &html\tctrl+shift+H"))
		if self.html == "":
			SaveAsHtmlItem.Enable(False)

		self.Bind(wx.EVT_MENU, self.OnSaveArticle, SaveArticleItem)
		self.Bind(wx.EVT_MENU, self.OnSaveAsHtml, SaveAsHtmlItem)
		self.PopupMenu(SaveMenu)


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
		ArticleLinksDialog.SetTitle(_("Linked articles"))
		ArticleLinksDialog.ListTitle.SetLabel(_("Linked articles"))
		#adding the links to list in the dialog.
		ArticleLinksDialog.ListResults.SetItems(self.links)
		ArticleLinksDialog.ListResults.Selection = 0
		#Enable buttons in the dialog.
		ArticleLinksDialog.ViewArticle.Enable(True)
		ArticleLinksDialog.OpenInWebBrowser.Enable(True)
		ArticleLinksDialog.CopyArticleLink.Enable(True)



	def OnTablesItem(self, event):
		ViewTablesDialog(self, self.url, self.title)

	# creating a function to add the article to favourites table in Database.
	def OnFavourites(self, event):
		name = wx.GetTextFromUser(_("Choose the name of the article in your favourites."), _("Add to Favourites"), default_value=self.title, parent=self)
		if name:
			global Data, ArticleLanguageCode
			Data.InsertData("FavouritesTable", (self.title, name, self.CurrentSettings ["search language"], ArticleLanguageCode, self.url))

