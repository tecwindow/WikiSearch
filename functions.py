# importing the modules
import gettext
import re
import requests
from bs4 import BeautifulSoup



# Create a function to add translations to the program
# This function is used to identify the program with translations added to it by contributors

def SetLanguage(CurrentSettings):

# This dictionary is used to define program on language folder and on name of language within program settings
# The dictionary key indicates the name of the language within the program settings. For example: "English"
# The dictionary value indicates the folder that contains the language files. Example: "en"

	language = {
	"English": "en",
	"Arabic": "ar",
	"Español": "es",
	"Français": "fr"
	}

	try:
		CurrentLanguage = language[CurrentSettings["language"]]
	except:
		_ = gettext.gettext
		return _

	try:
		ChangeLanguage = gettext.translation('WikiSearch', localedir='languages', languages=[CurrentLanguage])
		ChangeLanguage.install()
		_ = ChangeLanguage.gettext
	except:
		_ = gettext.gettext

	return _

def DisableLink(HtmlContent):
	HtmlContent = HtmlContent
	pattern =r'(href\=\".*?\")'
	result = re.sub(pattern, 'role="link" aria-disabled="false"', HtmlContent, flags=re.MULTILINE)
	return result