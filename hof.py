import sys
import csv
from time import time

import requests
import urllib.request
from bs4 import BeautifulSoup as bsoup

homepage="https://webbook.nist.gov"
prefix="https://webbook.nist.gov/cgi/cbook.cgi?Name="
suffix="&Units=SI&cTG=on"

def get_data(filename):
  lines = open(sys.argv[1], 'r').readlines()

  names = []
  inchis = []

  for line in lines:
    names.append(line)

  return names

def merge_dicts(dict1, dict2):
  return(dict2.update(dict1))


if __name__ == "__main__":
  
  filename = sys.argv[1]

  inchis = get_data(filename)
  mols = []

  start = time()

  hof_data = {}

  for i, mol in enumerate(inchis):
    quote_page = prefix + mol[:-1] + suffix
    page = urllib.request.urlopen(quote_page)
    soup = bsoup(page, 'html.parser')

    lis = soup.find_all("li")
    for li in lis:
        if not li.find('strong', text="IUPAC Standard InChI:"):
            continue
        else:
            fucking_inchi = li.select_one('span').text
    try:
      # find first table
      table = soup.find('table', attrs={'class' : 'data'})
    
      # find all rows in table
      rows = table.find_all("tr")
    
      for j,row in enumerate(rows):
    
        # ignore headers
        if row.find("th"): continue
    
        # isolate hof
        try:
          name = row.find("td")
        except: continue
    
        # filter by name
        try:
          if not "f" in name.find_all('sub',text=True)[0]: continue
        except: continue
    
        # save to dict
        key = inchis[i] + "_" + str(j)
        hof_data[key] = [ str(row.find_all('td')[0].text), str(row.find_all('td')[1].text[:6]), row.find_all('td')[2].text, row.find_all('td')[3].text, row.find_all('td')[4].text, fucking_inchi ]
        print(inchis[i][:-1], hof_data[key])

    except: #continue

      for a in soup.find_all('a', href=True):
        if "ID" in a['href']: mols.append(a['href'])
    
      for i, mol in enumerate(mols):
        quote_page = prefix[:-20] + mol + suffix
        page = urllib.request.urlopen(quote_page)
        soup = bsoup(page, 'html.parser')

        lis = soup.find_all("li")
        for li in lis:
            if not li.find('strong', text="IUPAC Standard InChI:"):
                continue
            else:
                fucking_inchi = li.select_one('span').text

    
        try:
          # find first table
          table = soup.find('table', attrs={'class' : 'data'})
      
          # find all rows in table
          rows = table.find_all("tr")
      
          for j,row in enumerate(rows):
      
            # ignore headers
            if row.find("th"): continue
      
            # isolate hof
            try:
              name = row.find("td")
            except: continue
      
            # filter by name
            try:
              if not "f" in name.find_all('sub',text=True)[0]: continue
            except: continue
      
            # save to dict
            key = inchis[i] + "_" + str(j)
            hof_data[key] = [ str(row.find_all('td')[0].text), str(row.find_all('td')[1].text[:6]), row.find_all('td')[2].text, row.find_all('td')[3].text, row.find_all('td')[4].text, fucking_inchi ]
            print(inchis[i][:-1], hof_data[key])
        except: continue

  print(hof_data)

  np.save("all_the_fucking_hofs.npy", hof_data)

  with open('dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in hof_data.items():
        writer.writerow([key, value])
  
  print("total run time: ", total_run_time)
