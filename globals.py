import os
from my_classes import DB

DBFile = os.path.join(os.getenv("AppData"), "WikiSearch", "WikiSearch.db")
global Data
if not os.path.exists(DBFile):
	Data = DB(DBFile)
	Data.CreateTable("HistoryTable", ("Title", "Date", "Time", "Article language name", "Article language code"))
else:
	Data = DB(DBFile)

global NumberArticle
NumberArticle = 0

global ArticleLanguageCode
ArticleLanguageCode = "None"