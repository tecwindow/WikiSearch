#-*- coding: utf-8 -*-
# import project libraries.
import wx
import nlpia2_wikipedia as wikipedia
import accessible_output2.outputs.auto
import pyperclip
from  my_classes import my_threads
import webbrowser
from settings import Settings
from functions import *
from globals import *


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
		self.ReferencesListTitle = wx.StaticText(Panel, -1, _("Article references"), pos=(10,10), size=(380,30))
		self.ReferencesList = wx.ListBox(Panel, -1, pos=(10,30), size=(290,170))

		# Create Buttons
		self.Go = wx.Button(Panel, -1, _("&Open in browser"), pos=(10,235), size=(120,30))
		self.Go.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"), pos=(140,235), size=(120,30))

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
		wx.StaticText(Panel, -1, _("Choose a heading"), pos=(10,10), size=(380,30))
		self.HeadingsList = wx.ListBox(Panel, -1, pos=(10,30), size=(290,170))
		self.result = re.findall("==.+==", self.content)
		NewResult = []

		for x in self.result:
			x = x.replace("=", "")
			NewResult.append(x[1:-1])
		self.HeadingsList.SetItems(NewResult)
		self.HeadingsList.Selection = 0

		# Create Buttons
		self.Go = wx.Button(Panel, -1, _("&Go"), pos=(10,235), size=(120,30))
		self.Go.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"), pos=(140,235), size=(120,30))

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
	def __init__(self, parent, url, ArticleTitle):
		wx.Dialog.__init__(self, parent, title=_("Tables in {}:").format(ArticleTitle), size=(550, 550))
		self.Center()
		self.url = url
		self.LoadTables = my_threads(target=self.OnViewTable, daemon=True)
		self.LoadTables.start()

	#Creating Panel
		Panel = wx.Panel(self)

	#Creating text ctrl to view article tables
		wx.StaticText(Panel, -1, _("Tables in {}:").format(ArticleTitle), pos=(10,10), size=(380, 30))
		self.ViewArticleTables = wx.TextCtrl(Panel, -1, pos=(10, 50), size=(500, 400), style=wx.TE_RICH2+wx.TE_MULTILINE+wx.TE_READONLY)

	#Creating cancel button
		self.close = wx.Button(Panel, wx.ID_CANCEL, _("&Close"), pos=(200,450), size=(120,30))

		self.hotKeys = wx.AcceleratorTable((
(wx.ACCEL_CTRL, ord("W"), self.close.GetId()),
))
		Panel.SetAcceleratorTable(self.hotKeys)

		#Show dialog
		self.Show()

	def OnViewTable(self):

		tables = GetTables(self.url)

		for table in range(len(tables)):
			self.ViewArticleTables.write(_("Table {}:\n {}").format(table+1,tables[table]))

		self.ViewArticleTables.SetInsertionPoint(0)

class HistoryDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("history"), size=(450, 450))
		self.CenterOnParent()
		self.o = accessible_output2.outputs.auto.Auto()
		global Data
		self.history = Data.GetData("HistoryTable")


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
		self.HistoryList.InsertColumn(0, "Title", width=100)
		self.HistoryList.InsertColumn(1, "Date", wx.LIST_FORMAT_RIGHT, width= 100)
		self.HistoryList.InsertColumn(2, "Time", wx.LIST_FORMAT_RIGHT, 100)
		self.HistoryList.InsertColumn(3, "Article language", wx.LIST_FORMAT_RIGHT, 100)

		self.LanguageCode = {}
		for item in reversed(self.history):
			self.HistoryList.Append(item[0:-1])
			self.LanguageCode[item[3]] = item[4]

		#Set selection for first item.
		self.HistoryList.Focus(0)

		#creating buttons
		self.Go = wx.Button(panel, wx.ID_OK, _("&Go"), size=(50, 20))
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
))
		panel.SetAcceleratorTable(self.hotKeys)


		#events
		self.Bind(wx.EVT_BUTTON, self.OnGo, self.Go)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnGo, self.HistoryList)
		self.Bind(wx.EVT_TEXT, self.OnSearch, self.search)
		self.Bind(wx.EVT_CONTEXT_MENU, self.ContextMenu, self.HistoryList)
		self.HistoryList.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

		# Show the Dialog
		self.Show()

	def OnGo(self, event):
		from view_article_window import ViewArticleWindow
		from web_viewer import WebViewArticle
		#Getting title of article
		ArticleLanguage = GetValue = self.HistoryList.GetItemText(self.HistoryList.GetFocusedItem(), 3)
		ArticleLanguage = self.LanguageCode[ArticleLanguage]
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
			global Data
			result = Data.SearchData("HistoryTable", "Title", self.search.Value)
			for item in reversed(result):
				self.HistoryList.Append(item[0:-1])


	# creating context menue
	def ContextMenu(self, event):
		menu = wx.Menu()
		OpenItem = menu.Append(-1, "Open")
		CopyLinkItem = menu.Append(-1, "Copy the article link")
		DeleteItem = menu.Append(-1, "Delete")
		self.Bind(wx.EVT_MENU, self.OnDeleteItem, DeleteItem)
		self.Bind(wx.EVT_MENU, self.OnGo, OpenItem)
		self.Bind(wx.EVT_MENU, lambda event: my_threads(target=self.OnCopyLinkItem, daemon=True).start(), CopyLinkItem)
		self.PopupMenu(menu)



	# creating function to delete any item in the history
	def OnDeleteItem(self, event):
		SelectedItem = self.HistoryList.GetItemText(self.HistoryList.GetFocusedItem(), 0)
		Data.DeleteItem("HistoryTable", "Title", SelectedItem)
		self.HistoryList.DeleteItem(self.HistoryList.GetFocusedItem())
		if not self.o.is_system_output():
			self.o.speak(_("The Item has deleted."), interrupt=True)


	#Creating OnCopyLinkItem function  to copy the Article Link to Clipboard
	def OnCopyLinkItem(self):
		ArticleLanguage = GetValue = self.HistoryList.GetItemText(self.HistoryList.GetFocusedItem(), 3)
		ArticleLanguage = self.LanguageCode[ArticleLanguage]
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

	# making access key
	def OnKeyDown(self, event):
		event.Skip()
		Key = event.GetKeyCode()
		if Key == wx.WXK_DELETE:
			self.OnDeleteItem(None)