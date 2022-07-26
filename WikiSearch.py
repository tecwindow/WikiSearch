﻿#-*- coding: utf-8 -*-
# import project libraries.
import wx
import json
import nlpia2_wikipedia as wikipedia
import threading 
import webbrowser
import os
import sys
#change working dir to main exe dir
os.chdir(os.path.dirname(sys.argv[0]))
from view_search_dialog import ViewSearch
from update_dialog import UpdateDialog
from settings import *
from functions import *
from dialogs import HistoryDialog
from globals import *
from packaging import version

#Set language for main window 
_ = SetLanguage(Settings().ReadSettings())

# Create app with wx.
app= wx.App()

# Include List of languages in JSON format.
# Check existence of file before running program.
try:
	with open('LanguageCodes.json', encoding="utf-8") as json_file:
		data = json.load(json_file)
except FileNotFoundError:
	wx.MessageBox(_("Some required files are missing."), _("Error"), style=wx.ICON_ERROR)
	exit()

# Create empty list
name = []
code = {}

# Include json file content and add it to list.
for w in data:
	name.append(w["name"])
	code[w["name"]] = w["code"]

# information of program
CurrntVersion = "1.3.0"
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
		self.LanguageSearch.SetItems(name)
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
		self.HistoryItems = MainMenu.Append(-1, _("&History\tAlt+H"))
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
(wx.ACCEL_ALT, ord("S"), self.PreferencesItem.GetId()),
		])
		Panel.SetAcceleratorTable(self.hotKeys)

		# Show Main window
		self.Show()

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
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://t.me/TecWindow"), TecWindow)
		self.Bind(wx.EVT_MENU, self.OnClose, self.CloseProgramItem)
		self.Bind(wx.EVT_MENU, self.OnHistory, self.HistoryItems)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.SearchText.Bind(wx.EVT_TEXT, self.OnText)

	# Creating Ontext function to disable start search buttion if search edit is empty.
	def OnText(self, event):
		self.StartSearch.Enable(enable = not self.SearchText.IsEmpty())

	#creating OnClose function to  Close Program.
	def OnClose(self, event):
		global Data, NumberArticle
		try:
			if NumberArticle == 1:
							ArticleCounte = _("There is 1 open article.")
			elif self.dialog1.NumberArticle > 1:
				ArticleCounte = _("There are {} open articles.").format(NumberArticle)
			if NumberArticle >= 1:
				ConfirmClosProgram = wx.MessageDialog(self,_("""{}
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
		except AttributeError:
			wx.Exit()
			Data.CloseConnection()

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



	#creating OnViewSearch function to show search results
	def OnViewSearch(self, event):
		CurrentSettings = Settings().ReadSettings()
		CurrentSettings["search language"] = self.LanguageSearch.Value
		Settings().WriteSettings(**CurrentSettings)

		#Set language for search
		global ArticleLanguageCode
		ArticleLanguageCode = code[self.LanguageSearch.GetValue()]
		try:
			wikipedia.set_lang(ArticleLanguageCode)
		except:
			ConnectionError = wx.MessageDialog(self, _("There is no internet connection."), _("Connection error"), style=wx.ICON_ERROR+wx.OK)
			ConnectionError.SetOKLabel(_("&Ok"))
			ConnectionError.ShowModal()
			return None

		#geting text of search
		TextSearch = self.SearchText.Value
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
		global ArticleLanguageCode
		ArticleLanguageCode = code[self.LanguageSearch.GetValue()]
		try:
			wikipedia.set_lang(ArticleLanguageCode)
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
		"Español": "es",
		"Français": "fr"
		}

		CurrentLanguage = language[CurrentSettings["language"]]
		HelpFile = os.getcwd() + "/" + "help/" + CurrentLanguage + "/" + "HelpMe.html"

		if os.path.exists(HelpFile):
			os.startfile(HelpFile)
		else:
			os.startfile(os.getcwd() + "/" + "help/en/HelpMe.html")

	#Creating function to show history dialog
	def OnHistory(self, event):
			HistoryDialog(self)
#end of class


main_window = window()

if CurrentSettings["auto update"] == "True":
	threading.Thread(target=main_window.OnCheckForItem(None, AutoCheck="yes"), daemon=True).start()

app.MainLoop()    