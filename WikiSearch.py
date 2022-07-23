#-*- coding: utf-8 -*-
# import project libraries.
import wx
import json
import nlpia2_wikipedia as wikipedia
import threading 
import webbrowser
import os
from urllib.request import urlopen
from view_search_dialog import ViewSearch
from update_dialog import UpdateDialog

# Create app with wx.
app= wx.App()

# Include List of languages in JSON format.
# Check existence of file before running program.
try:
	with open('LanguageCodes.json') as json_file:
		data = json.load(json_file)
except FileNotFoundError:
	wx.MessageBox("Some required files are missing.", "Error", style=wx.ICON_ERROR)
	Exit()

# Create empty list
name = []
code = []

# Include json file content and add it to list.
for w in data:
	name.append(w["name"])
	code.append(w["code"])

# information of program
CurrntVersion = 1.0
ProgramName = "WikiSearch"
ProgramDescription = "With this program, you can search or browse any Wikipedia article. site: https://t.me/tecwindow"

# Create main window with wx.

class window(wx.Frame):
	def __init__(self):
		super().__init__(None, title = ProgramName, size=(400, 335))
		#make window in center.
		self.Center()
		#make window Minimum size.
		self.Maximize(False)
		self.EnableMaximizeButton(False)


		# Creating panel
		Panel = wx.Panel(self)

		# Creating ComboBox for languages
		wx.StaticText(Panel, -1, "Choose the search language:", pos=(15,70), size=(380, 30))
		self.LanguageSearch = wx.ComboBox(Panel, -1, pos=(15, 100), size=(120, 40), style=wx.CB_READONLY+wx.CB_SORT)
		self.LanguageSearch.SetItems(name)
		self.LanguageSearch.Selection = 6

		# Creating  search edit
		wx.StaticText(Panel, -1, "Enter your search", pos=(160,70), size=(380, 30))
		self.SearchText = wx.TextCtrl(Panel, -1, pos=(160, 100), size=(200, 30))

		# Creating Buttons
		self.StartSearch = wx.Button(Panel, -1, "start search", pos=(10,235), size=(120,30))
		self.StartSearch.SetDefault()
		self.StartSearch.Enabled = False
		self.Close = wx.Button(Panel, -1, "Close the program", pos=(250,235), size=(120,30))

		#creating menu bar
		menubar = wx.MenuBar()
		Help = wx.Menu()
		HelpFile = Help.Append(-1, "Help file \tF1")
		AboutProgramItem = Help.Append(-1, "About")
		ContactMenu = wx.Menu()
		TecWindow=ContactMenu.Append(-1, "TecWindow on Telegram")
		QaisAlrefai=ContactMenu.Append(-1, "Qais Alrefai on Telegram")
		MahmoodAtef=ContactMenu.Append(-1, "mahmoodatef on Telegram")
		MesterPerfect = ContactMenu.Append(-1, "MesterPerfect on Telegram")
		Help.AppendSubMenu(ContactMenu, "Contact us")
		self.CheckForItem = Help.Append(-1, "Check for update")
		self.CloseProgramItem = Help.Append(-1, "Close program")
		menubar.Append(Help, "help")
		self.SetMenuBar(menubar)

		# Show Main window
		self.Show()

		# events for buttons
		self.StartSearch.Bind(wx.EVT_BUTTON, self.OnViewSearch)
		self.Close.Bind(wx.EVT_BUTTON, self.OnClose)
		#events for menu items
		self.Bind(wx.EVT_MENU, self.OnAboutProgram, AboutProgramItem)
		self.Bind(wx.EVT_MENU, self.OnCheckForItem, self.CheckForItem)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://t.me/TecWindow"), TecWindow)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://t.me/QaisAlrefai"), QaisAlrefai)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://t.me/MahmoodAtef"), MahmoodAtef)
		self.Bind(wx.EVT_MENU, lambda event: webbrowser.open_new("https://t.me/MesterPerfect"), MesterPerfect)
		self.Bind(wx.EVT_MENU, lambda event: os.startfile("help me.html"), HelpFile)
		self.Bind(wx.EVT_MENU, self.OnClose, self.CloseProgramItem)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.SearchText.Bind(wx.EVT_TEXT, lambda event: check().start())


	#creating OnClose function to  Close Program.
	def OnClose(self, event):
		wx.Exit()

	#creating OnAboutProgram function to show information about this program.
	def OnAboutProgram(self, event):
		wx.MessageBox(F"""{ProgramName} Version {CurrntVersion}.
{ProgramDescription}
		This program was developed by:
Ahmed Bakr.
Qais Alrifai.
Mahmoud Atef.""", "About the program")

	#creating OnViewSearch function to show search results
	def OnViewSearch(self, event):
		#Set language for search
		try:
			wikipedia.set_lang(code[self.LanguageSearch.GetSelection()])
		except:
			wx.MessageBox("there is no internet connection ", "Connection error", style=wx.ICON_ERROR)
			return None

		#geting text of search
		TextSearch = self.SearchText.Value
		#Show dialog of search results
		dialog1 = ViewSearch(self, TextSearch)
		#start thread function to add search results for list box in dialog.
		thread1 = threading.Thread(target=dialog1.OpenThread, daemon=True)
		thread1.start()

	#creating function to check for update
	def OnCheckForItem(self, event):
		#geting the  recent version from online info file.
		url = "https://raw.githubusercontent.com/tecwindow/WikiSearch/main/WikiSearch.json"
		try:
			response = urlopen(url)
		except:
			wx.MessageBox("there is no internet connection ", "Connection error", style=wx.ICON_ERROR)
			return None
		data_json = json.loads(response.read())
		RecentVersion = float(data_json["version"])
		#Show the update dialog if there is new version.
		if RecentVersion > CurrntVersion:
			UpdateDialog(self)
		#if there is no  new version show MessageBox tell that.
		else:
			wx.MessageBox(f"You are using version {CurrntVersion} which is the latest version.", "No update available")

# creating thread to disable start search buttion if search edit is empty.
class check(threading.Thread):
	def __init__(self):
		super(check, self).__init__()

	def run(self):
		if main_window.SearchText.IsEmpty():
			main_window.StartSearch.Enabled = False
		else:
			main_window.StartSearch.Enabled = True






main_window = window()
app.MainLoop()    