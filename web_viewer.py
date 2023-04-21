#-*- coding: utf-8 -*-
# import project libraries.
import wx
import wx.html2
import nlpia2_wikipedia as wikipedia
import pyperclip
import webbrowser
import accessible_output2.outputs.auto
import os
import re
import mouse
import globals as g
from dialogs import *
from settings import Settings
from functions import *
from my_classes import *


#Set language for View Article window
_ = SetLanguage(Settings().ReadSettings())


#View Article window
class WebViewArticle(wx.Frame):
	def __init__(self, parent, GetValues, handle):
		wx.Frame.__init__(self, parent, title=_("View article"), size=(800, 650))
		self.Center()
		self.GetValues = GetValues
		self.Content = ""
		self.url = ""
		self.title = ""
		self.links = []
		self.references = []
		self.html = _("<h1>Please wait</h1>")
		self.Loaded = False
		self.handle = handle
		self.o = accessible_output2.outputs.auto.Auto()
		self.CurrentSettings = Settings().ReadSettings()
		self.colour = self.GetBackgroundColour()
		g.NumberArticle += 1

		# creating some ID
		self.rand_id = wx.NewIdRef(count=1)
		self.Key1 = wx.NewIdRef(count=1)
		self.Key2 = wx.NewIdRef(count=1)
		self.Key3 = wx.NewIdRef(count=1)
		self.Key4 = wx.NewIdRef(count=1)
		self.Key5 = wx.NewIdRef(count=1)


#Creating panel
		Panel = wx.Panel(self, -1)

		#creating states bar
		self.statusbar = wx.StatusBar(self, -1)
		self.statusbar.SetFieldsCount(6)
		self.SetStatusBar(self.statusbar)

		# Create Menus.
		menubar = wx.MenuBar()
		actions = wx.Menu()
		self.CopyArticleItem = actions.Append(-1, _("&Copy article\tctrl+shift+c"))
		self.CopyArticleItem.Enable(False)
		self.CopyArticleLinkItem = actions.Append(-1, _("&Copy article link\talt+c"))
		self.CopyArticleLinkItem.Enable(False)
		self.AddToFavouritesItem = actions.Append(-1, _("Add to favourites\tctrl+f"))
		self.AddToFavouritesItem.Enable(False)
		GoToMenu = wx.Menu()
		self.ReferencesItem = GoToMenu.Append(-1, _("&References in article\tCtrl+r"))
		self.ReferencesItem.Enable(False)
		self.LinksItem = GoToMenu.Append(-1, _("&Linked articles\tCtrl+l"))
		self.LinksItem.Enable(False)
		actions.AppendSubMenu(GoToMenu, _("Go to"))
		SaveMenu = wx.Menu()
		self.SaveArticleItem = SaveMenu.Append(-1, _("Save article as &txt\tctrl+shift+T"))
		self.SaveArticleItem.Enable(False)
		self.SaveAsHtmlItem = SaveMenu.Append(-1, _("Save article as &html\tctrl+shift+H"))
		self.SaveAsHtmlItem.Enable(False)
		actions.AppendSubMenu(SaveMenu, _("Save article"))
		self.PrintItem = actions.Append(-1, _("&Print\tctrl+P"))
		self.PrintItem.Enable(False)
		self.CloseArticleItem = actions.Append(-1, _("Close article window\tctrl+w"))
		self.CloseProgramItem = actions.Append(-1, _("Close the program\tctrl+F4"))
		menubar.Append(actions, _("Actions"))
		self.SetMenuBar(menubar)


		 #creating web viewer
		self.ArticleTitle = wx.StaticText(Panel, -1, "please wait:")
		self.ViewArticle = wx.html2.WebView.New(Panel, -1, name="")
		self.ViewArticle.SetPage(self.html, "")
		self.ViewArticle.EnableContextMenu(False)
#loading article
		self.LoadArticle = my_threads(target=self.OpenThread, daemon=True)
		self.LoadArticle.start()
		self.LoadArticle2 = my_threads(target=self.OpenThread2, daemon=True)
		self.LoadArticle2.start()

		# Create Buttons
		self.CopyArticle = wx.Button(Panel, -1, _("Copy article"))
		self.CopyArticle.Enable(False)
		self.SaveArticle = wx.Button(Panel, -1, _("Save article"))
		self.SaveArticle.Enable(False)
		self.SaveArticle.SetDefault()
		self.CopyArticleLink = wx.Button(Panel, -1, _("Copy article link"))
		self.CopyArticleLink.Enable(False)
		self.GoTo = wx.Button(Panel, -1, _("Go to"))
		self.GoTo.Enable(False)
		self.CloseArticle = wx.Button(Panel, -1, _("Close article"))

		# Create sizer
		sizer = wx.BoxSizer(wx.VERTICAL)

		# Add widgets to sizer
		sizer.Add(self.ArticleTitle, 0, wx.ALL|wx.ALIGN_CENTER, 5)
		sizer.Add(self.ViewArticle, 1, wx.ALL|wx.EXPAND, 5)

		# Create button sizer
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

		# Add buttons to sizer
		buttonSizer.Add(self.CopyArticle, 0, wx.ALL, 5)
		buttonSizer.Add(self.SaveArticle, 0, wx.ALL, 5)
		buttonSizer.Add(self.CopyArticleLink, 0, wx.ALL, 5)
		buttonSizer.Add(self.GoTo, 0, wx.ALL, 5)
		buttonSizer.Add(self.CloseArticle, 0, wx.ALL, 5)

		# Add button sizer to main sizer
		sizer.Add(buttonSizer, 0, wx.ALL|wx.ALIGN_CENTER, 5)

		# Set sizer for panel
		Panel.SetSizer(sizer)
		Panel.Fit()
		self.Layout()

		# events 
		self.Bind(wx.EVT_CLOSE, self.OnCloseArticle)
		self.Bind(wx.EVT_BUTTON, self.OnCloseArticle, self.CloseArticle)
		self.Bind(wx.EVT_MENU, self.OnCopyArticle, self.CopyArticleItem) 
		self.Bind(wx.EVT_BUTTON, self.OnCopyArticle, self.CopyArticle)
		self.Bind(wx.EVT_MENU, self.OnCopyArticleLink, self.CopyArticleLinkItem) 
		self.Bind(wx.EVT_BUTTON, self.OnCopyArticleLink, self.CopyArticleLink)
		self.Bind(wx.EVT_BUTTON, self.OnGoToMenu, self.GoTo)
		self.Bind(wx.EVT_BUTTON, self.OnSaveArticleMenu, self.SaveArticle)
		self.Bind(wx.EVT_MENU, self.OnFavourites, self.AddToFavouritesItem)
		self.Bind(wx.EVT_MENU, self.OnSaveArticle, self.SaveArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCloseArticle, self.CloseArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCloseProgram, self.CloseProgramItem) 
		self.Bind(wx.EVT_MENU, self.OnEscape, id=self.rand_id)
		self.Bind(wx.EVT_MENU, self.OnReferencesItem, self.ReferencesItem)
		self.Bind(wx.EVT_MENU, self.OnSaveAsHtml, self.SaveAsHtmlItem)
		self.Bind(wx.EVT_MENU, self.OnLinks, self.LinksItem)
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnLoaded, self.timer)
		self.timer.Start(100)
		self.Bind(wx.EVT_MENU, self.OnEscape, id=self.rand_id)
		self.Bind(wx.EVT_MENU, lambda event: self.OnKey(1), self.Key1)
		self.Bind(wx.EVT_MENU, lambda event: self.OnKey(2), self.Key2)
		self.Bind(wx.EVT_MENU, lambda event: self.OnKey(3), self.Key3)
		self.Bind(wx.EVT_MENU, lambda event: self.OnKey(4), self.Key4)
		self.Bind(wx.EVT_MENU, lambda event: self.OnKey(5), self.Key5)
		self.Bind(wx.EVT_MENU, self.on_print, self.PrintItem)

		self.hotKeys = wx.AcceleratorTable((
			(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("C"), self.CopyArticleItem.GetId()),
			(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("H"), self.SaveAsHtmlItem.GetId()),
			(0+wx.ACCEL_ALT, ord("C"), self.CopyArticleLinkItem.GetId()),
			(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("T"), self.SaveArticleItem.GetId()),
(wx.ACCEL_CTRL, ord("P"), self.PrintItem.GetId()),
(wx.ACCEL_CTRL, ord("F"), self.AddToFavouritesItem.GetId()),
			(wx.ACCEL_CTRL, ord("R"), self.ReferencesItem.GetId()),
			(wx.ACCEL_CTRL, ord("L"), self.LinksItem.GetId()),
			(wx.ACCEL_CTRL, ord("W"), self.CloseArticleItem.GetId()),
			(wx.ACCEL_CTRL,wx.WXK_F4, self.CloseProgramItem.GetId()),
			(0, wx.WXK_ESCAPE, self.rand_id),
(0, ord("1"), self.Key1),
(0, ord("2"), self.Key2),
(0, ord("3"), self.Key3),
(0, ord("4"), self.Key4),
(0, ord("5"), self.Key5)
		))
		self.SetAcceleratorTable(self.hotKeys)

		# Show Article window
		self.Show()


	def OpenThread(self):
#mouse click on  wep viewer in order to make it accessible
		self.MakeAccessible()

		try:
			page = wikipedia.page(self.GetValues, auto_suggest=False)
			if not self.o.is_system_output():
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
			g.NumberArticle -=1
			return None

		#In case There is no internet connection.
		except :
			if self.LoadArticle.is_stopped():
				return None
			ConnectionError = wx.MessageDialog(self, _("There is no internet connection."), _("Connection error"), style=wx.ICON_ERROR+wx.OK)
			ConnectionError.SetOKLabel(_("&Ok"))
			ConnectionError.ShowModal()
			self.Destroy()
			g.NumberArticle -=1
			return None

		#Getting information of article, and show The title and content of it.
		self.title = page.title
		self.html = page.html()

		self.SetTitle(f"View {self.title}")
		self.ArticleTitle.SetLabel(self.title)
		self.url = page.url

#Enable menu items
		self.AddToFavouritesItem.Enable(True)
		self.SaveArticleItem.Enable(enable=True)
		self.CopyArticleLinkItem.Enable(enable=True)
		self.SaveAsHtmlItem.Enable(enable=True)
		self.CopyArticleItem.Enable(enable=True)

		# Enable Button
		self.SaveArticle.Enable(True)
		self.CopyArticle.Enable(True)
		self.CopyArticleLink.Enable(True)
		self.GoTo.Enable(True)


	def OpenThread2(self):
		page = wikipedia.page(self.GetValues, auto_suggest=False)
		self.Content = page.content
		# set statusbar
		self.SetStatusbar()
		self.links = page.links
		self.LinksItem.Enable(enable=True)
		self.references = page.references
		self.ReferencesItem.Enable(enable=True)


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

			file = open(FilePath, "w", encoding="utf-8")
			file.write(self.Content)
			file.close()
		else:
			return



	# Close Article Window
	def OnCloseArticle(self, event):
		g.NumberArticle -= 1
		self.LoadArticle.stop()
		self.LoadArticle2.stop()
		self.timer.Stop()
		self.Destroy()


		# Close Program 
	def OnCloseProgram(self, event):
		CurrentSettings = Settings().ReadSettings()
		if g.NumberArticle == 1:
						ArticleCounte = _("There is 1 open article.")
		elif g.NumberArticle > 1:
			ArticleCounte = _("There are {} open articles.").format(g.NumberArticle)
		if (g.NumberArticle >= 1) and (CurrentSettings["close message"] == "True"):
			ConfirmClosProgram = wx.RichMessageDialog(self,_("""{}
Do you want to close the program anyway?""").format(ArticleCounte), _("Confirm"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
			ConfirmClosProgram.ShowCheckBox(_("Don't show that again"))
			ConfirmClosProgram.SetYesNoLabels(_("&Yes"), _("&No"))
			ConfirmClosProgramResult = ConfirmClosProgram.ShowModal()
			if ConfirmClosProgram.IsCheckBoxChecked():
				CurrentSettings["close message"] = "False"
				Settings().WriteSettings(**CurrentSettings)
			if ConfirmClosProgramResult == wx.ID_YES:
				wx.Exit()
				g.Data.CloseConnection()
			else:
				return
		else:
			wx.Exit()
			g.Data.CloseConnection()

	def OnReferencesItem(self, event):
		ReferencesDialog = ReferencesListDialog(self, *self.references)
		threading.Thread(target=ReferencesDialog.OpenThread, daemon=True).start()

	def OnEscape(self, event):

		state = self.CurrentSettings["activ escape"]

		if state == "True":
			g.NumberArticle -= 1
			self.LoadArticle.stop()
			self.LoadArticle2.stop()
			self.timer.Stop()
			self.Destroy()
		else:
			pass


	def OnSaveAsHtml(self, event):
		SaveFile = wx.FileDialog(self, _("Save {}:").format(self.title), "self.FilePath", F"{self.title}", style=wx.FD_SAVE+wx.FD_OVERWRITE_PROMPT)
		SaveFile.Wildcard = "Html files (.html)|*.html"
		SaveFileResult = SaveFile.ShowModal()
		if SaveFileResult == wx.ID_OK:
			FilePath = SaveFile.Path

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

	# creating a function to add the article to favourites table in Database.
	def OnFavourites(self, event):
		name = wx.GetTextFromUser(_("Choose the name of the article in your favourites."), _("Add to Favourites"), default_value=self.title, parent=self)
		if name:
			g.Data.InsertData("FavouritesTable", (self.title, name, self.CurrentSettings ["search language"], self.url))

	# Set the article when it loaded.
	def OnLoaded(self, event):
		if self.html != _("<h1>Please wait</h1>") and not self.Loaded:
			self.html = DisableLink(self.html)
			self.ViewArticle.SetPage(self.html, self.title)
			self.PrintItem.Enable(True)
			if not self.o.is_system_output():
				self.o.speak(_("Article loaded."), interrupt=True)
			self.Loaded = True
			self.timer.Stop()

	def OnGoToMenu(self, event):

		GoToMenu = wx.Menu()

		ArticlesLinkedItem = GoToMenu.Append(-1, _("&Linked articles\tCtrl+l"))
		if self.links == []:
			ArticlesLinkedItem.Enable(False)

		ArticleReferencesItem = GoToMenu.Append(-1, _("&References in article\tCtrl+r"))
		if self.references == []:
			ArticleReferencesItem.Enable(False)

		self.Bind(wx.EVT_MENU, self.OnReferencesItem, ArticleReferencesItem)
		self.Bind(wx.EVT_MENU, self.OnLinks, ArticlesLinkedItem)

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

#mouse click on  wep viewer in order to make it accessible
	def MakeAccessible(self):
		robot = wx.UIActionSimulator() 
		self.ViewArticle.SetFocus()
		position = self.ViewArticle.GetPosition() 
		position = self.ViewArticle.ClientToScreen(position) 
		robot.MouseMove(position) 
		mouse.move(100, 100, absolute=False, duration=0.5)
		mouse.click('left')

	# load ofline article.
	def LoadOflineArticle(self, Article):
		# stop the threads
		self.LoadArticle.stop()
		self.LoadArticle2.stop()

		#make  accessible
		self.MakeAccessible()

	# set the article
		self.SetTitle(Article[0][0])
		self.ArticleTitle.SetLabel(Article[0][0])
		self.title = Article[0][0]
		self.Content = Article[0][3]
		self.html = Article[0][4]
		self.ViewArticle.SetPage(self.html)
		self.url = Article[0][5]
		self.links = Article[0][6].split("\n")
		self.references = Article[0][7].split("\n")

		# set statusbar
		self.SetStatusbar()

#Enable menu items
		self.AddToFavouritesItem.Enable(True)
		self.SaveArticleItem.Enable(enable=True)
		self.CopyArticleLinkItem.Enable(enable=True)
		self.SaveAsHtmlItem.Enable(enable=True)
		self.CopyArticleItem.Enable(enable=True)
		self.LinksItem.Enable(enable=True)
		self.ReferencesItem.Enable(enable=True)
		self.PrintItem.Enable(True)

		# Enable Button
		self.SaveArticle.Enable(True)
		self.CopyArticle.Enable(True)
		self.CopyArticleLink.Enable(True)
		self.GoTo.Enable(True)

	# Creating print function.
	def on_print(self, event):
		# Print the content of the webview
		self.ViewArticle.Print()

	# Set the info to statusbar
	def SetStatusbar(self):
		info = count_text_items(self.Content)
		self.statusbar.SetStatusText(_("Lines: {}.").format(info['lines']), 0)
		self.statusbar.SetStatusText(_("Paragraphs: {}.").format(info['paragraphs']), 1)
		self.statusbar.SetStatusText(_("Sentences: {}.").format(info['sentences']), 2)
		self.statusbar.SetStatusText(_("Words: {}.").format(info['words']), 3)
		self.statusbar.SetStatusText(_("Characters: {}.").format(info['characters']), 5)

	# Making access keys for article information.
	def OnKey(self, Key):
		info = count_text_items(self.Content)
		match Key:
			case 1:
				if not self.o.is_system_output():
					self.o.speak(_(_("Lines: {}.").format(info['lines'])), interrupt=True)
			case 2:
				if not self.o.is_system_output():
					self.o.speak(_("Paragraphs: {}.").format(info['paragraphs']), interrupt=True)
			case 3:
				if not self.o.is_system_output():
					self.o.speak(_("Sentences: {}.").format(info['sentences']), interrupt=True)
			case 4:
				if not self.o.is_system_output():
					self.o.speak(_("Words: {}.").format(info['words']), interrupt=True)
			case 5:
				if not self.o.is_system_output():
					self.o.speak(_("Characters: {}.").format(info['characters']), interrupt=True)
