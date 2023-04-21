#-*- coding: utf-8 -*-
# import project libraries.
from custome_errors import *
sys.excepthook = my_excepthook
import wx
import json
import nlpia2_wikipedia as wikipedia
import threading 
import webbrowser
import datetime
import os
import sys
#change working dir to main exe dir
#os.chdir(os.path.dirname(sys.argv[0]))
import globals as g
from view_search_dialog import ViewSearch
from update_dialog import UpdateDialog
from settings import *
from functions import *
from dialogs import HistoryDialog, FavouritesDialog, SavedArticlesDialog
from packaging import version
from view_search_dialog import *


#Set language for main window 
_ = SetLanguage(Settings().ReadSettings())

# information of program
CurrntVersion = "1.4.0"
ProgramName = "WikiSearch"
ProgramDescription = _("With this program, you can search or browse any Wikipedia article. site: https://github.com/tecwindow/WikiSearch")
CurrentSettings = Settings().ReadSettings()


# Create main window with wx.
class window(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title = ProgramName, size=(430, 335))
		#make window in center.
		self.Center()
		#make window Minimum size.
		self.Maximize(False)
		self.EnableMaximizeButton(False)


		# Creating panel
		Panel = wx.Panel(self)

		# Creating ComboBox for languages
		wx.StaticText(Panel, -1, _("Choose the search language:"), pos=(15,70), size=(380, 30))
		self.LanguageSearch = wx.ComboBox(Panel, -1, pos=(15, 100), size=(120, 40), style=wx.CB_READONLY+wx.CB_SORT)
		self.LanguageSearch.SetItems(g.name)
		self.LanguageSearch.Value = CurrentSettings["search language"]

		# Creating  search edit
		wx.StaticText(Panel, -1, _("Enter search words"), pos=(190,70), size=(380, 30))
		self.SearchText = wx.TextCtrl(Panel, -1, pos=(160, 100), size=(230, 30))

		# Creating Buttons
		self.StartSearch = wx.Button(Panel, -1, _("Start search"), pos=(10,235), size=(100,30))
		self.StartSearch.SetDefault()
		self.StartSearch.Enabled = False
		self.RandomArticles = wx.Button(Panel, -1, _("View random articles"), pos=(130,235), size=(120,30))
		self.Close = wx.Button(Panel, -1, _("Close the program"), pos=(270,235), size=(120,30))

		#creating menu bar
		menubar = wx.MenuBar()
		MainMenu = wx.Menu()
		self.HelpFile = MainMenu.Append(-1, _("&Help file\tF1"))
		AboutProgramItem = MainMenu.Append(-1, _("&About"))
		ContactMenu = wx.Menu()
		QaisMenu = wx.Menu()
		QaisEm = QaisMenu.Append(-1, "&E-mail")
		QaisTe =QaisMenu.Append(-1, "&Telegram")
		QaisWh =QaisMenu.Append(-1, "&Whats App")
		QaisTw =QaisMenu.Append(-1, "&Twitter")
		QaisFa =QaisMenu.Append(-1, "&Facebook")
		ContactMenu.AppendSubMenu(QaisMenu, _("Qais Alrefai"))
		MahmoodMenu = wx.Menu()
		MahmoodEm =MahmoodMenu.Append(-1, "&E-mail")
		MahmoodTe =MahmoodMenu.Append(-1, "&Telegram")
		MahmoodWh =MahmoodMenu.Append(-1, "&Whats App")
		MahmoodTw =MahmoodMenu.Append(-1, "&Twitter")
		MahmoodFa =MahmoodMenu.Append(-1, "&Facebook")
		ContactMenu.AppendSubMenu(MahmoodMenu, _("Mahmood atef"))
		MesterPerfectMenu = wx.Menu()
		MesterPerfectEm =MesterPerfectMenu.Append(-1, "&E-mail")
		MesterPerfectTe =MesterPerfectMenu.Append(-1, "&Telegram")
		MesterPerfectWh =MesterPerfectMenu.Append(-1, "&Whats App")
		MesterPerfectTw =MesterPerfectMenu.Append(-1, "&Twitter")
		MesterPerfectFa =MesterPerfectMenu.Append(-1, "&Facebook")
		ContactMenu.AppendSubMenu(MesterPerfectMenu, _("Ahmed Bakr"))
		TecWindow=ContactMenu.Append(-1, "TecWindow on Telegram")
		MainMenu.AppendSubMenu(ContactMenu, _("&Contact us"))
		self.SavedArticlesItem = MainMenu.Append(-1, _("&Saved articles\tctrl+S"))
		self.FavouritesItem = MainMenu.Append(-1, _("&Favourite articles\tctrl+F"))
		self.HistoryItems = MainMenu.Append(-1, _("&History\tctrl+H"))
		self.PreferencesItem = MainMenu.Append(-1, _("Program &settings\tAlt+S"))
		self.CheckForItem = MainMenu.Append(-1, _("Check for &update\tctrl+u"))
		self.CloseProgramItem = MainMenu.Append(-1, _("Close program\tctrl+w"))
		menubar.Append(MainMenu, _("Main menu"))



		self.SetMenuBar(menubar)

		self.hotKeys = wx.AcceleratorTable([
			(wx.ACCEL_CTRL, ord("W"), self.CloseProgramItem.GetId()),
			(0, wx.WXK_F1, self.HelpFile.GetId()),
			(wx.ACCEL_CTRL, ord("U"), self.CheckForItem.GetId()),
(wx.ACCEL_CTRL, ord("R"), self.RandomArticles.GetId()),
(wx.ACCEL_CTRL, ord("H"), self.HistoryItems.GetId()),
(wx.ACCEL_CTRL, ord("S"), self.SavedArticlesItem.GetId()),
(wx.ACCEL_CTRL, ord("F"), self.FavouritesItem.GetId()),
(wx.ACCEL_ALT, ord("S"), self.PreferencesItem.GetId()),
		])
		Panel.SetAcceleratorTable(self.hotKeys)

		# Show Main window
		self.Show()


	# Check if the is there link in the clipboard in case the feature is enabled.
		if CurrentSettings["auto detect"] == "True":
			self.AutoDetect()
		# Check if the is there update in case the feature is enabled.
		if CurrentSettings["auto update"] == "True":
			threading.Thread(target=self.OnCheckForItem(None, AutoCheck="yes"), daemon=True).start()

		# events for buttons
		self.StartSearch.Bind(wx.EVT_BUTTON, self.OnViewSearch)
		self.Close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.RandomArticles.Bind(wx.EVT_BUTTON, self.OnRandomArticle)

		#events for menu items
		self.Bind(wx.EVT_MENU, self.OnAboutProgram, AboutProgramItem)
		self.Bind(wx.EVT_MENU, lambda event: SettingsDialog(self).ShowModal(), self.PreferencesItem)
		self.Bind(wx.EVT_MENU, self.OnCheckForItem, self.CheckForItem)
		self.Bind(wx.EVT_MENU, self.OnHelp, self.HelpFile)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open("mailto:ww258148@gmail.com"), QaisEm)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://t.me/QaisAlrefai"), QaisTe)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://twitter.com/qais_Alrefai"), QaisTw)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://wa.me/962792540394"), QaisWh)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://www.facebook.com/Qais1461"), QaisFa)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open("mailto:mahmoud.atef.987123@gmail.com"), MahmoodEm)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://t.me/MahmoodAtef"), MahmoodTe)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://twitter.com/mahmoud_atef999"), MahmoodTw)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://wa.me/201224660664"), MahmoodWh)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://www.facebook.com/mahmoud.atef.000"), MahmoodFa)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open("mailto:AhmedBakr593@gmail.com"), MesterPerfectEm)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://t.me/MesterPerfect"), MesterPerfectTe)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://twitter.com/my_nvda"), MesterPerfectTw)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://wa.me/201554240991"), MesterPerfectWh)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://www.facebook.com/my.nvda.1"), MesterPerfectFa)
		if CurrentSettings["language"] == "Arabic":
			self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://t.me/TecWindow"), TecWindow)
		else:
			self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://t.me/TecWindowProjects"), TecWindow)
		self.Bind(wx.EVT_MENU, self.OnClose, self.CloseProgramItem)
		self.Bind(wx.EVT_MENU, lambda event: HistoryDialog(self), self.HistoryItems)
		self.Bind(wx.EVT_MENU, lambda event: FavouritesDialog(self), self.FavouritesItem)
		self.Bind(wx.EVT_MENU, lambda event: SavedArticlesDialog(self), self.SavedArticlesItem)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.SearchText.Bind(wx.EVT_TEXT, self.OnText)



	# Creating Ontext function to disable start search buttion if search edit is empty.
	def OnText(self, event):
		self.StartSearch.Enable(enable = not self.SearchText.IsEmpty())

	#creating OnClose function to  Close Program.
	def OnClose(self, event):
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

	#creating OnAboutProgram function to show information about this program.
	def OnAboutProgram(self, event):
		AboutDialog = wx.MessageDialog(self, _("""{} Version {}.
{}
This program was developed by:
Ahmed Bakr.
Qais Alrifai.
Mahmoud Atef.""").format(ProgramName, CurrntVersion, ProgramDescription), _("About the program"), style=wx.ICON_INFORMATION+wx.OK)
		AboutDialog.SetOKLabel(_("&Ok"))
		AboutDialog.ShowModal()


	#Create a function to detect links from the clipboard
	def AutoDetect(self):
		Link = pyperclip.paste()
		if (Link.startswith("https://") and "wikipedia.org" in Link):
			title, LanguageName, LanguageCode = GetTitleFromURL(Link)
			ArticleTitle = title.replace('_', ' ')
			AutoDetectDialog = wx.MessageDialog(None, _("A link to an article with the title {} has been detected in your clipboard.").format(ArticleTitle), _("AutoDetect"), style=wx.CANCEL+wx.YES_NO+wx.YES_DEFAULT+wx.ICON_QUESTION+wx.ICON_WARNING)
			AutoDetectDialog.SetYesNoCancelLabels(_("&View Article"), _("&Open in browser"), _("&Cancel"))
			AutoDetectDialogResult = AutoDetectDialog.ShowModal()
			if AutoDetectDialogResult == wx.ID_NO:
				webbrowser.open_new(Link)
				#self.Destroy()
				#return
			elif AutoDetectDialogResult == wx.ID_YES:
				wikipedia.set_lang(LanguageCode)
				if CurrentSettings["wepviewer"] == "0":
					window1 = ViewArticleWindow(None, title, self)
				else:
					window1 = WebViewArticle(None, title, self)
				#adding the article to history.
				#Getting the date and time of visit article.
				date = datetime.date.today()
				time = datetime.datetime.now()
				time = time.strftime("%H:%M:%S")
				g.Data.InsertData("HistoryTable", (title, str(date), str(time), LanguageName))
				#self.Destroy()
				#return
			return



	#creating OnViewSearch function to show search results
	def OnViewSearch(self, event):
		CurrentSettings = Settings().ReadSettings()
		CurrentSettings["search language"] = self.LanguageSearch.Value
		Settings().WriteSettings(**CurrentSettings)

		#Set language for search
		try:
			wikipedia.set_lang(g.code[self.LanguageSearch.GetValue()])
		except:
			ConnectionError = wx.MessageDialog(self, _("There is no internet connection."), _("Connection error"), style=wx.ICON_ERROR+wx.OK)
			ConnectionError.SetOKLabel(_("&Ok"))
			ConnectionError.ShowModal()
			return None

		#geting text of search
		TextSearch = self.SearchText.Value
		# if The Search text is a Wikipedia link make the article open directly.
		if (TextSearch.startswith("https://") and "wikipedia.org" in TextSearch):
			title, LanguageName, LanguageCode = GetTitleFromURL(self.SearchText.Value)
			wikipedia.set_lang(LanguageCode)
			if CurrentSettings["wepviewer"] == "0":
				window1 = ViewArticleWindow(None, title, self)
			else:
				window1 = WebViewArticle(None, title, self)

			#adding the article to history.
			#Getting the date and time of visit article.
			date = datetime.date.today()
			time = datetime.datetime.now()
			time = time.strftime("%H:%M:%S")
			g.Data.InsertData("HistoryTable", (title, str(date), str(time), LanguageName))

			return

		#Show dialog of search results
		self.dialog1 = ViewSearch(self, TextSearch)
		#start thread function to add search results for list box in dialog.
		thread1 = threading.Thread(target=self.dialog1.OpenThread, daemon=True)
		thread1.start()

	def OnRandomArticle(self, event):

		CurrentSettings = Settings().ReadSettings()
		CurrentSettings["search language"] = self.LanguageSearch.Value
		Settings().WriteSettings(**CurrentSettings)

		#Set language for random article
		try:
			wikipedia.set_lang(g.code[self.LanguageSearch.GetValue()])
		except:
			ConnectionError = wx.MessageDialog(self, _("There is no internet connection."), _("Connection error"), style=wx.ICON_ERROR+wx.OK)
			ConnectionError.SetOKLabel(_("&Ok"))
			ConnectionError.ShowModal()
			return None
		#Show dialog of random article
		self.dialog1 = ViewSearch(self, None)
		thread1 = threading.Thread(target=self.dialog1.OpenThread, daemon=True)
		thread1.start()


	#creating function to check for update
	def OnCheckForItem(self, event, AutoCheck= "no"):

		#geting the  info recent version from online info file.
		try:
			info = GetOnlineInfo()
		except:
			if AutoCheck == "no":
				ConnectionError = wx.MessageDialog(self, _("There is no internet connection."), _("Connection error"), style=wx.ICON_ERROR+wx.OK)
				ConnectionError.SetOKLabel(_("&Ok"))
				ConnectionError.ShowModal()
			return None

		RecentVersion = info["version"]
		whatIsNew = info["What's new"]

		#Show the update dialog if there is new version.
		if version.parse(RecentVersion) > version.parse(CurrntVersion):
			UpdateDialog(self, RecentVersion, whatIsNew)
		#if there is no  new version show MessageBox tell that.
		else:
			if AutoCheck == "yes":
				pass
			else:
				LatestVersionDialog = wx.MessageDialog(self, _("You are using version {} which is the latest version.").format(CurrntVersion), _("No update available"), style=wx.ICON_INFORMATION+wx.OK)
				LatestVersionDialog.SetOKLabel(_("&Ok"))
				LatestVersionDialog.ShowModal()




	def OnHelp(self, event):

		language = {
		"English": "en",
		"Arabic": "ar",
		"Spanish": "es",
		"French": "fr"
		}

		CurrentLanguage = language[CurrentSettings["language"]]
		HelpFile = os.getcwd() + "/" + "help/" + CurrentLanguage + "/" + "HelpMe.html"

		if os.path.exists(HelpFile):
			os.startfile(HelpFile)
		else:
			os.startfile(os.getcwd() + "/" + "help/en/HelpMe.html")


#end of class


if __name__ == "__main__":
	# Create app with wx.
	app= wx.App()
	# Call up the main window.
	main_window = window()
	# make loop for the main window
	app.MainLoop()