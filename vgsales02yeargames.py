import sqlite3
import seaborn
import matplotlib

yeardict=dict() # A DICTIONARY WITH YEARID AND YEAR
yearcountdict=dict() # A DICTIONARY WITH YEARID AND COUNTS
yearcountlist=list() # A LIST WITH count and year
yearlist=list() # A LIST WITH year
countlist=list() # A LIST WITH count

filesqlcon=sqlite3.connect('vgsales-clean.sqlite')
filesql=filesqlcon.cursor()

filetxt=open('2. Which year had the most game release.txt','w')

# RETRIEVE YEARID AND YEAR FROM TABLE YEAR
filesql.execute('select id,year from Year')
yearidyear=filesql.fetchall() # returns a list of tuples of 2 elements

# CREATE A DICT WITH YEARID AND YEAR. [yearid:year]
for yearid,year in yearidyear:
   yeardict[yearid]=year

# RETRIEVE YEARID FROM TABLE GAME
filesql.execute('select year_id from Game')
yearidlist=filesql.fetchall() # fetchall will return a list of tuples of 2 elements (yearid,)

# COUNT YEARID USING A DICTIONARY. [yearid:count]
for yearid in yearidlist:
   yearidvalue=yearid[0] # grab the 1st element of the tuple yearid
   yearcountdict[yearidvalue]=yearcountdict.get(yearidvalue,0)+1

# CREATE A LIST WITH COUNT AND YEAR AND SORT IT BY COUNT IN DESCENDING ORDER.
for yearid,count in yearcountdict.items():
   yearcountlist.append((count,str(yeardict[yearid]))) # instead of storing the yearid store the year as string, retrieving it from yeardict.

yearcountlist=sorted(yearcountlist,reverse=True)

# PRINT THE LIST ORDERED BY COUNT

print('2. Which year had the most game release?\n\nYear Game_count\n')
filetxt.write('2. Which year had the most game release?\n\nYear Game_count\n\n')

countmax=0
yearmax=''
for count,year in yearcountlist:
   wordprint=year+': '+str(count)
   print(wordprint)
   wordprint=wordprint+'\n'
   filetxt.write(wordprint)

   yearlist.append(year)
   countlist.append(count)

   # MAX YEAR COUNT

   if count>=countmax:
      countmax=count
      yearmax=year+' '+yearmax

wordprint='\n'+yearmax+'is/are the year(s) with most games.'
print(wordprint)
filetxt.write(wordprint)
wordprint='Year 0 represents games with unknown year of release.'
print(wordprint)
wordprint='\n'+wordprint
filetxt.write(wordprint)
filetxt.close

# PLOT WITH SEABORN (MATPLOTLIB)

matplotlib.pyplot.figure(figsize=(8,6)) # width,height in inches

plot=seaborn.barplot(x=yearlist,y=countlist) # create barplot object

plot.bar_label(plot.containers[0],rotation=90,padding=5) # put labels on bars (count)

matplotlib.pyplot.xticks(rotation=90) # rotate x axis labels 90 degrees

matplotlib.pyplot.title('2. Which year had the most game release')
matplotlib.pyplot.xlabel('Year') # axes names
matplotlib.pyplot.ylabel('Game count')

seaborn.despine() # remove top and right lines

axisgca=matplotlib.pyplot.gca() # show y grid
axisgca.yaxis.grid(linestyle='--')
axisgca.set_axisbelow(True)

matplotlib.pyplot.savefig('2. Which year had the most game release.jpg',dpi=200)

matplotlib.pyplot.show()