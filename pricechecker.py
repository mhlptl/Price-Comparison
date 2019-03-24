from bs4 import BeautifulSoup
import urllib.request
import csv
from datetime import datetime
from operator import itemgetter

date = datetime.now()
date = f'{date.month}/{date.day}/{date.year}'
linksL = []
lowered = []

# Compare
def compare():
    for i in range(len(linksL)-1):
        if linksL[i-1][0] == linksL[i-2][0] and linksL[i][0] != linksL[i-1][0]:
            if(linksL[i-1][1] < linksL[i-2][1]):
                lowered.append(f'{linksL[i-1][0]} is lowered.')
    
    with open('results.txt', 'w') as outfile:
        outfile.writelines(lowered)

# Sort List
def sortList():
    with open('price.csv', 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            linksL.append(row)
    linksL.sort(key=itemgetter(0))
    with open('price.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(linksL)
    # print(*linksL, sep='\n')

# Store data in csv file
def store(lists):
    with open('price.csv', 'a+', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(lists)

# Get name and price from url
def contents(link):
    url = urllib.request.urlopen(link)
    soup = BeautifulSoup(url, 'html.parser')
    desc = soup.find('meta', property={'og:description'}).get('content').split(':')
    name = desc[1].replace(', Category', '')
    price = desc[-1]
    linksL.append([name, price, date])

# Add link to list
def main():
    filename = 'links.txt'
    with open(filename, 'r') as lines:
        for line in lines:
            contents(line)
    store(linksL)
    linksL.clear()
    sortList()
    for i in linksL:
        i[1] = float(i[1])
    compare()

if __name__ == "__main__":
    main()

# Text File -> List -> Open Link -> Get Name and Price -> CSV File