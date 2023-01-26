import matplotlib
import seaborn
import sqlite3

idyeardict=dict() # A DICTIONARY TO STORE YEARID AND YEAR
idgenredict=dict() # A DICTIONARY TO STORE GENREID AND GENRE
yearidgenresdict=dict() # a nested dict, to store year id and a dictionary with the genre and count.{yearid:{genreid:count}}
yearmaxgenrelist=list() # a list to store a tuple of year,maxgenre and count, and sort it by year
yearlist=list() # a list to store years
genrelist=list() # a list to store max genres
countlist=list() # a list to store max counts
labelsformat=list() # a list to store the edited labels

filesqlcon=sqlite3.connect('vgsales-clean.sqlite')
filesql=filesqlcon.cursor()

filetxt=open('5. Which genre game has been released the most in a single year.txt','w')

# RETRIEVE YEARID AND GENREID FROM TABLE GAME
filesql.execute('select year_id,genre_id from Game')
yearidgenreidlist=filesql.fetchall()

# RETRIEVE YEAR ID AND YEAR FROM TABLE YEAR
filesql.execute('select id,year from Year')
idyearlist=filesql.fetchall()

# RETRIEVE GENRE ID AND GENRE FROM TABLE GENRE
filesql.execute('select id,genre from Genre')
idgenrelist=filesql.fetchall()

# CREATE A DICTIONARY TO STORE YEARID AND YEAR
for id,year in idyearlist:
   idyeardict[id]=year

# CREATE A DICTIONARY TO STORE GENREID AND GENRE
for id,genre in idgenrelist:
   idgenredict[id]=genre

# CREATE A NESTED DICT TO STORE THE COUNT FOR EACH GENRE IN EVERY YEAR.
for yearid,genreid in yearidgenreidlist: # yearidgenresdict is a nested dict {yearid:{genreid:count}}
   yearidgenresdict[yearid]=yearidgenresdict.get(yearid,{}) # first you have to create the dictionary key yearid if it doesn't exist. otherwise it can't access [genreid]
   yearidgenresdict[yearid][genreid]=yearidgenresdict.get(yearid,{}).get(genreid,0)+1 # yearidgenresdict.get(yearid,{}) returns a dictionary

# SEARCH FOR THE MAX COUNT OF A GENRE, FOR EACH YEARID
for yearid,genres in yearidgenresdict.items(): # yearid is an int, genres is a dictionary
   maxcount=None
   for genreid in genres:
      count=genres[genreid]
      if maxcount is None:
         maxcount=count
         maxgenreid=genreid # idgenredict[genreid] is the genre name
      if count>maxcount:
         maxcount=count
         maxgenreid=genreid

   maxgenre=idgenredict[maxgenreid] # store the name of the max genre retrieving the name from idgenredict

   # LOOP AGAIN OVER THE GENRES TO SEE IF THERE WERE 2 OR MORE MAXIMUMS OF THE SAME COUNT
   for genreid in genres:
      if genres[genreid]==maxcount and genreid!=maxgenreid: maxgenre=maxgenre+' / '+idgenredict[genreid]

   yearmaxgenrelist.append((str(idyeardict[yearid]),maxgenre,maxcount)) # append a 3-element tuple

yearmaxgenrelist=sorted(yearmaxgenrelist)

filetxt.write('5. Which genre game has been released the most in a single year\n\nYear Max_genre Game_count\n\n')
print('\n5. Which genre game has been released the most in a single year\n\nYear Max_genre Game_count\n')

# CREATE 3 INDEPENDENT LISTS FOR yearstr,genre(s),count
for yearstr,genre,count in yearmaxgenrelist:
   yearlist.append(yearstr)
   genrelist.append(genre)
   countlist.append(count)
   wordprint=yearstr+' '+genre+' '+str(count)
   print(wordprint)
   wordprint=wordprint+'\n'
   filetxt.write(wordprint)

# PLOT WITH MATPLOTLIB

matplotlib.pyplot.figure(figsize=(13,6))

plot=seaborn.barplot(y=yearlist,x=countlist,width=0.4,orient='h') # plot horizontally, x horizontal, y vertical. width of bars 0.4.

# FORMAT THE BARS LABELS
for yearstr,genre,count in yearmaxgenrelist:
   labelsformat.append(genre+' - '+str(count))

plot.bar_label(plot.containers[0],rotation=0,labels=labelsformat,padding=7) # rotation 0 for the labels to be horizontal

matplotlib.pyplot.xticks(rotation=-90) # rotation -90 to put the values vertically and reading them from top to bottom

matplotlib.pyplot.title('5. Which genre game has been released the most in a single year',loc='left')
matplotlib.pyplot.ylabel('Year')
matplotlib.pyplot.xlabel('Max game count (and genre)')

seaborn.despine()

axisgca=matplotlib.pyplot.gca() # show x grid instead of y
axisgca.xaxis.grid(linestyle='--')
axisgca.set_axisbelow(True)

matplotlib.pyplot.savefig('5. Which genre game has been released the most in a single year.jpg',dpi=200)

matplotlib.pyplot.show()