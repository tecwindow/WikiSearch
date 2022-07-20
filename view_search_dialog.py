#-*- coding: utf-8 -*-
# import project libraries.
import wx
import nlpia2_wikipedia as wikipedia
import threading 
import pyperclip
import webbrowser
from view_article_window import ViewArticleWindow

#create View  Search Dialog
class ViewSearch(wx.Dialog):
	def __init__(self, parent, TextSearch):
		super().__init__(parent, title="search results", size=(300, 400))
		self.Center()
		self.TextSearch = TextSearch

		# Create panel
		Panel = wx.Panel(self)

		# Create ListBox
		wx.StaticText(Panel, -1, "search results", pos=(10,10), size=(380,30))
		self.ListResults = wx.ListBox(Panel, -1, pos=(10,30), size=(290,170))

		# Create Buttons
		self.ViewArticle = wx.Button(Panel, -1, "View Article", pos=(10,235), size=(120,30))
		self.ViewArticle.SetDefault()
		self.OpenInWebBrowser = wx.Button(Panel, -1, "Open in browser", pos=(140,235), size=(120,30))
		self.CopyArticleLink = wx.Button(Panel, -1, "Copy the article link", pos=(10,280), size=(120,30))
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, "GoBack", pos=(140,280), size=(120,30))

		# Show List Results
		self.Show()

		# events for buttons
		self.ViewArticle.Bind(wx.EVT_BUTTON, self.OnViewArticleWindow)
		self.OpenInWebBrowser.Bind(wx.EVT_BUTTON, self.OnOpenInBrowser)
		self.CopyArticleLink.Bind(wx.EVT_BUTTON, self.OnCopyArticleLink)

	#create thread function to show results in list box
	def OpenThread(self):
		try:
			self.ViewResults = wikipedia.search(self.TextSearch, results=20)
		except:
			wx.MessageBox("there is no internet connection ", "Connection error", style=wx.ICON_ERROR)
			return None

		self.ListResults.SetItems(self.ViewResults)
		try:
			self.ListResults.Selection = 0
		except:
			self.Destroy()
			wx.MessageBox("We couldn't find  any articles that match your search", "Error", style=wx.ICON_ERROR)

	#creating OnOpenInBrowser function to open Article Link On Default Browser
	def OnOpenInBrowser(self, event):
		GetValues = self.ViewResults[self.ListResults.GetSelection()]
		url = wikipedia.page(GetValues, auto_suggest=False).url
		webbrowser.open_new(url)

	#Creating OnCopyArticleLink function  to copy Article Link to Clipboard
	def OnCopyArticleLink(self, event):
		GetValues = self.ViewResults[self.ListResults.GetSelection()]
		url = wikipedia.page(GetValues).url
		pyperclip.copy(url)

	#creating OnViewArticleWindow function  View Article On a New Window
	def OnViewArticleWindow(self, event):
		GetValues = self.ListResults.GetString(self.ListResults.GetSelection())
		window1 = ViewArticleWindow(None, GetValues, self)
		thread1 = threading.Thread(target=window1.OpenThread, daemon=True)
		thread1.start()
