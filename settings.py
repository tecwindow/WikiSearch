import wx
import configparser
import os
import sys
import globals as g
from functions import *


class Settings:
	def __init__(self):

		AppData = os.path.join(os.getenv("AppData"), "WikiSearch")
		self.path = os.path.join(AppData, "Settingss.ini")

		self.config = configparser.ConfigParser()

		self.DefaultSettings = {
		"language": "English",
		"activ escape": "False",
		"results number": "20",
		"random articles number": "20",
		"auto update": "True",
		"close message": "True",
		"auto detect": "True",
		"search language": "English",
		"wepviewer": "0"
				}

	def WriteSettings(self, **NewSettings):

		try:
			self.config.read(self.path, encoding='utf-8')
		except:
			pass

		try:
			self.config.add_section("default")
		except configparser.DuplicateSectionError:
			pass

		for Setting in NewSettings:
			self.config.set("default", Setting, NewSettings[Setting])

		with open(self.path, "w", encoding='utf-8') as config_file:
			self.config.write(config_file)

	def ReadSettings(self):

		try:
			self.config.read(self.path, encoding='utf-8')
		except:
			self.WriteSettings(**self.DefaultSettings)

		CurrentSettings = self.DefaultSettings.copy()

		for Setting in CurrentSettings:
			try:
				CurrentSettings[Setting] = self.config.get("default", Setting)
			except:
				DefaultSetting = {Setting: self.DefaultSettings[Setting]}
				self.WriteSettings(**DefaultSetting)

		return CurrentSettings

	# Reset the settings to defaults.
	def ResetSettings(self):
		self.WriteSettings(**self.DefaultSettings)

#end of class

#Set language for Settings Dialog
_ = SetLanguage(Settings().ReadSettings())

# Create Settings Dialog
class SettingsDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("Program Settings"), size=(400, 600))
		#make window in center.
		self.CenterOnParent()
		#make window Minimum size.
		self.Maximize(False)
		self.CurrentSettings = Settings().ReadSettings()

		# Creating panel
		Panel = wx.Panel(self)

	# Create the notebook and the pages
		notebook = wx.Notebook(Panel)

		# general tab
		general_page = wx.Panel(notebook)

		# Creating ComboBox for languages
		LanguageTitle = wx.StaticText(general_page, -1, _("Choose language:"))
		self.ProgramLanguage = wx.ComboBox(general_page, -1, choices=['Arabic', 'English', 'Español', 'Français',], style=wx.CB_READONLY+wx.CB_SORT)
		self.ProgramLanguage.Value = self.CurrentSettings["language"]

		#creating RadioBox to chews Favorite  view.
		self.viewer = wx.RadioBox(general_page, -1, label=_("Choose your prefered view:"), choices=[_("Normal View"), _("Web View(Not recommended)")])
		self.viewer.Selection = int(self.CurrentSettings["wepviewer"])

		# Creating SpinCtrl for Results Number
		ResultsNumberTitle = wx.StaticText(general_page, -1, _("Select the number of results:"))
		self.NumberResults = wx.SpinCtrl(general_page, -1, "20", min=1, max=100, style=wx.SP_ARROW_KEYS)
		self.NumberResults.Value = self.CurrentSettings["results number"]

		# Creating SpinCtrl for random article Number
		RandomArticlesTitle = wx.StaticText(general_page, -1, _("Select the number of random articles:"))
		self.random_articles_number = wx.SpinCtrl(general_page, -1, "20", min=1, max=100, style=wx.SP_ARROW_KEYS)
		self.random_articles_number.Value = self.CurrentSettings["random articles number"]

		# Creating Check Boxes
		self.VerificationMsg = wx.CheckBox(general_page, -1, label=_("Show Close message when at least an article is open"))
		if self.CurrentSettings["close message"] == "True":
			self.VerificationMsg.Value = True

		self.AutoDetect = wx.CheckBox(general_page, -1, label=_("Auto detect links from the clipboard"))
		if self.CurrentSettings["auto detect"] == "True":
			self.AutoDetect.Value = True

		self.AutoUpdate = wx.CheckBox(general_page, -1, label=_("Check for updates automatically"))
		if self.CurrentSettings["auto update"] == "True":
			self.AutoUpdate.Value = True

		self.CloseArticleWithScape = wx.CheckBox(general_page, -1, label=_("Close the article via the Escape key"))
		if self.CurrentSettings["activ escape"] == "True":
			self.CloseArticleWithScape.Value = True

		# Creating sizer
		sizer = wx.BoxSizer(wx.VERTICAL)

		# Adding widgets to the sizer
		sizer.Add(LanguageTitle, 0, wx.ALL, 5)
		sizer.Add(self.ProgramLanguage, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(self.viewer, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(ResultsNumberTitle, 0, wx.ALL, 5)
		sizer.Add(self.NumberResults, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(RandomArticlesTitle, 0, wx.ALL, 5)
		sizer.Add(self.random_articles_number, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(self.VerificationMsg, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(self.AutoDetect, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(self.AutoUpdate, 0, wx.EXPAND|wx.ALL, 5)
		sizer.Add(self.CloseArticleWithScape, 0, wx.EXPAND|wx.ALL, 5)

		# Setting sizer to the panel
		general_page.SetSizer(sizer)
		sizer.Fit(self)

		# Add general page to the notebook
		notebook.AddPage(general_page, _("General"))

		# clean tab
		clean_page = wx.Panel(notebook)

		# Add widgets to the Clean page
		self.CleanHistoryButton = wx.Button(clean_page, -1, _("Delete history"))
		self.CleanFavouritesButton = wx.Button(clean_page, -1, _("Delete favourites"))
		self.CleanSavedArticlesButton = wx.Button(clean_page, -1, _("Delete saved articles"))
		self.DefaultSettingsButton = wx.Button(clean_page, -1, _("Reset to default settings"))

		# Creating sizer for the clean tab
		clean_sizer = wx.BoxSizer(wx.HORIZONTAL)

		# Adding widgets to the sizer
		clean_sizer.Add(self.CleanHistoryButton, 0, wx.ALL, 5)
		clean_sizer.Add(self.CleanFavouritesButton, 0, wx.ALL, 5)
		clean_sizer.Add(self.CleanSavedArticlesButton, 0, wx.ALL, 5)
		clean_sizer.Add(self.DefaultSettingsButton, 0, wx.ALL, 5)

		# Setting sizer to the clean tab panel
		clean_page.SetSizer(clean_sizer)
		clean_sizer.Fit(self)

		# add clean page to the notebook.
		notebook.AddPage(clean_page, _("Advanced"))

		# Create general Buttons
		self.SaveSettings = wx.Button(Panel, -1, _("&Save changes"))
		self.SaveSettings.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"))

		# Creating sizer for the panel
		MainSizer = wx.BoxSizer(wx.VERTICAL)
		MainSizer.Add(notebook, 1, wx.EXPAND|wx.ALL, 5)

		# Adding buttons to the sizer
		ButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
		ButtonsSizer.Add(self.SaveSettings, 0, wx.ALL, 5)
		ButtonsSizer.Add(self.GoBack, 0, wx.ALL, 5)

		# Adding buttons sizer to the MainSizer
		MainSizer.Add(ButtonsSizer, 0, wx.ALIGN_RIGHT)

    # Setting sizer to the panel
		Panel.SetSizer(MainSizer)
		MainSizer.Fit(self)

		#event for button
		self.SaveSettings.Bind(wx.EVT_BUTTON, self.OnSaveSettings)
		self.Bind(wx.EVT_BUTTON, self.OnCleanHistory, self.CleanHistoryButton)
		self.Bind(wx.EVT_BUTTON, self.OnCleanFavourites, self.CleanFavouritesButton)
		self.Bind(wx.EVT_BUTTON, self.OnCleanSavedArticles, self.CleanSavedArticlesButton)
		self.Bind(wx.EVT_BUTTON, self.OnDefaultSettings, self.DefaultSettingsButton)

		self.hotKeys = wx.AcceleratorTable([
			(wx.ACCEL_ALT, ord("S"), self.SaveSettings.GetId()),
			(wx.ACCEL_CTRL, ord("W"), self.GoBack.GetId()),
		])
		Panel.SetAcceleratorTable(self.hotKeys)


		#Show settings dialog
		self.Show()

	#Save Settings function
	def OnSaveSettings(self, event):

		languages = {
"Arabic": "Arabic",
"English": "English",
"Español": "Spanish",
"Français": "French"
}

		NewSettings = {
		"language": languages[self.ProgramLanguage.Value],
		"results number": str(self.NumberResults.Value),
		"random articles number": str(self.random_articles_number.Value),
		"close message": str(self.VerificationMsg.Value),
		"auto update": str(self.AutoUpdate.Value),
		"auto detect": str(self.AutoDetect.Value),
		"activ escape": str(self.CloseArticleWithScape.Value),
		"search language": self.CurrentSettings["search language"],
		"wepviewer": str(self.viewer.Selection)
}

		Settings().WriteSettings(**NewSettings)

		if NewSettings["language"] != self.CurrentSettings["language"]:
			ConfirmRestartProgram = wx.MessageDialog(self, _("""You must restart the program for the new language to take effect.
Do you want to restart the program now?"""), _("Confirm"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
			ConfirmRestartProgram.SetYesNoLabels(_("&Yes"), _("&No"))
			if ConfirmRestartProgram.ShowModal() == wx.ID_YES:
				os.execv(sys.executable, ['python'] + sys.argv)
			else:
				self.Destroy()

		self.Destroy()

	# reset default settings function.
	def OnDefaultSettings(self, event):
		ConfirmRestartProgram = wx.MessageDialog(self, _("""Are you sure you want to reset all settings?
The program will restart."""), _("Confirm"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
		ConfirmRestartProgram.SetYesNoLabels(_("&Yes"), _("&No"))
		if ConfirmRestartProgram.ShowModal() == wx.ID_YES:
			Settings().ResetSettings()
			os.execv(sys.executable, ['python'] + sys.argv)

	# Clean savedArticles
	def OnCleanSavedArticles(self, event):
		Confirmclean = wx.MessageDialog(self, _("Are you sure you want to delete the saved articles content?"), _("Confirm"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
		Confirmclean.SetYesNoLabels(_("&Yes"), _("&No"))
		if Confirmclean.ShowModal() == wx.ID_YES:
			g.Data.CleanTable("SavedArticlesTable")

	# Clean favourites.
	def OnCleanFavourites(self, event):
		Confirmclean = wx.MessageDialog(self, _("Are you sure you want to delete your favourites content?"), _("Confirm"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
		Confirmclean.SetYesNoLabels(_("&Yes"), _("&No"))
		if Confirmclean.ShowModal() == wx.ID_YES:
			g.Data.CleanTable("FavouritesTable")

	# Clean history.
	def OnCleanHistory(self, event):
		Confirmclean = wx.MessageDialog(self, _("Are you sure you want to delete the history content?"), _("Confirm"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
		Confirmclean.SetYesNoLabels(_("&Yes"), _("&No"))
		if Confirmclean.ShowModal() == wx.ID_YES:
			g.Data.CleanTable("HistoryTable")



#end of class

