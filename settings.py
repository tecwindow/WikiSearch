import wx
import configparser
import os
import sys
from ChLanguages import *

class Settings:
	def __init__(self):

		AppData = os.getenv("AppData")
		AppData = AppData + "/" + "WikiSearch"

		if not os.path.exists(AppData):
			os.mkdir(AppData)

		filename = "Settingss.ini"
		self.path = AppData + "/" + filename

		self.config = configparser.ConfigParser()

		self.DefaultSettings = {
		"Language": "english",
		"ActivEscape": "False",
		"ResultsNumber": "20",
		"AutoUpdate": "True",
		"CloseMessage": "True",
		"SearchLanguage": "English"
				}

	def WriteSettings(self, **NewSettings):

		try:
			self.config.add_section("default")
		except configparser.DuplicateSectionError:
			pass

		self.config.set("default", "language", NewSettings["Language"])
		self.config.set("default", "activ escape", NewSettings["ActivEscape"])
		self.config.set("default", "results number", NewSettings["ResultsNumber"])
		self.config.set("default", "auto update", NewSettings["AutoUpdate"])
		self.config.set("default", "close message", NewSettings["CloseMessage"])
		self.config.set("default", "search language", NewSettings["SearchLanguage"])

		with open(self.path, "w") as config_file:
			self.config.write(config_file)

	def ReadSettings(self):

		while 1:
			try:
				self.config.read(self.path)
				CurrentSettings = {
				"Language": self.config.get("default", "language"),
				"ActivEscape": self.config.get("default", "activ escape"),
				"ResultsNumber": self.config.get("default", "results number"),
				"AutoUpdate": self.config.get("default", "auto update"),
				"CloseMessage": self.config.get("default", "close message"),
				"SearchLanguage": self.config.get("default", "search language")
				}
				break
			except:
				self.WriteSettings(**self.DefaultSettings)
				continue

		return CurrentSettings

#end of class

# Create main window with wx.
class SettingsDialog(wx.Dialog):
	def __init__(self):
		super().__init__(None, title=_("Program Settings"), size=(400, 335))
		#make window in center.
		self.Center()
		#make window Minimum size.
		self.Maximize(False)
		self.CurrentSettings = Settings().ReadSettings()

		# Creating panel
		Panel = wx.Panel(self)

		# Creating ComboBox for languages
		wx.StaticText(Panel, -1, _("Choose language:"), pos=(15,20), size=(380, 30))
		self.ProgramLanguage = wx.ComboBox(Panel, -1, choices=['arabic', 'english', 'spanish'], pos=(15, 50), size=(120, 40), style=wx.CB_READONLY+wx.CB_SORT)
		self.ProgramLanguage.Value = self.CurrentSettings["Language"]

		# Creating SpinCtrl for Results Number
		wx.StaticText(Panel, -1, _("Choose the number of results:"), pos=(140,20), size=(380, 30))
		self.NumberResults = wx.SpinCtrl(Panel, -1, "20", min=1, max=100, style=wx.SP_ARROW_KEYS, pos=(160, 50), size=(50, 20))
		self.NumberResults.Value = self.CurrentSettings["ResultsNumber"]

		# Creating Check Boxes
		self.VerificationMsg = wx.CheckBox(Panel, -1, label=_("Show Close message when at least an article is open"), pos=(10, 80), size=(380, 30))
		if self.CurrentSettings["CloseMessage"] == "True":
			self.VerificationMsg.Value = True

		self.AutoUpdate = wx.CheckBox(Panel, -1, label=_("Check for updates automatically"), pos=(10, 110), size=(380, 30))
		if self.CurrentSettings["AutoUpdate"] == "True":
			self.AutoUpdate.Value = True

		self.CloseArticleWithScape = wx.CheckBox(Panel, -1, label=_("Close the article via the Escape key"), pos=(10, 140), size=(380, 30))
		if self.CurrentSettings["ActivEscape"] == "True":
			self.CloseArticleWithScape.Value = True

		# Create Buttons
		self.SaveSettings = wx.Button(Panel, -1, _("&Save changes"), pos=(10,190), size=(100,30))
		self.SaveSettings.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"), pos=(120,190), size=(80,30))

		#event for Save Settings button
		self.SaveSettings.Bind(wx.EVT_BUTTON, self.OnSaveSettings)

		# Show Main window
		self.Show()

	#Save Settings function
	def OnSaveSettings(self, event):

		NewSettings = {
		"Language": self.ProgramLanguage.Value,
		"ResultsNumber": str(self.NumberResults.Value),
		"CloseMessage": str(self.VerificationMsg.Value),
		"AutoUpdate": str(self.AutoUpdate.Value),
		"ActivEscape": str(self.CloseArticleWithScape.Value),
		"SearchLanguage": self.CurrentSettings["SearchLanguage"]
}

		Settings().WriteSettings(**NewSettings)

		self.Destroy()

		if NewSettings["Language"] != self.CurrentSettings["Language"]:
			ConfirmRestartProgram = wx.MessageDialog(self, _("""You must restart the program for the new language to take effect.
Do you want to restart the program now?"""), _("Confirm"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
			if ConfirmRestartProgram.ShowModal() == wx.ID_YES:
				os.execv(sys.executable, ['python'] + sys.argv)
			else:
				return None


#end of class
