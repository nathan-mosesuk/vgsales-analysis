import matplotlib
import seaborn
import sqlite3
import numpy
from decimal import Decimal

idgenredict=dict() # A DICTIONARY TO STORE GENREID AND GENRE
genreidsalesdict={} # A NESTED DICTIONARY TO SUM THE SALES OF EACH REGION
genreregionsaleslist=list() # A LIST TO STORE TOTAL GLOBAL SALES, GENRE, AND REGIONAL SALES. ORDER LIST BY GLOBAL SALES
globalsaleslist=list() # A LIST TO STORE GLOBAL SALES PER GENRE
genrelist=list() # A LIST TO STORE GENRES
NAsaleslist=list() # A LIST TO STORE NA SALES PER GENRE
EUsaleslist=list() # A LIST TO STORE EU SALES PER GENRE
JPsaleslist=list() # A LIST TO STORE JP SALES PER GENRE
Othersaleslist=list() # A LIST TO STORE OTHER SALES PER GENRE

filesqlcon=sqlite3.connect('vgsales-clean.sqlite')
filesql=filesqlcon.cursor()

filename='10. Sales comparison by genre'
filetext=filename+'.txt'
filetxt=open(filetext,'w')
print('\n10. Sales comparison by genre')
filetxt.write('10. Sales comparison by genre\n')

# RETRIEVE GENRE ID AND SALES FROM TABLE GENRE
filesql.execute('select genre_id,Global_sales,NA_sales,EU_sales,JP_sales,Other_sales from Game')
genreidsaleslist=filesql.fetchall()

# RETRIEVE GENRE ID AND GENRE FROM TABLE GENRE
filesql.execute('select id,genre from Genre')
idgenrelist=filesql.fetchall()

# CREATE A DICTIONARY TO STORE GENREID AND GENRE
for id,genre in idgenrelist:
   idgenredict[id]=genre

# CREATE A NESTED DICTIONARY TO SUM THE SALES OF EACH REGION
for genreid,Globalsales,NAsales,EUsales,JPsales,Othersales in genreidsaleslist:
   genreidsalesdict[genreid]=genreidsalesdict.get(genreid,{}) # create the key genreid first, if it doesn't exist
   genreidsalesdict[genreid]['Globalsales']=genreidsalesdict.get(genreid,{}).get('Globalsales',Decimal(0.0))+Decimal(Globalsales)
   genreidsalesdict[genreid]['NAsales']=genreidsalesdict.get(genreid,{}).get('NAsales',Decimal(0.0))+Decimal(NAsales)
   genreidsalesdict[genreid]['EUsales']=genreidsalesdict.get(genreid,{}).get('EUsales',Decimal(0.0))+Decimal(EUsales)
   genreidsalesdict[genreid]['JPsales']=genreidsalesdict.get(genreid,{}).get('JPsales',Decimal(0.0))+Decimal(JPsales)
   genreidsalesdict[genreid]['Othersales']=genreidsalesdict.get(genreid,{}).get('Othersales',Decimal(0.0))+Decimal(Othersales)

# CREATE A LIST TO STORE TOTAL GLOBAL SALES, GENRE, AND REGIONAL SALES. ORDER LIST BY GLOBAL SALES
for genreid,regionsales in genreidsalesdict.items(): # create a list out of the dict. regionsales is a dictionary {}
   genreregionsaleslist.append((genreidsalesdict[genreid]['Globalsales'],idgenredict[genreid],genreidsalesdict[genreid]['NAsales'],genreidsalesdict[genreid]['EUsales'],genreidsalesdict[genreid]['JPsales'],genreidsalesdict[genreid]['Othersales']))
   # it will have 6-element tuples

genreregionsaleslist=sorted(genreregionsaleslist,reverse=True) # will sort by global sales

# THE CATEGORIES ARE THE GENRES (12). THE SUBCATEGORIES ARE THE REGIONAL SALES (4).
# WE NEED TO CREATE LISTS WITH ALL REGIONAL SALES FOR EVERY GENRE (12 LISTS IN TOTAL)

# CREATE 3 INDEPENDENT LISTS AND PRINT GENRE AND SALES
filetxt.write('\nGenre  NA_sales EU_sales JP_sales Other_sales Global_sales (in millions)\n\n')
print('\nGenre  NA_sales EU_sales JP_sales Other_sales Global_sales (in millions)\n')

for Globalsales,genre,NAsales,EUsales,JPsales,Othersales in genreregionsaleslist:
   Globalsales=round(Globalsales,2) # round values to 2 decimals
   NAsales=round(NAsales,2)
   EUsales=round(EUsales,2)
   JPsales=round(JPsales,2)
   Othersales=round(Othersales,2)
   globalsaleslist.append(Globalsales)
   genrelist.append(genre)
   NAsaleslist.append(NAsales)
   EUsaleslist.append(EUsales)
   JPsaleslist.append(JPsales)
   Othersaleslist.append(Othersales)
   wordprint=genre+'  '+str(NAsales)+' '+str(EUsales)+' '+str(JPsales)+' '+str(Othersales)+'  '+str(Globalsales)
   print(wordprint)
   wordprint=wordprint+'\n'
   filetxt.write(wordprint)

#PLOT SUBPLOTS WITH MATPLOTLIB

matplotlib.pyplot.figure(figsize=(14,6)) # WIDTH BY HEIGHT

locationslist=list(range(len(genrelist))) # [0,1,2,3...]
locationslistnpy=numpy.array(locationslist) # convert list to numpy narray to operate with vectorization.

width=0.2 # it's the width of each individual bar. There's gonna be 4 per genre. Total length 0.8

fig,ax=matplotlib.pyplot.subplots()

# PLOT EACH BAR SUBPLOT, AND USE NUMPY VECTORIZATION TO SET AN OFFSET FOR EVERY BAR LOCATION
# LOCATIONS ARE -2W,-W,0,W WITH RESPECT TO EDGE OF BAR
plotNAsales=ax.bar(locationslistnpy-width*2,NAsaleslist,width,label='NA sales',align='edge')
plotEUsales=ax.bar(locationslistnpy-width,EUsaleslist,width,label='EU sales',align='edge')
plotJPsales=ax.bar(locationslistnpy,JPsaleslist,width,label='JP sales',align='edge')
plotOthersales=ax.bar(locationslistnpy+width,Othersaleslist,width,label='Other sales',align='edge')

ax.set_xticks(locationslist,genrelist)

ax.bar_label(plotNAsales,rotation=90,padding=5)
ax.bar_label(plotEUsales,rotation=90,padding=5)
ax.bar_label(plotJPsales,rotation=90,padding=5)
ax.bar_label(plotOthersales,rotation=90,padding=5)

matplotlib.pyplot.title('10. Sales comparison by genre')
matplotlib.pyplot.ylabel('Sales (in millions)\nOrdered by Global sales')
matplotlib.pyplot.xlabel('Genre')

seaborn.despine()

axis=matplotlib.pyplot.gca()
axis.yaxis.grid(linestyle='--')
axis.set_axisbelow(True)

ax.legend()

fig.tight_layout()

matplotlib.pyplot.savefig('10. Sales comparison by genre.jpg',dpi=200)

matplotlib.pyplot.show()