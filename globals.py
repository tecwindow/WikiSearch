import os
from my_classes import DB
from functions import LanguageJSON

DBFile = os.path.join(os.getenv("AppData"), "WikiSearch", "WikiSearch.db")
global Data
if not os.path.exists(DBFile):
	Data = DB(DBFile)
	Data.CreateTable("HistoryTable", ("Title", "Date", "Time", "Article language name"))
	Data.CreateTable("FavouritesTable", ("Title", "Name", "Article language name", "url"))
else:
	Data = DB(DBFile)

global NumberArticle
NumberArticle = 0

global name, code
name, code = LanguageJSON()
