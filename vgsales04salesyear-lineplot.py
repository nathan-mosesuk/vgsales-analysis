import sqlite3
import matplotlib
import seaborn
from decimal import Decimal

idyeardict=dict() # DICTIONARY WITH THE IDS AND YEAR
yearsalesdict=dict() # DICTIONARY WITH YEAR ID AND GLOBAL SALES
yearsaleslist=list() # LIST WITH YEAR STR AND GLOBAL SALES
yearlist=list() # LIST FOR YEAR STR 
globalsaleslist=list() # LIST FOR GLOBAL SALES

filesqlcon=sqlite3.connect('vgsales-clean.sqlite')
filesql=filesqlcon.cursor()

filetxt=open('4. Which year had the highest sales worldwide.txt','w')

# RETRIEVE YEAR ID AND YEAR FROM TABLE YEAR
filesql.execute('select id,year from Year')
idyearlist=filesql.fetchall() # a list of tuples (id,year)

# CREATE A DICTIONARY WITH THE IDS AND YEAR
for id,year in idyearlist:
   idyeardict[id]=year

# RETRIEVE YEAR ID AND GLOBAL SALES LIST FROM TABLE GAME
filesql.execute('select year_id,Global_sales from Game')
yearidsaleslist=filesql.fetchall() # a list of tuples (year_id,Global_sales)

# CREATE A DICTIONARY TO SUM GLOBAL SALES FOR EVERY YEAR
for yearid,globalsales in yearidsaleslist:
   yearsalesdict[yearid]=yearsalesdict.get(yearid,Decimal(0.0))+Decimal(globalsales) # use Decimal to improve precision and avoid wrong decimals.

# CREATE A LIST WITH YEAR STR AND GLOBAL SALES
for yearid,globalsales in yearsalesdict.items():
   yearstr=str(idyeardict[yearid]) # retrieves the year as integer and converts to str
   if yearstr=='0': continue # this ommits storing year 0
   yearsaleslist.append((yearstr,globalsales))

yearsaleslist=sorted(yearsaleslist,reverse=False) # will order by year in ascending order, instead of descending

filetxt.write('4. Which year had the highest sales worldwide\n\nYear Global_Sales (in millions)\n\n')
print('\n4. Which year had the highest sales worldwide\n\nYear Global_Sales (in millions)\n')

# CREATE 2 INDEPENDENT LISTS FOR YEAR STR AND GLOBAL SALES
globalsalesmax=None
yearmax=''
for year,globalsales in yearsaleslist:
   yearlist.append(year)
   globalsaleslist.append(round(globalsales,2))

   #PRINT YEARS AND GLOBAL SALES IN TXT
   wordprint=year+' '+str(round(globalsales,2))
   print(wordprint)
   wordprint=wordprint+'\n'
   filetxt.write(wordprint)

   # MAX SALES
   if globalsalesmax==None:
      globalsalesmax=globalsales
   if globalsales>globalsalesmax:
      globalsalesmax=globalsales

#RE CHECK IF THERE ARE MORE THAN ONE YEAR WITH THE SAME MAX SALES AND STORE YEARMAX
for year,globalsales in yearsaleslist:
   if globalsales==globalsalesmax:
      yearmax=year+' '+yearmax

wordprint='\n'+yearmax+'is/are the year(s) with most global sales.'
print(wordprint)
filetxt.write(wordprint)
filetxt.close

# PLOT WITH MATPLOTLIB

figureplot=matplotlib.pyplot.figure(figsize=(13,6))
ax=figureplot.add_subplot()

matplotlib.pyplot.plot(yearlist,globalsaleslist,linewidth=1)

for i in range(len(yearlist)):
   ax.text(i,globalsaleslist[i]+25,globalsaleslist[i],rotation=90,ha='center',size='small')

matplotlib.pyplot.xticks(rotation=90)

matplotlib.pyplot.title('4. Which year had the highest sales worldwide',loc='left')
matplotlib.pyplot.xlabel('Year')
matplotlib.pyplot.ylabel('Global Sales (in millions)')

seaborn.despine() # remove top and right lines

axisgca=matplotlib.pyplot.gca() # show y grid
axisgca.yaxis.grid(linestyle='--')
axisgca.set_axisbelow(True)

matplotlib.pyplot.savefig('4. Which year had the highest sales worldwide.jpg',dpi=200)

matplotlib.pyplot.show()
