import gettext

def SetLanguage(CurrentSettings):

	language = {
	"english": "en", 
	"arabic": "ar",
	"spanish": "es"
	}

	CurrentLanguage = language[CurrentSettings["Language"]]
	try:
		ChangeLanguage = gettext.translation('WikiSearch', localedir='languages', languages=[CurrentLanguage])
		ChangeLanguage.install()
		_ = ChangeLanguage.gettext
	except:
		_ = gettext.gettext

	return _
