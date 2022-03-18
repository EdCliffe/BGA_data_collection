# BGA_Scraper 
Collects the stats of the top players of each 
game from https://boardgamearena.com, for each game they have played,
including basic information about each game itself. 

Basic Functionality is inherited from bot.py, and data cleaning
is carried out by cleaning.py. 
The data storage is integrated with cloud services in cloud.py.
Once data is gathered, some tools for inspecting the data are included 
in database_access.py.
Tests/test_BGA contains the unittest class, which inspects 
the resulting data after the code is run.


Suggested workflow for scraping the BGA website:
Run BGA_scraper
Run test_BGA

# BoardgameArena player data collection tool

> Project focused on collecting the statistics from www.boardgamearena.com for the top 20 players of each game, for the 20 games they have played most. 
> Stats: Elo ranking, number of game wins
> Also collects basic information and an associated image for each game.
> Tools used : Python, Selenium, BeautifulSoup, SQL, 
> Services used: AWS S3, AWS RDS, Dockerhub, Github

## Project scope

> The website boardgamearena was chosen because of the abundance of data available on its site, and the lack of any public analysis of this data. Potential analysis opportunities include: behavioural analysis of time spent playing, and comparing different high-level player's statistics. For example, are the best players good at one game, or many? Specialised, or generalised?

> As a proof of concept, initally I have focused on just the basic stats of the top players ranking in their top 20 games. Which involves:
    > Collect the links to all desired games pages
    > Collect the top 20 player links from that page, along with basic game data and an image for each game.
    > Visit those links to gather the desired stats
    > Clean the stats, store in dictionaries and lists
    > Run the test suite, check the data is as expected
    > Convert to dataframes
    > Store in the cloud

## Scraper Class - bot.py

> This defines some generic scraping tools, which are then inherited by the class defined within BGA_scraper.py for use with boardgamearena.com. 

> Defining a generic scraper class allows this framework to be more easily adapted for new purposes in the future.

> Selenium is used primarily when webpage interaction is required. Methods include sending keys to a web element, clicking a button, and collecting data from the webpage.

> BeautifulSoup is used for gathering a whole webpage when there are is no page interaction required. Methods include creating a BS object from the html link, and gathering data from a table from that BS object.


## BGA_scraper.py

> The class BGAscraper inherits many methods from Scraper, in bot.py. It uses these methods to create more complex sequences in order to gather data from BGA. This file does not stand alone, as well as inheriting from Scraper, it relies on cleaning.py and cloud.py

> The function run_scraper is of particular importance, as it calls the methods in order to execute the full workflow. Which is as follows:
    > Gather list of game urls with BeautifulSoup
    > log in using selenium
    > gather tabular data, and save images
    > clean tabular data
    > save results to file, sorted by collection date

The 'if __name__ == "__main__"' block calls this function, along with a timer, and then calls cloud.py to store the data in the cloud.



## Cloud integtation
> This script takes the data dictionaries and images, converts them to pandas dataframes, and stores using AWS cloud services. Images are sent to an S3 bucket, whereas the dataframes are stored in RDS. Which is then connected to pgAdmin4.
*Screenshot*

> The player statistics are initially stored in nested dictionaries by BGAscraper. This is not ideal for storing in an RDS database, and so to avoid needing hundreds and thousands of Postgres tables, some reorgansing of the data into fewer, larger tables is required.
*Screenshot*

> Potential improvement: organse the data into this dataframe format during original processing, instead of nested dictionaries. 

## Remote Monitoring
> Prometheus and node_exporter were set up on the EC2, and Grafana was used to connect to these targets from my local machine. I created a dashboard to monitor docker processes, and OS processes taking place on the EC2 while I ran the Scraper.
*Screenshots*

## Conclusions

- Maybe write a conclusion to the project, what you understood about it and also how you would improve it or take it further.

- Read through your documentation, do you understand everything you've written? Is everything clear and cohesive?




- Answer some of these questions in the next few bullet points. What have you built? What technologies have you used? Why have you used those?

```python
"""Insert your code here"""
```

> Insert an image/screenshot of what you have built so far here.


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


- Continue this process for every milestone, making sure to display clear understanding of each task and the concepts behind them as well as understanding of the technologies used.

- Also don't forget to include code snippets and screenshots of the system you are building, it gives proof as well as it being an easy way to evidence your experience!
