#-*- coding: utf-8 -*-
# import project libraries.
import wx
import nlpia2_wikipedia as wikipedia
import threading 
import pyperclip
import webbrowser
import accessible_output2.outputs.auto
from view_article_window import ViewArticleWindow
from settings import Settings
from functions import *

#Set language for View  Search Dialog
_ = SetLanguage(Settings().ReadSettings())

#create View  Search Dialog
class ViewSearch(wx.Dialog):
	def __init__(self, parent, TextSearch):
		super().__init__(parent, title=_("Search results"), size=(300, 400))
		self.Center()
		self.TextSearch = TextSearch
		self.NumberArticle = 0
		self.o = accessible_output2.outputs.auto.Auto()
		# Create panel
		Panel = wx.Panel(self)

		# Create ListBox
		self.ListTitle = wx.StaticText(Panel, -1, _("Search results"), pos=(10,10), size=(380,30))
		self.ListResults = wx.ListBox(Panel, -1, pos=(10,30), size=(290,170))

		# Create Buttons
		self.ViewArticle = wx.Button(Panel, -1, _("View Article\t(Alt+V)"), pos=(10,235), size=(120,30))
		self.ViewArticle.SetDefault()
		self.ViewArticle.Enable(enable=False)
		self.OpenInWebBrowser = wx.Button(Panel, -1, _("Open in browser\t(Alt+O)"), pos=(140,235), size=(120,30))
		self.OpenInWebBrowser.Enable(enable=False)
		self.CopyArticleLink = wx.Button(Panel, -1, _("Copy article link\t(Alt+C)"), pos=(10,280), size=(120,30))
		self.CopyArticleLink.Enable(enable=False)
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("GoBack\t(Alt+B)"), pos=(140,280), size=(120,30))

		self.hotKeys = wx.AcceleratorTable([
			(wx.ACCEL_ALT, ord("V"), self.ViewArticle.GetId()),
			(wx.ACCEL_ALT, ord("O"), self.OpenInWebBrowser.GetId()),
			(wx.ACCEL_ALT, ord("C"), self.CopyArticleLink.GetId()),
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
			RandomArticle = wikipedia.random(pages=RandomArticlesNumber)
			self.ListResults.SetItems(RandomArticle)
			self.ListResults.Selection = 0
			self.ViewArticle.Enable(enable=True)
			self.OpenInWebBrowser.Enable(enable=True)
			self.CopyArticleLink.Enable(enable=True)
			return None

		# in case display search results.
		ResultsNumber = Settings().ReadSettings()["results number"]

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
			self.o.speak(_("Article link copied."), interrupt=False)
		except:
			CantCopy = wx.MessageDialog(self, _("This link cannot be copied."), _("Error"), style=wx.ICON_ERROR)
			CantCopy.SetOKLabel(_("&Ok"))
			CantCopy.ShowModal()
			return

	#creating OnViewArticleWindow function  View Article On a New Window
	def OnViewArticleWindow(self, event):
		GetValues = self.ListResults.GetString(self.ListResults.GetSelection())
		self.NumberArticle += 1
		window1 = ViewArticleWindow(None, GetValues, self)
		thread1 = threading.Thread(target=window1.OpenThread, daemon=True)
		thread1.start()
		thread2 = threading.Thread(target=window1.OpenThread2, daemon=True)
		thread2.start()

