import pandas as pd
from bs4 import BeautifulSoup
import urllib2

wiki = "http://en.wikipedia.org/wiki/List_of_Metropolitan_Statistical_Areas" #page containing the table

header = {'User-Agent': 'Mozilla/5.0'} #needed to prevent 403 error on Wikipedia
req = urllib2.Request(wiki,headers=header)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page)

#column headers
rank = ""
metroarea = ""
est2013 = ""
census2010 = ""
change = ""
statarea = ""

table = soup.find("table", { "class" : "wikitable sortable" })

f = open('output.dat', 'w')

for row in table.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) > 0:
        metroarea = cells[1].find(text=True)
        est2013 = cells[2].find(text=True)
        census2010 = cells[3].find(text=True)
        # use findAll bc of multiple text fields within the td
        change = cells[4].findAll(text=True)[1]
        statarea = cells[5].find(text=True)
        # make sure statarea isn't blank
        if statarea is None:
            statarea = "none"

        write_to_file = metroarea + "::" + est2013 + "::" + census2010 + "::" +change + "::" + statarea + "\n"
        write_to_file = write_to_file.encode('utf-8')

        f.write(write_to_file)

f.close()

headnames = ['metroarea', 'est2013', 'census2010', 'change', 'statarea']
population = pd.read_table('output.dat',
                      sep='::', header=None, names=headnames, engine='python')
print(population)
print(population.describe())
