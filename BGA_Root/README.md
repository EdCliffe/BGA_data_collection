# BGA_Scraper 
collects the stats of the top players of each 
game from https://boardgamearena.com, for each game they have played,
including basic information about each game itself. 

Basic Functionality is inherited from bot.py, and data cleaning
is carried out by cleaning.py. 
Once data is gathered, some tools for inspecting the data are included 
in database_access.py.
Tests/test_BGA contains the unittest class, which largely inspects 
the resulting data after the code is run.


Suggested workflow for scraping the BGA website:
run setup for dependencies
Run BGA_scraper
Run test_BGA

