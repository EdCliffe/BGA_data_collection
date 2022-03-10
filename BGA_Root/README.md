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

# BoardgameArena player data collection tool

> Project focused on collecting the statistics from www.boardgamearena.com for the top 20 players of each game, for the 20 games they have played most. 
> Stats: Elo ranking, number of game wins
> Also collects basic information and an associated image for each game.
> Tools used : Python, Selenium, BeautifulSoup, SQL, 
> Services used: AWS S3, AWS RDS, Dockerhub, Github

## Project scope

- The website boardgamearena was chosen because of the abundance of data available on its site, and the lack of any public analysis of this data. Potential analysis opportunities include: behavioural analysis of time onsite, comparing different high-level players statistics. For example, are the best players good at one game, or many? Specialised, or generalised?

- As a proof of concept, initally I have focussed on just the basic stats of the top players ranking in their top 20 games. Which involves:
    - Collect the links to all desired games pages
    - Collect the top 20 player links from that page, along with basic game data and an image for each game.
    - Visit those links to gather the desired stats
    - Clean the stats, store in dictionaries and lists
    - Run the test suite, check the data is as expected
    - Convert to dataframes
    - Store in the cloud

## Scraper Class - bot.py

- Answer some of these questions in the next few bullet points. What have you built? What technologies have you used? Why have you used those?

- Example: The FastAPI framework allows for fast and easy construction of APIs and is combined with pydantic, which is used to assert the data types of all incoming data to allow for easier processing later on. The server is ran locally using uvicorn, a library for ASGI server implementation.
  
```python
"""Insert your code here"""
```

> Insert an image/screenshot of what you have built so far here.

## BGA_scraper.py

- Does what you have built in this milestone connect to the previous one? If so explain how. What technologies are used? Why have you used them? Have you run any commands in the terminal? If so insert them using backticks (To get syntax highlighting for code snippets add the language after the first backticks).

- Example below:

```bash
/bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181
```

- The above command is used to check whether the topic has been created successfully, once confirmed the API script is edited to send data to the created kafka topic. The docker container has an attached volume which allows editing of files to persist on the container. The result of this is below:

```python
"""Insert your code here"""
```

> Insert screenshot of what you have built working.

## Cloud integtation

- Continue this process for every milestone, making sure to display clear understanding of each task and the concepts behind them as well as understanding of the technologies used.

- Also don't forget to include code snippets and screenshots of the system you are building, it gives proof as well as it being an easy way to evidence your experience!

## Conclusions

- Maybe write a conclusion to the project, what you understood about it and also how you would improve it or take it further.

- Read through your documentation, do you understand everything you've written? Is everything clear and cohesive?