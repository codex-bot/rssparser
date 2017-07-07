import feedparser
import requests

import json

rss = 'https://meduza.io/rss/all'
# rss = 'https://www.reddit.com/r/funny.rss'
# rss = 'https://lenta.ru/rss'

def parseRSS(rss_link):
    return feedparser.parse(rss_link)

def main():

    # parse feed
    parsed = parseRSS(rss)

    if not 'title' in parsed['feed']:
        print('not a RSS link')
    else:
        # get title and subtitle
        title = parsed['feed']['title']
        if parsed['feed']['subtitle']:
            title += " – " + parsed['feed']['subtitle']

        # print title for this rss
        print(title)

        # for each item in this feed do something
        for entry in parsed['entries']:
            message = entry['title'] + "\n" + entry['link']

            # print item
            print(message + "\n\n")

if __name__ == "__main__":
    main()
