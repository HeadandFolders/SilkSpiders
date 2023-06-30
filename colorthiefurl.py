import sys
import pandas as pd


df = pd.read_csv('C:/Users/ItsJa/spiders/ResultsLeftiesWRowData.csv')
print(df['link'])
if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen, Request

import io
from colorthief import ColorThief
colors_list = []
#df['link'] = df.apply(color)

#urls = ['https://th.bing.com/th/id/OIP.1pNvbuhq-Qn7BLHlNjrsZAHaJv?pid=ImgDet&rs=1','https://static.lefties.com/9/photos2/2023/I/0/1/p/1033/301/800/1033301800_1_1_3.jpg?t=1686399641068']



for url in df.loc[[30,50,60,67,55,60],'link']:  #works (20 and 23 not included i think)#for url in df['link']:
#for url in df['link']:
    req = Request(url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"})
    try:
        if url!="null":
            fd = urlopen(req)
            f = io.BytesIO(fd.read())
            color_thief = ColorThief(f)
           #print(color_thief.get_color(quality=7))
            color = color_thief.get_palette(5, quality=7)[2]
            print(color)
            colors_list.append(color)
        else:
            colors_list.append(1000,1000,1000)
    except:
        print("An exception occured; (266,266,266)")
        color = (1000,1000,1000)
        colors_list.append(color)
     
#df['color_extracted']= colors_list
#df.to_csv('C:/Users/ItsJa/spiders/ResultsLeftiesWithColor.csv')
with open('ColorsLefties.txt', 'w') as outfile:
    outfile.write('\n'.join(str(i) for i in colors_list))
     
    print("File written successfully")
 
 
# close the file
#outfile.close()    
#print("Data appended successfully.")



from math import sqrt

def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in colors_list:
        cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]
a = input("please enter r,g,b: ")
a = tuple(int(x) for x in a.split(","))

row_number = colors_list.index(closest_color(a))
print(closest_color(a))
print("index of the closest color is: ", row_number)
linkk = df.iloc[row_number]['link']
print(linkk)

from selenium import webdriver
import time
#browser exposes an executable file
#Through Selenium test we will invoke the executable file which will then #invoke actual browser
driver = webdriver.Edge()
# to maximize the browser window
#driver.maximize_window()
#get method to launch the URL
driver.get(linkk)
time.sleep(60)

