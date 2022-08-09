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
import shutil
from dialogs import *
from settings import Settings
from functions import *
from my_classes import *

#Set language for View Article window
_ = SetLanguage(Settings().ReadSettings())


#View Article window
class WebViewArticle(wx.Frame):
	def __init__(self, parent, GetValues, handle):
		wx.Frame.__init__(self, parent, title=_("View article"), size=(560, 600))
		self.Center()
		self.EnableMaximizeButton(False)
		self.GetValues = GetValues
		self.Content = ""
		self.url = ""
		self.title = ""
		self.links = []
		self.references = []
		self.html = _("<h1>Please wait</h1>")
		self.handle = handle
		self.o = accessible_output2.outputs.auto.Auto()
		self.rand_id = wx.NewIdRef(count=1)
		self.CurrentSettings = Settings().ReadSettings()
		self.colour = self.GetBackgroundColour()

		self.temp = os.path.join(os.getenv("temp"), "WikiSearch")
		self.FileName = self.title + ".html"
		self.path = os.path.join(self.temp, self.FileName)
		if not os.path.exists(self.temp):
			os.mkdir(self.temp)

#Creating panel
		Panel = wx.Panel(self, -1)
		# Create Menus.
		menubar = wx.MenuBar()
		actions = wx.Menu()
		self.CopyArticleItem = actions.Append(-1, _("Copy article\tctrl+shift+c"))
		self.CopyArticleItem.Enable(False)
		self.CopyArticleLinkItem = actions.Append(-1, _("Copy article link\t+alt+c"))
		self.CopyArticleLinkItem.Enable(False)
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
		self.CloseArticleItem = actions.Append(-1, _("Close article window\tctrl+w"))
		self.CloseProgramItem = actions.Append(-1, _("Close the program\tctrl+F4"))
		menubar.Append(actions, _("Actions"))
		self.SetMenuBar(menubar)



		# creating web viewer
		self.ArticleTitle = wx.StaticText(Panel, -1, "please wait:", pos=(10,10), size=(380,30))
		self.ViewArticle = wx.html2.WebView.New(Panel, -1, pos=(30,40), size=(480,420))
		self.ViewArticle.SetPage(self.html, "")
		self.ViewArticle.EnableContextMenu(False)
#loading article
		self.LoadArticle = my_threads(target=self.OpenThread, daemon=True)
		self.LoadArticle.start()
		self.LoadArticle2 = my_threads(target=self.OpenThread2, daemon=True)
		self.LoadArticle2.start()


		# events 
		self.Bind(wx.EVT_CLOSE, self.OnCloseArticle)
		self.Bind(wx.EVT_MENU, self.OnCopyArticle, self.CopyArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCopyArticleLink, self.CopyArticleLinkItem) 
		self.Bind(wx.EVT_MENU, self.OnSaveArticle, self.SaveArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCloseArticle, self.CloseArticleItem) 
		self.Bind(wx.EVT_MENU, self.OnCloseProgram, self.CloseProgramItem) 
		self.Bind(wx.EVT_MENU, self.OnEscape, id=self.rand_id)
		self.Bind(wx.EVT_MENU, self.OnReferencesItem, self.ReferencesItem)
		self.Bind(wx.EVT_MENU, self.OnSaveAsHtml, self.SaveAsHtmlItem)
		self.Bind(wx.EVT_MENU, self.OnLinks, self.LinksItem)
		self.Bind(wx.html2.EVT_WEBVIEW_LOADED, lambda event: self.o.speak(_("Article loaded."), interrupt=True))

		self.hotKeys = wx.AcceleratorTable((
			(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("C"), self.CopyArticleItem.GetId()),
			(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("H"), self.SaveAsHtmlItem.GetId()),
			(0+wx.ACCEL_ALT, ord("C"), self.CopyArticleLinkItem.GetId()),
			(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("T"), self.SaveArticleItem.GetId()),
			(wx.ACCEL_CTRL, ord("R"), self.ReferencesItem.GetId()),
			(wx.ACCEL_CTRL, ord("L"), self.LinksItem.GetId()),
			(wx.ACCEL_CTRL, ord("W"), self.CloseArticleItem.GetId()),
			(wx.ACCEL_CTRL,wx.WXK_F4, self.CloseProgramItem.GetId()),
			(0, wx.WXK_ESCAPE, self.rand_id)
		))
		self.SetAcceleratorTable(self.hotKeys)

		# Show Article window
		self.Show()


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
			if self.LoadArticle.is_stopped():
				return None
			ConnectionError = wx.MessageDialog(self, _("There is no internet connection."), _("Connection error"), style=wx.ICON_ERROR+wx.OK)
			ConnectionError.SetOKLabel(_("&Ok"))
			ConnectionError.ShowModal()
			self.Destroy()
			self.handle.NumberArticle -=1
			return None

		#Getting information of article, and show The title and content of it.
		self.title = page.title
		self.html = page.html()
		self.html = DisableLink(self.html)
		with open(self.path, "w", encoding="utf-16") as f:
			f.write(self.html)
		self.ViewArticle.LoadURL(self.path)
		self.SetTitle(f"View {self.title}")
		self.ArticleTitle.SetLabel(self.title)
		self.url = page.url
		self.Content = page.content

#Enable menu items
		self.SaveArticleItem.Enable(enable=True)
		self.CopyArticleLinkItem.Enable(enable=True)
		self.SaveAsHtmlItem.Enable(enable=True)
		self.CopyArticleItem.Enable(enable=True)
		self.SaveArticle.Enable(enable=True)

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
			file.write(self.Content)
			file.close()
		else:
			return



	# Close Article Window
	def OnCloseArticle(self, event):
		self.handle.NumberArticle -= 1
		self.LoadArticle.stop()
		self.LoadArticle2.stop()
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
Do you want to close the program anyway?""").format(ArticleCounte), _("Confirm"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
			ConfirmClosProgram.SetYesNoLabels(_("&Yes"), _("&No"))
			if ConfirmClosProgram.ShowModal() == wx.ID_YES:
				wx.Exit()
				shutil.rmtree(self.temp, ignore_errors=False)
			else:
				return
		else:
			wx.Exit()
			shutil.rmtree(self.temp, ignore_errors=False)


	def OnReferencesItem(self, event):
		ReferencesDialog = ReferencesListDialog(self, *self.references)
		threading.Thread(target=ReferencesDialog.OpenThread, daemon=True).start()

	def OnEscape(self, event):

		state = self.CurrentSettings["activ escape"]

		if state == "True":
			self.handle.NumberArticle -= 1
			self.LoadArticle.stop()
			self.LoadArticle2.stop()
			self.Destroy()
		else:
			pass




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

