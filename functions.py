import gettext

# Create a function to add translations to the program
# This function is used to identify the program with translations added to it by contributors

def SetLanguage(CurrentSettings):

# This dictionary is used to define program on language folder and on name of language within program settings
# The dictionary key indicates the name of the language within the program settings. For example: "English"
# The dictionary value indicates the folder that contains the language files. Example: "en"

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
