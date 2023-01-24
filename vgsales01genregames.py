import sqlite3
import seaborn
import matplotlib

genredict=dict() # a dictionary to store id,genre
genrecountdict=dict() # a dictionary to store the genre count
genrecountlist=list() # a list to CONVERT DICT TO LIST AND SORT IT IN DESCENDING ORDER
genrelist=list() # a list to store genre names
countlist=list() # a list to store genre games count

filesqlcon=sqlite3.connect('vgsales-clean.sqlite')
filesql=filesqlcon.cursor()

filetxt=open('1. What genre games have been made the most.txt','w')

# 1. What genre games have been made the most?

# SELECT ONLY THE GENRE TABLE ID AND GENRE
filesql.execute('select id,genre from Genre')
idgenrelist=filesql.fetchall() # a list of tuples of 2 elements

# CREATE A GENRE DICT
for genreid,genre in idgenrelist:
   genredict[genreid]=genre # key = id, value = genre name

# SELECT ONLY THE GENRE_ID COLUMN FROM GAME TABLE
filesql.execute('select genre_id from Game')
gamegenrelist=filesql.fetchall() # a list of tuples of 2 elements, only the first one will have a value. The 2nd is empty. (value,)

# COUNT GAMES PER GENRE. STORE IN DICT genrecountdict
for genreid in gamegenrelist: # genreid[0] is going to be an INTEGER
   genrecountdict[genreid[0]]=genrecountdict.get(genreid[0],0)+1 # just grab the 1st element of tuple genreid

# CREATE LIST AND INVERT ORDER
for genreid,count in genrecountdict.items():
   genrecountlist.append((count,genreid))

# SORT LIST BY COUNT IN DESCENDING ORDER
genrecountlist=sorted(genrecountlist,reverse=True) # this will order by count

# PRINT NUMBER OF GAMES PER GENRE AND WRITE IT INTO A TXT FILE
print('\nWhat genre games have been made the most?\n\nGenre Game_count\n')
filetxt.write('What genre games have been made the most?\n\nGenre Game_count\n\n')

countmax=0
genremax=''
for count,genreid in genrecountlist:
   genrename=genredict[genreid]
   wordprint=genrename+': '+str(count)
   print(wordprint)
   wordprint=wordprint+'\n'
   filetxt.write(wordprint)

   # CREATE 2 LISTS WITH GENRE AND GAME COUNT FOR PLOTTING

   genrelist.append(genrename)
   countlist.append(count)

   # MAX GENRE COUNT

   if count>=countmax:
      countmax=count
      genremax=genrename+' '+genremax

wordprint='\n'+genremax+'is/are the genre(s) with most games.'
print(wordprint)
filetxt.write(wordprint)

# PLOT WITH SEABORN (MATPLOTLIB)

matplotlib.pyplot.figure(figsize=(7,5)) # width,height in inches

plot=seaborn.barplot(x=genrelist,y=countlist) # create barplot object

plot.bar_label(plot.containers[0]) # put labels on bars

matplotlib.pyplot.title('1. What genre games have been made the most')
matplotlib.pyplot.xlabel('Genre') # name axes
matplotlib.pyplot.ylabel('Game count')

seaborn.despine() # remove top and right lines

axisgca=matplotlib.pyplot.gca() # show y grid
axisgca.yaxis.grid(linestyle='--')
axisgca.set_axisbelow(True)

matplotlib.pyplot.savefig('1. What genre games have been made the most.jpg',dpi=200)

matplotlib.pyplot.show()