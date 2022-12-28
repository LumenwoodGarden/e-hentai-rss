from bs4 import BeautifulSoup
import requests
import sys

from feedgen.feed import FeedGenerator

def get_entries(soup):
    tr = soup.find('table', {'class': 'itg gltc'}).findAll('tr') 
    entries = []
    for x in range(1, len(tr)):
        #print(tr[x].prettify())
        td = tr[x].findAll('td')
        if len(td) < 4:         #filter out the header and ads
            continue

        td1div = td[1].findAll('div')
        thumbnail = td1div[2].img.get('src')
        if td1div[2].img.has_attr('data-src'):
            thumbnail = td1div[2].img.get('data-src')
        media = td1div[5].text
        date = td1div[6].text
        pages = td1div[9].text
        
        link = td[2].find('a').get('href')
        title = td[2].find('div', {'class': 'glink'}).text
        language = "language: "
        authors = "authors: "
        groups = "groups: "
        parody = "parody: "
        characters = "characters: "
        m_tags = "male: "
        f_tags = "female: "
        other = "other: "

        for t in td[2].findAll('div', {'class': 'gt'}):
            if t.get('title').startswith("language"):
                language += t.text + ", "
            elif t.get('title').startswith("artist"):
                authors += t.text + ", "
            elif t.get('title').startswith("group"):
                groups += t.text + ", "
            elif t.get('title').startswith("parody"):
                parody += t.text + ", "
            elif t.get('title').startswith("character"):
                characters += t.text + ", "
            elif t.get('title').startswith("male"):
                m_tags += t.text[2:] + ", "
            elif t.get('title').startswith("female"):
                f_tags += t.text[2:] + ", "
            else:
                other += t.text + ", "

        op = ""
        if not td[3].div.has_attr('style'):
            op = td[3].div.a.text
        else:
            op = td[3].div.text

        entries.append(
            {
                "thumbnail": thumbnail,
                "date": date,
                "link": link,
                "title": title,
                "language": language,
                "authors": authors,
                "groups": groups,
                "parody": parody,
                "characters": characters,
                "m_tags": m_tags,
                "f_tags": f_tags,
                "other": other,
                "pages": pages,
                "op": op
            }
        )
    return entries



def get_url(query, confFile):
    fullUrl = "https://e-hentai.org/?"
    
    cat = 1023
    configs = open(confFile, 'r')

    # [ Doujinshi,  Manga,      Artist CG,  Game CG,    Western, 
    #   Non-H,      Image Set,  Cosplay,    Asian Porn, Misc    ]
    categories = [2, 4, 8, 16, 512, 256, 32, 64, 128, 1]

    for x in categories:
        cat -= x * int(configs.readline()[-2])
       
    ratConf = configs.readline()
    minRat = ratConf[-2]

    fullUrl += "f_cats=" + str(cat)
    fullUrl += "&f_search=" + query
    fullUrl += "&f_srdd=" + minRat

    return fullUrl


def main():
    feed = []
    feedFile = open("feeds.txt")
    line = feedFile.readline()
    while line:
        currFeed = line[:-1].split(";")
        if currFeed[0] == sys.argv[1]:
            feed = currFeed
            break
        line = feedFile.readline()

    if len(feed) == 0:
        sys.exit("couldn't find a matching feed in feeds.txt")

    fg = FeedGenerator()
    fg.id("https://e-hentai.org/")
    fg.title(feed[0])
    fg.link(href="https://e-hentai.org/", rel="alternate")
    fg.logo("https://e-hentai.org/favicon.ico")
    fg.subtitle(feed[0])
    fg.language("en")

#    testFile = open('test-html/test3.html')
#    content = testFile.read()
#    soup = BeautifulSoup(content,'html5lib')
    
    url = get_url(feed[1], (feed[2], "configs.txt") [len(feed)<3 or len(feed[2])==0])
#    print(feed)
    print(url)
    website = requests.get(url)
    soup = BeautifulSoup(website.content,'html5lib')
    for entry in get_entries(soup):
        fe = fg.add_entry()
        fe.title(entry['title'])
        fe.guid(entry['link'])
        fe.link(href=entry['link'])
        fe.enclosure(url=entry['thumbnail'], type='image/jpeg')
        fe.published(entry['date'] + 'UTC')
        fe.author(name=entry['op'], email=entry['op'])
        
        summary = "<p>" + entry['pages'] + "</p>"
        tagArray = ['language', 'authors', 'groups', 'parody', 'characters', 'm_tags', 'f_tags', 'other']
        for tagName in tagArray:
            if not entry[tagName].endswith(": "):
                summary += "<p>" + entry[tagName][0:-2] + "</p>"

        fe.description(summary)
    outputFile = (feed[3], feed[0] + ".xml") [len(feed)<4 or len(feed[3])==0]
    fg.rss_file(outputFile)
   
if __name__ == "__main__":
    main()
