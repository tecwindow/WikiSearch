#-*- coding: utf-8 -*-
# import project libraries.
import wx
import wx.adv
import nlpia2_wikipedia as wikipedia
import pyperclip
import webbrowser
import accessible_output2.outputs.auto
import os
import threading 
import requests
import globals as g
from dialogs import *
from settings import Settings
from functions import *
from my_classes import *


#Set language for View Article window
_ = SetLanguage(Settings().ReadSettings())


#View Article window
class ViewArticleWindow(wx.Frame):
	def __init__(self, parent, GetValues, handle):
		wx.Frame.__init__(self, parent, title=_("View article"), size=(900, 720))
		self.Center()
		self.GetValues = GetValues
		self.Content = ""
		self.url = ""
		self.title = ""
		self.links = []
		self.references = []
		self.html = ""
		self.tables = ""
		self.handle = handle
		self.o = accessible_output2.outputs.auto.Auto()
		self.CurrentSettings = Settings().ReadSettings()
		self.LoadArticle = my_threads(target=self.OpenThread, daemon=True)
		self.LoadArticle.start()
		self.LoadArticle2 = my_threads(target=self.OpenThread2, daemon=True)
		self.LoadArticle2.start()

		# creating some ID
		self.rand_id = wx.NewIdRef(count=1)
		self.Key1 = wx.NewIdRef(count=1)
		self.Key2 = wx.NewIdRef(count=1)
		self.Key3 = wx.NewIdRef(count=1)
		self.Key4 = wx.NewIdRef(count=1)
		self.Key5 = wx.NewIdRef(count=1)
		self.hotKeys = wx.AcceleratorTable([
			(0, wx.WXK_ESCAPE, self.rand_id)])
		self.SetAcceleratorTable(self.hotKeys)

		self.colour = self.GetBackgroundColour()

		g.NumberArticle += 1

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
		self.AddToSavedItem = actions.Append(-1, _("Add to saved articles\tctrl+shift+s"))
		self.AddToSavedItem.Enable(False)
		GoToMenu = wx.Menu()
		self.GoToHeading = GoToMenu.Append(-1, _("&Headings in article\tCtrl+h"))
		self.GoToHeading.Enable(False)
		self.ReferencesItem = GoToMenu.Append(-1, _("&References in article\tCtrl+r"))
		self.ReferencesItem.Enable(False)
		self.TablesItem = GoToMenu.Append(-1, _("&Tables in article\tCtrl+t"))
		self.TablesItem.Enable(False)
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
		ViewMenu = wx.Menu()
		self.FontItem = ViewMenu.Append(-1, _("Change &font\tCtrl+d"))
		self.ChangeThemeItem = ViewMenu.Append(-1, _("&Change color\tctrl+shift+d"))
		menubar.Append(actions, _("Actions"))
		menubar.Append(ViewMenu, _("View"))
		self.SetMenuBar(menubar)



		# Create RichEdit to View Article Content
		self.ArticleTitle = wx.StaticText(Panel, -1, _("Please wait."))
		self.ViewArticle = wx.TextCtrl(Panel, -1, style=wx.TE_RICH2+wx.TE_MULTILINE+wx.TE_READONLY)
		#Getting current font and colour for text
		self.font = self.ViewArticle.GetFont()
		self.colour  = self.ViewArticle.GetForegroundColour()

		# Create Buttons
		self.SaveArticle = wx.Button(Panel, -1, _("Save article"))
		self.SaveArticle.Enable(False)
		self.SaveArticle.SetDefault()
		self.CopyArticle = wx.Button(Panel, -1, _("Copy article"))
		self.CopyArticle.Enable(False)
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

		# events for buttons
		self.CopyArticle.Bind(wx.EVT_BUTTON, self.OnCopyArticle)
		self.SaveArticle.Bind(wx.EVT_BUTTON, self.OnSaveArticleMenu)
		self.CopyArticleLink.Bind(wx.EVT_BUTTON, self.OnCopyArticleLink)
		self.GoTo.Bind(wx.EVT_BUTTON, self.OnGoToMenu)
		self.CloseArticle.Bind(wx.EVT_BUTTON, self.OnCloseArticle)

		# events for Menus
		self.Bind(wx.EVT_MENU, self.on_print, self.PrintItem)
		self.Bind(wx.EVT_MENU, self.OnCopyArticle, self.CopyArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCopyArticleLink, self.CopyArticleLinkItem) 
		self.Bind(wx.EVT_MENU, self.OnSaveArticle, self.SaveArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCloseArticle, self.CloseArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnChangeTheme, self.ChangeThemeItem) 
		self.Bind(wx.EVT_MENU, self.OnCloseProgram, self.CloseProgramItem) 
		self.Bind(wx.EVT_MENU, self.OnGoToheading, self.GoToHeading)
		self.Bind(wx.EVT_MENU, self.OnFont, self.FontItem)
		self.Bind(wx.EVT_MENU, self.OnReferencesItem, self.ReferencesItem)
		self.Bind(wx.EVT_MENU, self.OnSaveAsHtml, self.SaveAsHtmlItem)
		self.Bind(wx.EVT_MENU, self.OnLinks, self.LinksItem)
		self.Bind(wx.EVT_MENU, self.OnTablesItem, self.TablesItem)
		self.Bind(wx.EVT_MENU, self.OnFavourites, self.AddToFavouritesItem)
		self.Bind(wx.EVT_MENU, self.OnSavedArticles, self.AddToSavedItem)

		# general events
		self.Bind(wx.EVT_CLOSE, self.OnCloseArticle)
		self.Bind(wx.EVT_MENU, self.OnEscape, id=self.rand_id)
		self.Bind(wx.EVT_MENU, lambda event: self.OnKey(1), self.Key1)
		self.Bind(wx.EVT_MENU, lambda event: self.OnKey(2), self.Key2)
		self.Bind(wx.EVT_MENU, lambda event: self.OnKey(3), self.Key3)
		self.Bind(wx.EVT_MENU, lambda event: self.OnKey(4), self.Key4)
		self.Bind(wx.EVT_MENU, lambda event: self.OnKey(5), self.Key5)


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
(wx.ACCEL_CTRL, ord("P"), self.PrintItem.GetId()),
(wx.ACCEL_CTRL, ord("F"), self.AddToFavouritesItem.GetId()),
(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("S"), self.AddToSavedItem.GetId()),
(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("D"), self.ChangeThemeItem.GetId()),
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
		# set statusbar
		self.SetStatusbar()
		self.GoToHeading.Enable(True)
		self.CopyArticleItem.Enable(True)
		self.CopyArticle.Enable(True)
		self.SaveArticle.Enable(True)
		self.SaveArticleItem.Enable(True)
		self.PrintItem.Enable(True)
	#Getting link of article
		self.url = page.url
		self.CopyArticleLinkItem.Enable(True)
		self.CopyArticleLink.Enable(True)
		self.tables = GetTables(self.url)
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
		self.AddToSavedItem.Enable(True)

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
		g.NumberArticle -= 1
		self.LoadArticle.stop()
		self.LoadArticle2.stop()
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
			g.NumberArticle -= 1
			self.LoadArticle.stop()
			self.LoadArticle2.stop()
			self.Destroy()
		else:
			pass

	def OnGoToMenu(self, event):

		GoToMenu = wx.Menu()

		GoToHeadingItem = GoToMenu.Append(-1, _("&Headings in article\tCtrl+h"))
		if self.Content == "":
			GoToHeadingItem.Enable(False)

		ArticleReferencesItem = GoToMenu.Append(-1, _("&References in article\tCtrl+r"))
		if self.references == []:
			ArticleReferencesItem.Enable(False)

		ArticleTablesItem = GoToMenu.Append(-1, _("&Tables in article\tCtrl+t"))
		if self.url == "":
			ArticleTablesItem.Enable(False)

		ArticlesLinkedItem = GoToMenu.Append(-1, _("&Linked articles\tCtrl+l"))
		if self.links == []:
			ArticlesLinkedItem.Enable(False)

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
		# call view tables dialog
		TablesDialog = ViewTablesDialog(self, self.title)
		# convert list of tables to str
		tables = ""
		for n,table in enumerate(self.tables):
			tables += _("Table {}:\n {}").format(n+1, table)
		# write the tables in text ctrl.
			TablesDialog.ViewArticleTables.Value = tables

	# creating a function to add the article to favourites table in Database.
	def OnFavourites(self, event):
		# delete the article if is exists to prevent recurrence.
		if g.Data.SearchData("FavouritesTable", "Title", self.title):
			g.Data.DeleteItem("FavouritesTable", "Title", self.title)

		# Getting the article name from SavedArticlesTable if it is exists.
		name = g.Data.SearchData("SavedArticlesTable", "Title", self.title)
		# Show dialog to choose the name if it is not exists.
		if not name:
			AddToFavouriteDialog = wx.TextEntryDialog(self, _("Choose the name of the article in your favourites."), _("Add to Favourites"), self.title)
			AddToFavouriteDialog.GetChildren()[-3].SetLabel(_("&Add"))
			AddToFavouriteDialog.GetChildren()[-2].SetLabel(_("&Cancel"))
			# if the user press add.
			if AddToFavouriteDialog.ShowModal() == wx.ID_OK:
					name = AddToFavouriteDialog.GetValue()
					if name == "":
						self.OnFavourites(None)
						return
			# if the user press cancel.
			else:
				return
			# if the article is there in saved articles table.
		else:
			name = name[0][1]

		# inserting the data.
		g.Data.InsertData("FavouritesTable", (self.title, name, self.CurrentSettings["search language"], self.url))

		if not self.o.is_system_output():
			self.o.speak(_("The article has been added to favourites."), interrupt=True)

	# creating a function to add the article to saved articles table in Database.
	def OnSavedArticles(self, event):
# delete the article if is exists to prevent recurrence.
		if g.Data.SearchData("   SavedArticlesTable", "Title", self.title):
			g.Data.DeleteItem("SavedArticlesTable", "Title", self.title)

		# Getting the article name from SavedArticlesTable if it is exists.
		name = g.Data.SearchData("FavouritesTable", "Title", self.title)
		if not name:
			AddToSavedArticlesDialog = wx.TextEntryDialog(self, _("Choose the name of the article in your saved articles."), _("Add to saved articles"), self.title)
			AddToSavedArticlesDialog.GetChildren()[-3].SetLabel(_("&Add"))
			AddToSavedArticlesDialog.GetChildren()[-2].SetLabel(_("&Cancel"))
			# if the user press add.
			if AddToSavedArticlesDialog.ShowModal() == wx.ID_OK:
					name = AddToSavedArticlesDialog.GetValue()
					if name == "":
						self.OnSavedArticles(None)
						return
			# if the user press cancel.
			else:
				return
			# if the article is there in favourites table.
		else:
			name = name[0][1]

		links = ""
		for l in self.links:
			links += l + "\n"

		references = ""
		for r in self.references:
			references += r + "\n"

		tables = ""
		for n,table in enumerate(self.tables):
			tables += _("Table {}:\n {}").format(n+1, table)

		sql = '''INSERT INTO SavedArticlesTable VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
		row = (self.title, name, self.CurrentSettings["search language"], self.Content, self.html, self.url, links, references, tables)
		g.Data.cursor.execute(sql, row)
		g.Data.conn.commit()

		if not self.o.is_system_output():
			self.o.speak(_("The article has been added to your saved articles."), interrupt=True)

	# load ofline article.
	def LoadOflineArticle(self, Article):
		# stop the threads
		self.LoadArticle.stop()
		self.LoadArticle2.stop()

	# set the article
		self.SetTitle(Article[0][0])
		self.ArticleTitle.SetLabel(Article[0][0])
		self.title = Article[0][0]
		self.Content = Article[0][3]
		self.ViewArticle.Value = self.Content
		self.html = Article[0][4]
		self.url = Article[0][5]
		self.links = Article[0][6].split("\n")
		self.references = Article[0][7].split("\n")
		self.tables = Article[0][8]

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
		self.GoToHeading.Enable(True)
		self.TablesItem.Enable(True)
		self.PrintItem.Enable(True)
		# Enable Buttons
		self.SaveArticle.Enable(True)
		self.CopyArticle.Enable(True)
		self.CopyArticleLink.Enable(True)
		self.GoTo.Enable(True)

	# Creating print function.
	def on_print(self, event):
        # get the text from the TextCtrl
		text = self.ViewArticle.Value

		# create a TextPrintout object
		printout = TextPrintout(text, self.font )

		# create a wx.PrintData object to hold the printing settings
		print_data = wx.PrintData()
		print_data.SetQuality(wx.PRINT_QUALITY_HIGH)
		print_data.SetFilename(self.title)
		print_data.SetPrintMode(wx.PRINT_MODE_PRINTER)

		# create a wx.PrintDialogData object to hold the print dialog settings
		print_dialog_data = wx.PrintDialogData(print_data)

        # create a wx.Printer object
		printer = wx.Printer(print_dialog_data)
		printer.Print(self, printout)

	#	 Set the info to statusbar
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
