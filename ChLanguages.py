from settings import Settings
CurrentSettings = Settings().ReadSettings()
import gettext

language = {
"english": "en", 
"arabic": "ar",
		"spanish": "es"
}

CurrentLanguage = language[CurrentSettings["Language"]]

ChangeLanguage = gettext.translation('WikiSearch', localedir='languages', languages=[CurrentLanguage])
ChangeLanguage.install()
_ = ChangeLanguage.gettext
