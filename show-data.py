import csv

with open('firstscrapy/tripRestaurants.csv') as f:
    for date, text, title in csv.reader(f):
        text = text.replace('\n', '')
        print(f'{date:20.20} {title:40.40} {text:80.80}')
