vgsalestodatabase.py

==============================

Skills:

SQL
Python

==============================

Description: A Python script that creates an sqlite relational database with the data in the csv
Excel file created after cleaning the dataset (for details on the cleaning process see separate 
folder and files vgsales-csv-data-cleaning).

==============================

Running the code:

-From windows command prompt, execute the .py file by writing "python filename.py"

==============================

Requirements:

-Python 3.7.1 or superior installed

==============================

Output:

-sqlite relational database file (.sqlite) with a Game,Genre,Platform,Publisher,Year table.

==============================

About the csv Excel dataset

Fields (columns): Rank,Name,Platform,Year,Genre,Publisher,NA_Sales,EU_Sales,JP_Sales,Other_Sales,Global_Sales
(see description of each field in separate file)

The dataset has games from 1980 through 2020. But for the years 2017 and 2020 there is
few data collected so those years though included in the plots should be disregarded. There
is no data from 2018 or 2019.

Missing fields: have been replaced by ~Unknown. In the case of unknown Year, a 0 was inserted
into the database (so all fields are integers).

==============================

About the sqlite database:

5 Tables:
Game, Platform, Publisher, Genre, Year

Game table:
id,name,NA_sales,EU_sales,JP_sales,Other_sales,Global_sales,rank,platform_id,publisher_id,genre_id,year_id

Platform table:
id,platform

PUblisher table:
id,pUblisher

Genre table:
id,genre

Year table:
id,year

Genres: 12
-Action
-Adventure
-Fighting
-Misc
-Platform
-Puzzle
-Racing
-Role-Playing
-Shooter
-Simulation
-Sports
-Strategy

Platform: 31
(see pdf list or screenshot)

Publishers: 578
(see pdf list or screenshot)

Years: 40
1980-2020 (except 2018,2019)
(see pdf list or screenshot)

Games: 16598
(see screenshot, pdf too long to print)

==============================

Files uploaded:

-python script: vgsalestodatabase.py
-SQLITE DATABASE: vgsales-clean.sqlite
-screenshots of database Tables: Game,Genre,Platform,Publisher,Year
-screenshots of games for the years 2017 and 2020 (3 and 1 respectively)
-screenshots of windows command prompt
-Pdf prints of database Schema and all tables except Games (too long)
