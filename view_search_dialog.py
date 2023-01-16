#-*- coding: utf-8 -*-
# import project libraries.
import wx
import nlpia2_wikipedia as wikipedia
import threading 
import pyperclip
import webbrowser
import accessible_output2.outputs.auto
import datetime
import globals as g
from view_article_window import ViewArticleWindow
from web_viewer import WebViewArticle
from settings import Settings
from functions import *


#Set language for View  Search Dialog
_ = SetLanguage(Settings().ReadSettings())

#create View  Search Dialog
class ViewSearch(wx.Dialog):
	def __init__(self, parent, TextSearch):
		wx.Dialog.__init__(self, parent, title=_("Search results"), size=(450, 400))
		self.CenterOnParent()
		self.TextSearch = TextSearch
		self.o = accessible_output2.outputs.auto.Auto()

		# Create panel
		Panel = wx.Panel(self)

		# Create ListBox
		self.ListTitle = wx.StaticText(Panel, -1, _("Search results"))
		self.ListResults = wx.ListBox(Panel, -1)

		# Create Buttons
		self.ViewArticle = wx.Button(Panel, -1, _("&View Article"))
		self.ViewArticle.SetDefault()
		self.ViewArticle.Enable(enable=False)
		self.OpenInWebBrowser = wx.Button(Panel, -1, _("&Open in browser"))
		self.OpenInWebBrowser.Enable(enable=False)
		self.CopyArticleLink = wx.Button(Panel, -1, _("&Copy article link"))
		self.CopyArticleLink.Enable(enable=False)
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("Go&Back"))

		# Create main sizer
		sizer = wx.BoxSizer(wx.VERTICAL)

		# Add widgets to sizer
		sizer.Add(self.ListTitle, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		sizer.Add(self.ListResults, 2, wx.EXPAND|wx.ALL, 5)

		# Create horizontal sizer.
		button_sizer = wx.BoxSizer(wx.HORIZONTAL)

		# Add buttons to horizontal sizer
		button_sizer.Add(self.ViewArticle, 0, wx.ALL, 5)
		button_sizer.Add(self.OpenInWebBrowser, 0, wx.ALL, 5)
		button_sizer.Add(self.CopyArticleLink, 0, wx.ALL, 5)
		button_sizer.Add(self.GoBack, 0, wx.ALL, 5)

		# Add horizontal sizer to vertical sizer
		sizer.Add(button_sizer, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

		# Set sizer for panel
		Panel.SetSizer(sizer)
		Panel.Fit()

		self.hotKeys = wx.AcceleratorTable([
			(wx.ACCEL_ALT, ord("V"), self.ViewArticle.GetId()),
			(wx.ACCEL_ALT, ord("O"), self.OpenInWebBrowser.GetId()),
			(wx.ACCEL_ALT, ord("C"), self.CopyArticleLink.GetId()),
			(wx.ACCEL_CTRL, ord("W"), self.GoBack.GetId()),
			(wx.ACCEL_ALT, ord("B"), self.GoBack.GetId()),
		])
		Panel.SetAcceleratorTable(self.hotKeys)

		# Show List Results
		self.Show()

		# events for buttons
		self.ViewArticle.Bind(wx.EVT_BUTTON, self.OnViewArticleWindow)
		self.OpenInWebBrowser.Bind(wx.EVT_BUTTON, self.OnOpenInBrowser)
		self.CopyArticleLink.Bind(wx.EVT_BUTTON, self.OnCopyArticleLink)


	#create thread function to show results in list box
	def OpenThread(self):

		# in case display random articles.
		if not self.TextSearch:
			self.ListTitle.SetLabel(_("Random articles"))
			self.SetTitle(_("View random articles"))
			RandomArticlesNumber = Settings().ReadSettings()["random articles number"]
			if int(Settings().ReadSettings()["random articles number"]) >100:
				RandomArticlesNumber = 100
			RandomArticle = wikipedia.random(pages=RandomArticlesNumber)
			self.ListResults.SetItems(RandomArticle)
			self.ListResults.Selection = 0
			self.ViewArticle.Enable(enable=True)
			self.OpenInWebBrowser.Enable(enable=True)
			self.CopyArticleLink.Enable(enable=True)
			return None

		# in case display search results.
		ResultsNumber = Settings().ReadSettings()["results number"]
		if int(Settings().ReadSettings()["results number"]) > 100:
			ResultsNumber = 100

		try:
			self.ViewResults = wikipedia.search(self.TextSearch, results=ResultsNumber)
		except:
			ConnectionError = wx.MessageDialog(self, _("There is no internet connection."), _("Connection error"), style=wx.ICON_ERROR+wx.OK)
			ConnectionError.SetOKLabel(_("&Ok"))
			ConnectionError.ShowModal()
			return None

		self.ListResults.SetItems(self.ViewResults)
		try:
			self.ListResults.Selection = 0
		except:
			UnableToFind = wx.MessageDialog(None, _("We couldn't find  any articles that match your search."), _("Error"), style=wx.ICON_ERROR+wx.OK)
			UnableToFind.SetOKLabel(_("&Ok"))
			UnableToFind.ShowModal()
			self.Close()

		self.ViewArticle.Enable(enable=True)
		self.OpenInWebBrowser.Enable(enable=True)
		self.CopyArticleLink.Enable(enable=True)

	#creating OnOpenInBrowser function to open Article Link On Default Browser
	def OnOpenInBrowser(self, event):
		GetValues = self.ListResults.GetString(self.ListResults.GetSelection())
		try:
			url = wikipedia.page(GetValues).url
			webbrowser.open_new(url)
			if not self.o.is_system_output():
				self.o.speak(_("Opening:"), interrupt=False)
		except:
			CantOpen = wx.MessageDialog(self, _("This link cannot be opened in the browser."), _("Error"), style=wx.ICON_ERROR+wx.OK)
			CantOpen.SetOKLabel(_("&Ok"))
			CantOpen.ShowModal()
			return


	#Creating OnCopyArticleLink function  to copy Article Link to Clipboard
	def OnCopyArticleLink(self, event):
		GetValues = self.ListResults.GetString(self.ListResults.GetSelection())
		try:
			url = wikipedia.page(GetValues).url
			pyperclip.copy(url)
			if not self.o.is_system_output():
				self.o.speak(_("Article link copied."), interrupt=False)
		except:
			CantCopy = wx.MessageDialog(self, _("This link cannot be copied."), _("Error"), style=wx.ICON_ERROR)
			CantCopy.SetOKLabel(_("&Ok"))
			CantCopy.ShowModal()
			return

	#creating OnViewArticleWindow function  View Article On a New Window
	def OnViewArticleWindow(self, event):

		GetValues = self.ListResults.GetString(self.ListResults.GetSelection())
		CurrentSettings = Settings().ReadSettings()
		state = CurrentSettings["wepviewer"]
		ArticleLanguageName = CurrentSettings["search language"]

		if state == "0":
			window1 = ViewArticleWindow(None, GetValues, self)
		else:
			window1 = WebViewArticle(None, GetValues, self)

		# Check if the article is saved in the database.
		SavedArticle = g.Data.SearchData("SavedArticlesTable", "Title", GetValues)
		if SavedArticle:
			window1.LoadOflineArticle(SavedArticle)
			return

		#adding the article to history.
		#Getting the date and time of visit article.
		date = datetime.date.today()
		time = datetime.datetime.now()
		time = time.strftime("%H:%M:%S")
		g.Data.InsertData("HistoryTable", (GetValues, str(date), str(time), ArticleLanguageName))




