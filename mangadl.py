import requests, bs4, os, ui


def get_manga(title, frm, t):
    if not os.path.exists(title):
        os.mkdir(title)
    os.chdir(title)
    search_url = 'https://mangakakalot.com/search/' + title
    search_source = requests.get(search_url).content
    search_soup = bs4.BeautifulSoup(search_source, 'html.parser')
    results = search_soup.find_all('div')
    url = [result.a['href'] for result in results if result.has_attr('class') and 'story_item' in result['class']][0]
    #url = 'https://mangakakalot.com/manga/' + title
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
        os.chdir('chapter{}'.format(str(i)))
        csource = requests.get(chapter).content
        csoup = bs4.BeautifulSoup(csource, 'html.parser')
        imgs = csoup.find_all('img', src=True)
        for l in range(len(imgs)):
            img = imgs[l]
            if '/mangakakalot/' in img['src']:
                with open('page{}.jpg'.format(l), 'wb') as f:
                    f.write(requests.get(img['src']).content)
        i += 1
