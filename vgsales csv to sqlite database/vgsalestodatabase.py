import sqlite3

filename=input('Enter file name: ')
file=open(filename)

filenamesql=filename.replace('.csv','.sqlite')
filesqlcon=sqlite3.connect(filenamesql)
filesql=filesqlcon.cursor()

# CREATE TABLES IN RELATIONAL DATABASE (5)

filesql.executescript('''create table if not exists Game(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,name TEXT,
                         NA_sales REAL,EU_sales REAL,JP_sales REAL,Other_sales REAL,Global_sales REAL,rank INTEGER UNIQUE,
                         platform_id INTEGER,publisher_id INTEGER,genre_id INTEGER,year_id INTEGER);
                         create table if not exists Platform(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,platform TEXT UNIQUE);
                         create table if not exists Publisher(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,publisher TEXT UNIQUE);
                         create table if not exists Genre(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,genre TEXT UNIQUE);
                         create table if not exists Year(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,year INTEGER UNIQUE);''')

# CSV FILE columns: Rank,Name,Platform,Year,Genre,Publisher,NA_Sales,EU_Sales,JP_Sales,Other_Sales,Global_Sales
# linelist index    0    1    2        3    4     5         6        7        8        9           10

# INSERT VALUES IN THE TABLES

print('Inserting data into sqlite database...')

countrow11=0
countrowother=0
for line in file:
   linelist=line.split(',')
   if len(linelist)==11:

      #INSERT PLATFORM
      filesql.execute('insert or ignore into Platform(platform) values(?)',(linelist[2],))
      filesql.execute('select id from Platform where platform=?',(linelist[2],))
      platformid=filesql.fetchone()[0]

      #INSERT PUBLISHER
      filesql.execute('insert or ignore into Publisher(publisher) values(?)',(linelist[5],))
      filesql.execute('select id from Publisher where publisher=?',(linelist[5],))
      publisherid=filesql.fetchone()[0]

      #INSERT GENRE
      filesql.execute('insert or ignore into Genre(genre) values(?)',(linelist[4],))
      filesql.execute('select id from Genre where genre=?',(linelist[4],))
      genreid=filesql.fetchone()[0]

      #INSERT YEAR
      try:
         yearint=int(linelist[3]) # if the year is an integer, ok
      except:
         yearint=0 # if it's a string or '~Unknown', put 0
      filesql.execute('insert or ignore into Year(year) values(?)',(yearint,))
      filesql.execute('select id from Year where year=?',(yearint,))
      yearid=filesql.fetchone()[0]

      #INSERT GAME
      filesql.execute('''insert or ignore into Game(name,NA_Sales,EU_Sales,JP_Sales,Other_Sales,Global_Sales,rank,platform_id,publisher_id,genre_id,year_id) 
                         values(?,?,?,?,?,?,?,?,?,?,?)''',
                         (linelist[1],float(linelist[6]),float(linelist[7]),float(linelist[8]),float(linelist[9]),float(linelist[10]),int(linelist[0]),platformid,publisherid,genreid,yearid))
      countrow11=countrow11+1
   else:
      countrowother=countrowother+1

print('Rows inserted in database:',countrow11)
print('Rows discarded:',countrowother)
filesqlcon.commit()
