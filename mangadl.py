import sqlite3, requests, bs4, os


title = input('Name of manga: ').replace(' ', '_').lower()
chaprange = input('From chapter-To chapter: ')
frm, t = chaprange.split('-')
frm, t = int(frm), int(t)
url = 'https://mangakakalot.com/manga/' + title
source = requests.get(url).content
soup = bs4.BeautifulSoup(source, 'html.parser')
a = soup.find_all('a', href=True)
chapter_list = []
for href in a:
    if url.replace('/manga/', '/chapter/') in href['href']:
        chapter_list.append(href['href'])
chapter_list.reverse()
i = frm
while i <= t:
    chapter = chapter_list[i]
    os.mkdir('chapter{}'.format(str(i)))
    csource = requests.get(chapter).content
    csoup = bs4.BeautifulSoup(csource, 'html.parser')
    imgs = csoup.find_all('img', src=True)
    for l in range(len(imgs)):
        img = imgs[l]
        if '/mangakakalot/' in img['src']:
            with open('page{}.jpg'.format(l), 'rb') as f:
                f.write(requests.get(img['src']).content)
    i += 1
