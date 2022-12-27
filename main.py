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
        if len(td) < 4:
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
        if td[3].div.has_attr('style'):
            op = "(Disowned)"
        else:
            op = td[3].div.a.text

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



def get_url(query):
    fullUrl = "https://e-hentai.org/?"
    cat = 1023
    configs = open('configs.txt', 'r')
    if configs.readline().endswith('1\n'): #Doujinshi
        cat -= 1
    if configs.readline().endswith('1\n'): #Manga
        cat -= 1
    if configs.readline().endswith('1\n'): #Artist CG
        cat -= 1
    if configs.readline().endswith('1\n'): #Game CG
        cat -= 1
    if configs.readline().endswith('1\n'): #Western
        cat -= 1
    if configs.readline().endswith('1\n'): #Non-H
        cat -= 1
    if configs.readline().endswith('1\n'): #Image Set
        cat -= 1
    if configs.readline().endswith('1\n'): #Cosplay
        cat -= 1
    if configs.readline().endswith('1\n'): #Asian Porn
        cat -= 1
    if configs.readline().endswith('1\n'): #Misc
        cat -= 1
    
    fullUrl += "f_cats=" + str(cat)
    fullUrl += "&f_search=" + query

    return fullUrl


def main():
    fg = FeedGenerator()
    fg.id("https://e-hentai.org/")
    fg.title(sys.argv[1])
    fg.link(href="https://e-hentai.org/", rel="alternate")
    fg.logo("https://e-hentai.org/favicon.ico")
    fg.subtitle(sys.argv[1])
    fg.language("en")

    file = open('test-html/test1.html')
    content = file.read()
    soup = BeautifulSoup(content,'html5lib')
    
    url = get_url(sys.argv[2])
    print(url)
#    website = requests.get(url)
#    soup = BeautifulSoup(website.content,'html5lib')
    for entry in get_entries(soup):
        fe = fg.add_entry()
        fe.title(entry['title'])
        fe.guid(entry['link'])
        fe.link(href=entry['link'])
        fe.enclosure(url=entry['thumbnail'], type='image/jpeg')
        fe.published(entry['date'] + 'UTC')
        fe.author(name=entry['op'], email=entry['op'])
        
        summary = "<p>" + entry['pages'] + "</p>"
        if not entry['authors'].endswith(": "):
            summary += "<p>" + entry['authors'] + "</p>"
        if not entry['groups'].endswith(": "):
            summary += "<p>" + entry['groups'] + "</p>"
        if not entry['parody'].endswith(": "):
            summary += "<p>" + entry['parody'] + "</p>"
        if not entry['characters'].endswith(": "):
            summary += "<p>" + entry['characters'] + "</p>"
        if not entry['m_tags'].endswith(": "):
            summary += "<p>" + entry['m_tags'] + "</p>"
        if not entry['f_tags'].endswith(": "):
            summary += "<p>" + entry['f_tags'] + "</p>"
        if not entry['other'].endswith(": "):
            summary += "<p>" + entry['other'] + "</p>"

        fe.description(summary)
    fg.rss_file(sys.argv[1] + ".xml")
   
if __name__ == "__main__":
    main()
