#-*- coding: utf-8 -*-
# import project libraries.
import wx
import nlpia2_wikipedia as wikipedia
import accessible_output2.outputs.auto
import pyperclip
import webbrowser
import globals as g
from  my_classes import my_threads
from settings import Settings
from functions import *


#Set language  for Headings List Dialog
_ = SetLanguage(Settings().ReadSettings())

#creating references List Dialog
class ReferencesListDialog(wx.Dialog):
	def __init__(self, parent, *references ):
		wx.Dialog.__init__(self, parent, title=_("Article references"), size=(300, 320))
		self.Center()
		self.references = references

		# Create panel
		Panel = wx.Panel(self)

		# Create ListBox
		self.ReferencesListTitle = wx.StaticText(Panel, -1, _("Article references"))
		self.ReferencesList = wx.ListBox(Panel, -1)

		# Create Buttons
		self.Go = wx.Button(Panel, -1, _("&Open in browser"))
		self.Go.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"))

		# Create sizer
		sizer = wx.BoxSizer(wx.VERTICAL)

		# Add widgets to sizer
		sizer.Add(self.ReferencesListTitle, 0, wx.ALL|wx.ALIGN_CENTER, 5)
		sizer.Add(self.ReferencesList, 1, wx.ALL|wx.EXPAND, 5)

		# Create button sizer
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

		# Add buttons to sizer
		buttonSizer.Add(self.Go, 0, wx.ALL, 5)
		buttonSizer.Add(self.GoBack, 0, wx.ALL, 5)

		# Add button sizer to main sizer
		sizer.Add(buttonSizer, 0, wx.ALL|wx.ALIGN_CENTER, 5)

		# Set sizer for panel
		Panel.SetSizer(sizer)
		Panel.Fit()

		self.hotKeys = wx.AcceleratorTable((
(wx.ACCEL_CTRL, ord("W"), self.GoBack.GetId()),
(wx.ACCEL_ALT, ord("O"), self.Go.GetId()),
))
		Panel.SetAcceleratorTable(self.hotKeys)


#Event of go button 
		self.Go.Bind(wx.EVT_BUTTON, self.OnGo)

#Show dialog
		self.Show()

	def OpenThread(self):

		pattern = r'^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)'

		for i in range(len(self.references)):
			res = re.search(pattern, self.references[i])
			link = res.group(0)
			self.ReferencesList.Append(_("Reference {}: {}").format(i+1, link))

		self.ReferencesList.Selection = 0

	def OnGo(self, event):
		SelectedItem = self.references[self.ReferencesList.Selection]
		webbrowser.open_new(SelectedItem)
		self.Destroy()


class HeadingsListDialog(wx.Dialog):
	def __init__(self, parent, content):
		wx.Dialog.__init__(self, parent, title=_("Headings in this article"), size=(300, 320))
		self.Center()
		self.content = content

		# Create panel
		Panel = wx.Panel(self)

		# Create ListBox
		HeadingsListTitle = wx.StaticText(Panel, -1, _("Choose a heading"))
		self.HeadingsList = wx.ListBox(Panel, -1)
		self.result = re.findall("==.+==", self.content)
		NewResult = []

		for x in self.result:
			x = x.replace("=", "")
			NewResult.append(x[1:-1])
		self.HeadingsList.SetItems(NewResult)
		self.HeadingsList.Selection = 0

		# Create Buttons
		self.Go = wx.Button(Panel, -1, _("&Go"))
		self.Go.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"))

		# Create sizer
		sizer = wx.BoxSizer(wx.VERTICAL)

		# Add widgets to sizer
		sizer.Add(HeadingsListTitle, 0, wx.ALL|wx.ALIGN_CENTER, 5)
		sizer.Add(self.HeadingsList, 1, wx.ALL|wx.EXPAND, 5)

		# Create button sizer
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

		# Add buttons to sizer
		buttonSizer.Add(self.Go, 0, wx.ALL, 5)
		buttonSizer.Add(self.GoBack, 0, wx.ALL, 5)

		# Add button sizer to main sizer
		sizer.Add(buttonSizer, 0, wx.ALL|wx.ALIGN_CENTER, 5)

		# Set sizer for panel
		Panel.SetSizer(sizer)
		Panel.Fit()

		self.hotKeys = wx.AcceleratorTable((
(wx.ACCEL_CTRL, ord("W"), self.GoBack.GetId()),
(wx.ACCEL_CTRL, ord("H"), self.Go.GetId()),
))
		Panel.SetAcceleratorTable(self.hotKeys)

#Event of go button 
		self.Go.Bind(wx.EVT_BUTTON, self.OnGo)

	def OnGo(self, event):
		position = self.content.find(self.result[self.HeadingsList.Selection])
		self.EndModal(position)

class ViewTablesDialog(wx.Dialog):
	def __init__(self, parent, ArticleTitle):
		wx.Dialog.__init__(self, parent, title=_("Tables in {}:").format(ArticleTitle), size=(550, 550))
		self.Center()

	#Creating Panel
		Panel = wx.Panel(self)

	#Creating text ctrl to view article tables
		ArticleTitle = wx.StaticText(Panel, -1, _("Tables in {}:").format(ArticleTitle))
		self.ViewArticleTables = wx.TextCtrl(Panel, -1, style=wx.TE_RICH2+wx.TE_MULTILINE+wx.TE_READONLY)

	#Creating cancel button
		self.close = wx.Button(Panel, wx.ID_CANCEL, _("&Close"))

		# create sizer
		sizer = wx.BoxSizer(wx.VERTICAL)

		# Add widgets to sizer
		sizer.Add(ArticleTitle, 0, wx.ALL|wx.ALIGN_CENTER, 5)
		sizer.Add(self.ViewArticleTables, 1, wx.ALL|wx.EXPAND, 5)

		# Create button sizer
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

		# Add buttons to sizer
		buttonSizer.Add(self.close, 0, wx.ALL, 5)

		# Add button sizer to main sizer
		sizer.Add(buttonSizer, 0, wx.ALL|wx.ALIGN_CENTER, 5)

		# Set sizer for panel
		Panel.SetSizer(sizer)
		Panel.Fit()

		self.hotKeys = wx.AcceleratorTable((
(wx.ACCEL_CTRL, ord("W"), self.close.GetId()),
))
		Panel.SetAcceleratorTable(self.hotKeys)

		#Show dialog
		self.Show()


# Creating history dialog
class HistoryDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("History"), size=(450, 450))
		self.CenterOnParent()
		self.o = accessible_output2.outputs.auto.Auto()
		self.OpenInBrowser_id = wx.NewIdRef(count=1)
		self.CopyLink_id = wx.NewIdRef(count=1)
		self.history = g.Data.GetData("HistoryTable")


		#creating Panel
		panel = wx.Panel(self, -1)
	#creating sizer
		box = wx.BoxSizer(wx.VERTICAL)
		box2 = wx.BoxSizer(wx.HORIZONTAL)
		#Creating search edit.
		self.SearchLabel = wx.StaticText(panel, -1, _("Search"), pos=(12, 15), size=(50, 20))
		self.search = wx.TextCtrl(panel, -1, pos=(56, 12), size=(150, 30))
		#creating listbox to show history.
		self.HistoryLabel = wx.StaticText(panel, -1, _("History"), pos=(12, 51), size=(50, 20))
		self.HistoryList = wx.ListCtrl(panel, -1, style = wx.LC_REPORT)
		self.HistoryList.InsertColumn(0, _("Title"), width=100)
		self.HistoryList.InsertColumn(1, _("Date"), wx.LIST_FORMAT_RIGHT, width= 100)
		self.HistoryList.InsertColumn(2, _("Time"), wx.LIST_FORMAT_RIGHT, 100)
		self.HistoryList.InsertColumn(3, _("Article language"), wx.LIST_FORMAT_RIGHT, 100)

		for item in reversed(self.history):
			self.HistoryList.Append(item)

		#Set selection for first item.
		self.HistoryList.Focus(0)

		#creating buttons
		self.Go = wx.Button(panel, wx.ID_OK, _("&View Article"), size=(50, 20))
		if not len(self.history):
			self.Go.Enable(False)
		self.Cancel = wx.Button(panel, wx.ID_CANCEL, _("&Cancel"), size=(50, 20))

		#Adding the controls to sizer
		box.Add(self.SearchLabel)
		box.Add(self.search) 
		box.Add(self.HistoryLabel)
		box.Add(self.HistoryList, 2, wx.EXPAND)
		box2.Add(self.Go)
		box2.Add(self.Cancel)
		box.Add(box2, 1, wx.EXPAND|wx.TOP, 20)
		#Set sizer
		panel.SetSizer(box) 
		panel.Fit()

		self.hotKeys = wx.AcceleratorTable((
		(wx.ACCEL_CTRL, ord("W"), self.Cancel.GetId()),
		(wx.ACCEL_ALT, ord("V"), self.Go.GetId()),
		(wx.ACCEL_CTRL, ord("O"), self.OpenInBrowser_id),
		(wx.ACCEL_ALT, ord("C"), self.CopyLink_id)
))
		panel.SetAcceleratorTable(self.hotKeys)


		#events
		self.Bind(wx.EVT_BUTTON, self.OnGo, self.Go)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnGo, self.HistoryList)
		self.Bind(wx.EVT_TEXT, self.OnSearch, self.search)
		self.Bind(wx.EVT_CONTEXT_MENU, self.ContextMenu, self.HistoryList)
		self.Bind(wx.EVT_MENU, lambda event: my_threads(target=self.OnOpenInBrowser, daemon=True).start(), self.OpenInBrowser_id)
		self.Bind(wx.EVT_MENU, lambda event: my_threads(target=self.OnCopyLinkItem(), daemon=True).start(), self.CopyLink_id)
		self.HistoryList.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

		# Show the Dialog
		self.Show()

	def OnGo(self, event):
		from view_article_window import ViewArticleWindow
		from web_viewer import WebViewArticle
		#Getting title of article
		ArticleLanguage = GetValue = self.HistoryList.GetItemText(self.HistoryList.GetFocusedItem(), 3)
		ArticleLanguage = g.code[ArticleLanguage]
		GetValue = self.HistoryList.GetItemText(self.HistoryList.GetFocusedItem(), 0)

		#Set language for  a article.
		try:
			wikipedia.set_lang(ArticleLanguage)
		except:
			ConnectionError = wx.MessageDialog(self, _("There is no internet connection."), _("Connection error"), style=wx.ICON_ERROR+wx.OK)
			ConnectionError.SetOKLabel(_("&Ok"))
			ConnectionError.ShowModal()
			return None

		state = Settings().ReadSettings()["wepviewer"]
		if state == "0":
			window1 = ViewArticleWindow(None, GetValue, self)
		else:
			window1 = WebViewArticle(None, GetValue, self)

	def OnSearch(self, event):
		self.HistoryList.DeleteAllItems()
		if not self.search.Value:
			for item in reversed(self.history):
				self.HistoryList.Append(item[0:-1])
		else:
			result = g.Data.SearchData("HistoryTable", "Title", self.search.Value)
			for item in reversed(result):
				self.HistoryList.Append(item[0:-1])


	# creating context menue
	def ContextMenu(self, event):
		menu = wx.Menu()
		OpenItem = menu.Append(-1, _("&View Article"))
		OpenInBrowserItem = menu.Append(-1, _("&Open in browser"))
		CopyLinkItem = menu.Append(-1, _("&Copy article link"))
		DeleteItem = menu.Append(-1, _("&Delete"))
		self.Bind(wx.EVT_MENU, self.OnGo, OpenItem)
		self.Bind(wx.EVT_MENU, lambda event: my_threads(target=self.OnOpenInBrowser, daemon=True).start(), OpenInBrowserItem)
		self.Bind(wx.EVT_MENU, lambda event: my_threads(target=self.OnCopyLinkItem, daemon=True).start(), CopyLinkItem)
		self.Bind(wx.EVT_MENU, self.OnDeleteItem, DeleteItem)
		if not len(self.history):
			OpenItem.Enable(False)
			OpenInBrowserItem.Enable(False)
			CopyLinkItem.Enable(False)
			DeleteItem.Enable(False)
		self.PopupMenu(menu)

	# creating function to delete any item in the history
	def OnDeleteItem(self, event):
		SelectedItem = self.HistoryList.GetItemText(self.HistoryList.GetFocusedItem(), 0)
		g.Data.DeleteItem("HistoryTable", "Title", SelectedItem)
		self.HistoryList.DeleteItem(self.HistoryList.GetFocusedItem())
		self.history = g.Data.GetData("HistoryTable")
		if not len(self.history):
			self.Go.Enable(False)
		if not self.o.is_system_output():
			self.o.speak(_("The selected item has been deleted."), interrupt=True)

	#Creating OnCopyLinkItem function  to copy the Article Link to Clipboard
	def OnCopyLinkItem(self):
		ArticleLanguage = GetValue = self.HistoryList.GetItemText(self.HistoryList.GetFocusedItem(), 3)
		ArticleLanguage = g.code[ArticleLanguage]
		SelectedItem = self.HistoryList.GetItemText(self.HistoryList.GetFocusedItem(), 0)

		try:
			wikipedia.set_lang(ArticleLanguage)
			url = wikipedia.page(SelectedItem).url
			pyperclip.copy(url)
			if not self.o.is_system_output():
				self.o.speak(_("Article link copied."), interrupt=True)
		except:
			CantCopy = wx.MessageDialog(self, _("This link cannot be copied."), _("Error"), style=wx.ICON_ERROR)
			CantCopy.SetOKLabel(_("&Ok"))
			CantCopy.ShowModal()
			return


	def OnOpenInBrowser(self):
		ArticleLanguage = GetValue = self.HistoryList.GetItemText(self.HistoryList.GetFocusedItem(), 3)
		ArticleLanguage = g.code[ArticleLanguage]
		SelectedItem = self.HistoryList.GetItemText(self.HistoryList.GetFocusedItem(), 0)

		try:
			wikipedia.set_lang(ArticleLanguage)
			url = wikipedia.page(SelectedItem).url
			webbrowser.open_new(url)
			if not self.o.is_system_output():
				self.o.speak(_("Opening:"), interrupt=True)
		except:
			CantOpen = wx.MessageDialog(self, _("This link cannot be opened in the browser."), _("Error"), style=wx.ICON_ERROR+wx.OK)
			CantOpen.SetOKLabel(_("&Ok"))
			CantOpen.ShowModal()
			return


	# making access key
	def OnKeyDown(self, event):
		event.Skip()
		Key = event.GetKeyCode()
		if (Key == wx.WXK_DELETE) and (len(self.history)):
			self.OnDeleteItem(None)

# Creating favourites dialog
class FavouritesDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("Favourite Articles"), size=(450, 450))
		self.CenterOnParent()
		self.o = accessible_output2.outputs.auto.Auto()
		self.OpenInBrowser_id = wx.NewIdRef(count=1)
		self.CopyLink_id = wx.NewIdRef(count=1)
		self.Favourites = g.Data.GetData("FavouritesTable")
		#creating Panel
		panel = wx.Panel(self, -1)
	#creating sizer
		box = wx.BoxSizer(wx.VERTICAL)
		box2 = wx.BoxSizer(wx.HORIZONTAL)
		#Creating search edit.
		self.SearchLabel = wx.StaticText(panel, -1, _("Search"), pos=(12, 15), size=(50, 20))
		self.search = wx.TextCtrl(panel, -1, pos=(56, 12), size=(150, 30))
		#creating listbox to show history.
		self.FavouritesLabel = wx.StaticText(panel, -1, _("Favourite Articles"), pos=(12, 51), size=(50, 20))
		self.FavouritesList = wx.ListCtrl(panel, -1, style = wx.LC_REPORT)
		self.FavouritesList.InsertColumn(0, _("Title"), width=100)
		self.FavouritesList.InsertColumn(1, _("Article language"), wx.LIST_FORMAT_RIGHT, 100)

		self.ArticleTitle = {}
		for item in reversed(self.Favourites):
			self.FavouritesList.Append(item[1:3])
			self.ArticleTitle[item[1]] = item[0]

		#Set selection for first item.
		self.FavouritesList.Focus(0)

		#creating buttons
		self.Go = wx.Button(panel, wx.ID_OK, _("&View Article"), size=(50, 20))
		if not len(self.Favourites):
			self.Go.Enable(False)
		self.Cancel = wx.Button(panel, wx.ID_CANCEL, _("&Cancel"), size=(50, 20))

		#Adding the controls to sizer
		box.Add(self.SearchLabel)
		box.Add(self.search) 
		box.Add(self.FavouritesLabel)
		box.Add(self.FavouritesList, 2, wx.EXPAND)
		box2.Add(self.Go)
		box2.Add(self.Cancel)
		box.Add(box2, 1, wx.EXPAND|wx.TOP, 20)
		#Set sizer
		panel.SetSizer(box) 
		panel.Fit()

		self.hotKeys = wx.AcceleratorTable((
		(wx.ACCEL_CTRL, ord("W"), self.Cancel.GetId()),
		(wx.ACCEL_ALT, ord("V"), self.Go.GetId()),
		(wx.ACCEL_CTRL, ord("O"), self.OpenInBrowser_id),
		(wx.ACCEL_ALT, ord("C"), self.CopyLink_id)
))
		panel.SetAcceleratorTable(self.hotKeys)


		#events
		self.Bind(wx.EVT_BUTTON, self.OnGo, self.Go)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnGo, self.FavouritesList)
		self.Bind(wx.EVT_TEXT, self.OnSearch, self.search)
		self.Bind(wx.EVT_CONTEXT_MENU, self.ContextMenu, self.FavouritesList)
		self.Bind(wx.EVT_MENU, self.OnOpenInBrowser, self.OpenInBrowser_id)
		self.Bind(wx.EVT_MENU, self.OnCopyLinkItem, self.CopyLink_id)
		self.FavouritesList.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

		# Show the Dialog
		self.Show()

	def OnGo(self, event):
		from view_article_window import ViewArticleWindow
		from web_viewer import WebViewArticle
		#Getting title of article
		ArticleLanguage = GetValue = self.FavouritesList.GetItemText(self.FavouritesList.GetFocusedItem(), 1)
		ArticleLanguage = g.code[ArticleLanguage]
		GetValue = self.FavouritesList.GetItemText(self.FavouritesList.GetFocusedItem(), 0)
		GetValue = self.ArticleTitle[		GetValue]

		#Set language for  a article.
		try:
			wikipedia.set_lang(ArticleLanguage)
		except:
			ConnectionError = wx.MessageDialog(self, _("There is no internet connection."), _("Connection error"), style=wx.ICON_ERROR+wx.OK)
			ConnectionError.SetOKLabel(_("&Ok"))
			ConnectionError.ShowModal()
			return None

		state = Settings().ReadSettings()["wepviewer"]
		if state == "0":
			window1 = ViewArticleWindow(None, GetValue, self)
		else:
			window1 = WebViewArticle(None, GetValue, self)

	def OnSearch(self, event):
		self.FavouritesList.DeleteAllItems()
		if not self.search.Value:
			for item in reversed(self.Favourites):
				self.FavouritesList.Append(item[1:3])
		else:
			result = g.Data.SearchData("FavouritesTable", "Name", self.search.Value)
			for item in reversed(result):
				self.FavouritesList.Append(item[1:3])

	# creating context menue
	def ContextMenu(self, event):
		menu = wx.Menu()
		OpenItem = menu.Append(-1, _("&View Article"))
		OpenInBrowserItem = menu.Append(-1, _("&Open in browser"))
		CopyLinkItem = menu.Append(-1, _("&Copy article link"))
		RenameItem = menu.Append(-1, _("&Rename"))
		DeleteItem = menu.Append(-1, _("&Delete"))
		self.Bind(wx.EVT_MENU, self.OnGo, OpenItem)
		self.Bind(wx.EVT_MENU, self.OnOpenInBrowser, OpenInBrowserItem)
		self.Bind(wx.EVT_MENU, self.OnCopyLinkItem, CopyLinkItem)
		self.Bind(wx.EVT_MENU, self.OnDeleteItem, DeleteItem)
		self.Bind(wx.EVT_MENU, self.OnRenameItem, RenameItem)
		if not len(self.Favourites):
			OpenItem.Enable(False)
			OpenInBrowserItem.Enable(False)
			CopyLinkItem.Enable(False)
			RenameItem.Enable(False)
			DeleteItem.Enable(False)
		self.PopupMenu(menu)

	# creating function to delete any item.
	def OnDeleteItem(self, event):
		SelectedItem = self.FavouritesList.GetItemText(self.FavouritesList.GetFocusedItem(), 0)
		g.Data.DeleteItem("FavouritesTable", "Name", SelectedItem)
		self.FavouritesList.DeleteItem(self.FavouritesList.GetFocusedItem())
		self.Favourites = g.Data.GetData("FavouritesTable")
		if not len(self.Favourites):
			self.Go.Enable(False)
		if not self.o.is_system_output():
			self.o.speak(_("The selected item has been deleted."), interrupt=True)

# creating function to rename items
	def OnRenameItem(self, event):
		SelectedItem = self.FavouritesList.GetItemText(self.FavouritesList.GetFocusedItem(), 0)
		RenameDialog = wx.TextEntryDialog(self, _("Choose the new name for the article."), _("Rename the article"), SelectedItem)
		RenameDialog.GetChildren()[-3].SetLabel(_("&Rename"))
		RenameDialog.GetChildren()[-2].SetLabel(_("&Cancel"))
		if RenameDialog.ShowModal() == wx.ID_OK:
			NewName = RenameDialog.GetValue()
			if NewName == "":
				self.OnRenameItem(None)
				return
		else:
			return

		g.Data.UpdateData("FavouritesTable", "Name", SelectedItem, NewName)
		self.FavouritesList.SetItemText(self.FavouritesList.GetFocusedItem(), NewName)

	#Creating OnCopyLinkItem function  to copy the Article Link to Clipboard
	def OnCopyLinkItem(self, event):
		# Getting url from Database.
		SelectedItem = self.FavouritesList.GetItemText(self.FavouritesList.GetFocusedItem(), 0)
		url = g.Data.SearchData("FavouritesTable", "Name", SelectedItem)[0][3]
		# Copy the link.
		pyperclip.copy(url)
		if not self.o.is_system_output():
			self.o.speak(_("Article link copied."), interrupt=True)


	def OnOpenInBrowser(self, event):
# Getting url from Database.
		SelectedItem = self.FavouritesList.GetItemText(self.FavouritesList.GetFocusedItem(), 0)
		url = g.Data.SearchData("FavouritesTable", "Name", SelectedItem)[0][3]

		# Open the link in browser.
		webbrowser.open_new(url)
		if not self.o.is_system_output():
			self.o.speak(_("Opening:"), interrupt=True)

	# making access key
	def OnKeyDown(self, event):
		event.Skip()
		Key = event.GetKeyCode()
		if (Key == wx.WXK_DELETE) and (len(self.Favourites)):
			self.OnDeleteItem(None)
		elif Key == wx.WXK_F2:
			self.OnRenameItem(None)


# Creating saved articles dialog
class SavedArticlesDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("Saved Articles"), size=(450, 450))
		self.CenterOnParent()
		self.o = accessible_output2.outputs.auto.Auto()
		self.OpenInBrowser_id = wx.NewIdRef(count=1)
		self.CopyLink_id = wx.NewIdRef(count=1)
		self.SavedArticles = g.Data.GetData("SavedArticlesTable")

		#creating Panel
		panel = wx.Panel(self, -1)
	#creating sizer
		box = wx.BoxSizer(wx.VERTICAL)
		box2 = wx.BoxSizer(wx.HORIZONTAL)
		#Creating search edit.
		self.SearchLabel = wx.StaticText(panel, -1, _("Search"), pos=(12, 15), size=(50, 20))
		self.search = wx.TextCtrl(panel, -1, pos=(56, 12), size=(150, 30))
		#creating listbox to show history.
		self.SavedArticlesLabel = wx.StaticText(panel, -1, _("Saved Articles"), pos=(12, 51), size=(50, 20))
		self.SavedArticlesList = wx.ListCtrl(panel, -1, style = wx.LC_REPORT)
		self.SavedArticlesList.InsertColumn(0, _("Title"), width=100)
		self.SavedArticlesList.InsertColumn(1, _("Article language"), wx.LIST_FORMAT_RIGHT, 100)

		self.ArticleTitle = {}
		for item in reversed(self.SavedArticles):
			self.SavedArticlesList.Append(item[1:3])
			self.ArticleTitle[item[1]] = item[0]

		#Set selection for first item.
		self.SavedArticlesList.Focus(0)

		#creating buttons
		self.Go = wx.Button(panel, wx.ID_OK, _("&View Article"), size=(50, 20))
		if not len(self.SavedArticles):
			self.Go.Enable(False)
		self.Cancel = wx.Button(panel, wx.ID_CANCEL, _("&Cancel"), size=(50, 20))

		#Adding the controls to sizer
		box.Add(self.SearchLabel)
		box.Add(self.search) 
		box.Add(self.SavedArticlesLabel)
		box.Add(self.SavedArticlesList, 2, wx.EXPAND)
		box2.Add(self.Go)
		box2.Add(self.Cancel)
		box.Add(box2, 1, wx.EXPAND|wx.TOP, 20)
		#Set sizer
		panel.SetSizer(box) 
		panel.Fit()

		self.hotKeys = wx.AcceleratorTable((
		(wx.ACCEL_CTRL, ord("W"), self.Cancel.GetId()),
		(wx.ACCEL_ALT, ord("V"), self.Go.GetId()),
		(wx.ACCEL_CTRL, ord("O"), self.OpenInBrowser_id),
		(wx.ACCEL_ALT, ord("C"), self.CopyLink_id)
))
		panel.SetAcceleratorTable(self.hotKeys)


		#events
		self.Bind(wx.EVT_BUTTON, self.OnGo, self.Go)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnGo, self.SavedArticlesList)
		self.Bind(wx.EVT_TEXT, self.OnSearch, self.search)
		self.Bind(wx.EVT_CONTEXT_MENU, self.ContextMenu, self.SavedArticlesList)
		self.Bind(wx.EVT_MENU, self.OnOpenInBrowser, self.OpenInBrowser_id)
		self.Bind(wx.EVT_MENU, self.OnCopyLinkItem, self.CopyLink_id)
		self.SavedArticlesList.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

		# Show the Dialog
		self.Show()

	def OnGo(self, event):
		from view_article_window import ViewArticleWindow
		from web_viewer import WebViewArticle
		#Getting Name of article
		GetValue = self.SavedArticlesList.GetItemText(self.SavedArticlesList.GetFocusedItem(), 0)
		CurrentArticle = g.Data.SearchData("SavedArticlesTable", "Name", GetValue)

		state = Settings().ReadSettings()["wepviewer"]
		if state == "0":
			window1 = ViewArticleWindow(None, "", self)
		else:
			window1 = WebViewArticle(None, "", self)



		# load the article
		window1.LoadOflineArticle(CurrentArticle)


	def OnSearch(self, event):
		self.SavedArticlesList.DeleteAllItems()
		if not self.search.Value:
			for item in reversed(self.SavedArticles):
				self.SavedArticlesList.Append(item[1:3])
		else:
			result = g.Data.SearchData("SavedArticlesTable", "Name", self.search.Value)
			for item in reversed(result):
				self.SavedArticlesList.Append(item[1:3])

	# creating context menue
	def ContextMenu(self, event):
		menu = wx.Menu()
		OpenItem = menu.Append(-1, _("&View Article"))
		OpenInBrowserItem = menu.Append(-1, _("&Open in browser"))
		CopyLinkItem = menu.Append(-1, _("&Copy article link"))
		RenameItem = menu.Append(-1, _("&Rename"))
		DeleteItem = menu.Append(-1, _("&Delete"))
		self.Bind(wx.EVT_MENU, self.OnGo, OpenItem)
		self.Bind(wx.EVT_MENU, self.OnOpenInBrowser, OpenInBrowserItem)
		self.Bind(wx.EVT_MENU, self.OnCopyLinkItem, CopyLinkItem)
		self.Bind(wx.EVT_MENU, self.OnDeleteItem, DeleteItem)
		self.Bind(wx.EVT_MENU, self.OnRenameItem, RenameItem)
		if not len(self.SavedArticles):
			OpenItem.Enable(False)
			OpenInBrowserItem.Enable(False)
			CopyLinkItem.Enable(False)
			RenameItem.Enable(False)
			DeleteItem.Enable(False)
		self.PopupMenu(menu)

	# creating function to delete any item in the history
	def OnDeleteItem(self, event):
		SelectedItem = self.SavedArticlesList.GetItemText(self.SavedArticlesList.GetFocusedItem(), 0)
		g.Data.DeleteItem("SavedArticlesTable", "Name", SelectedItem)
		self.SavedArticlesList.DeleteItem(self.SavedArticlesList.GetFocusedItem())
		self.SavedArticles = g.Data.GetData("SavedArticlesTable")
		if not len(self.SavedArticles):
			self.Go.Enable(False)
		if not self.o.is_system_output():
			self.o.speak(_("The selected item has been deleted."), interrupt=True)

	# creating function to rename items
	def OnRenameItem(self, event):
		SelectedItem = self.SavedArticlesList.GetItemText(self.SavedArticlesList.GetFocusedItem(), 0)
		RenameDialog = wx.TextEntryDialog(self, _("Choose the new name for the article."), _("Rename the article"), SelectedItem)
		RenameDialog.GetChildren()[-3].SetLabel(_("&Rename"))
		RenameDialog.GetChildren()[-2].SetLabel(_("&Cancel"))
		if RenameDialog.ShowModal() == wx.ID_OK:
			NewName = RenameDialog.GetValue()
			if NewName == "":
				self.OnRenameItem(None)
				return
		else:
			return

		g.Data.UpdateData("SavedArticlesTable", "Name", SelectedItem, NewName)
		self.SavedArticlesList.SetItemText(self.SavedArticlesList.GetFocusedItem(), NewName)

	#Creating OnCopyLinkItem function  to copy the Article Link to Clipboard
	def OnCopyLinkItem(self, event):
		# Getting url from Database.
		SelectedItem = self.SavedArticlesList.GetItemText(self.SavedArticlesList.GetFocusedItem(), 0)
		url = g.Data.SearchData("SavedArticlesTable", "Name", SelectedItem)[0][5]
		# Copy the link.
		pyperclip.copy(url)
		if not self.o.is_system_output():
			self.o.speak(_("Article link copied."), interrupt=True)


	def OnOpenInBrowser(self, event):
# Getting url from Database.
		SelectedItem = self.SavedArticlesList.GetItemText(self.SavedArticlesList.GetFocusedItem(), 0)
		url = g.Data.SearchData("SavedArticlesTable", "Name", SelectedItem)[0][5]

		# Open the link in browser.
		webbrowser.open_new(url)
		if not self.o.is_system_output():
			self.o.speak(_("Opening:"), interrupt=True)

	# making access key
	def OnKeyDown(self, event):
		event.Skip()
		Key = event.GetKeyCode()
		if (Key == wx.WXK_DELETE) and (len(self.SavedArticles)):
			self.OnDeleteItem(None)
		elif Key == wx.WXK_F2:
			self.OnRenameItem(None)