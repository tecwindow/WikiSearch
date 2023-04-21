# importing the modules
import gettext
import re
import requests
import json
import urllib.parse
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Create a function to add translations to the program
# This function is used to identify the program with translations added to it by contributors

def SetLanguage(CurrentSettings):

# This dictionary is used to define program on language folder and on name of language within program settings
# The dictionary key indicates the name of the language within the program settings. For example: "English"
# The dictionary value indicates the folder that contains the language files. Example: "en"

	language = {
	"English": "en",
	"Arabic": "ar",
	"Spanish": "es",
	"French": "fr"
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

def GetOnlineInfo():

	#load and read gson online file
	url = "https://raw.githubusercontent.com/tecwindow/WikiSearch/main/WikiSearch.json"
	response = urlopen(url)
	data_json = json.loads(response.read())

	#Putting information into a dictionary.
	info = {
	"name": data_json["name"],
	"version": data_json["version"],
	"What's new": data_json["What's new"],
	"url": data_json["url"]
	}

	return info

	# Delete The empty lines.
def remove_blank_lines(text):
    lines = text.split("\n")
    lines = list(filter(lambda x: x.strip(), lines))
    text = "\n".join(lines)
    return text

# Getting the tables of article.
def GetTables(url):

	reqs = requests.get(url)

	# using the BeautifulSoup module
	soup = BeautifulSoup(reqs.content, "html.parser")

	tables = soup.find_all("table")
	TablesText = []
 
	for i in range(len(tables)):
		content = tables[i].text
		content = remove_blank_lines(content)
		TablesText.append(content + "\n")

	return TablesText

# Include List of languages in JSON format.
def LanguageJSON():
# Check existence of file before running program.
	try:
		with open('LanguageCodes.json', encoding="utf-8") as json_file:
			data = json.load(json_file)
	except FileNotFoundError:
		wx.MessageBox(_("Some required files are missing."), _("Error"), style=wx.ICON_ERROR)
		exit()

	# Create a empty  list and dictionary.
	name = []
	code = {}

	# Include json file content and add it to list.
	for w in data:
		name.append(w["name"])
		code[w["name"]] = w["code"]

	return name, code

	# Get title and language of any article from its link.
def GetTitleFromURL(url):

	url = urllib.parse.unquote(url)
	url = url.split('/')

	LanguageCode = url[2].split(".")[0]
	title = url[-1]

	code = LanguageJSON()[1]
	keys = list(code.keys())
	Values = list(code.values())
	LanguageName = keys[Values.index(LanguageCode)]

	return title, LanguageName, LanguageCode

# Analyze the text.
def count_text_items(text):
	lines = text.count('\n') + 1
	paragraphs = text.count('\n\n') + 1
	sentences = len(re.findall(r'[^.!?]+[.!?]', text))
	words = len(re.findall(r'\b\w+\b', text))
	characters = len(text) + 1
    
	information = {
	'lines': lines,
	'paragraphs': paragraphs,
	'sentences': sentences,
	'words': words,
	'characters': characters
	}

	return information
