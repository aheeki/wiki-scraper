from bs4 import BeautifulSoup
import urllib2

wiki = "http://en.wikipedia.org/wiki/List_of_Metropolitan_Statistical_Areas"
header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
req = urllib2.Request(wiki,headers=header)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page)
 
rank = ""
metroarea = ""
est2013 = ""
census2010 = ""
change = ""
statarea = ""
table = soup.find("table", { "class" : "wikitable sortable" })

f = open('output.dat', 'w')

counter = 0
for row in table.findAll("tr"):
    print(counter)
    counter += 1
    cells = row.findAll("td")
    if len(cells) > 0:
        metroarea = cells[1].find(text=True)
        est2013 = cells[2].find(text=True)
        census2010 = cells[3].find(text=True)
        # use findAll bc there are multiple text fields within the td
        change = cells[4].findAll(text=True)[1]
        statarea = cells[5].find(text=True)
        # make sure statarea isn't blank
        if statarea is None:
            statarea = "none"
    
        write_to_file = metroarea + "::" + est2013 + "::" + census2010 + "::" +change + "::" + statarea + "\n"
        write_to_file = write_to_file.encode('utf-8')
#         print write_to_file
        f.write(write_to_file)
  
  f.close()
  
  import pandas as pd

headnames = ['metroarea', 'est2013', 'census2010', 'change', 'statarea']
population = pd.read_table('output.dat',
                      sep='::', header=None, names=headnames, engine='python')
print(population)

population.describe()
