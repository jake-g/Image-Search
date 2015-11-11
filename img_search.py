import urllib2
from cookielib import CookieJar
import re
import time


start = time.time()     # Debug Timer

cookies = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 '
                                    '(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]


def image_lookup(path):
    google_path = 'http://google.com/searchbyimage?image_url=' + path
    source = opener.open(google_path).read()
    # print(source) # Debug regex
    links = re.findall(r'"ou":"(.*?)","ow"', source)   # TODO is this robust?
    return links


def image_scrape(links):
    for link in links:
        # print link    # Debug
        filename = link.split('/')[-1].split('.')[0]
        ext = '.' + link.split('.')[-1]

        try:    # Try to Download Image
            img = urllib2.urlopen(link)
        except urllib2.URLError, err:   # TODO Why are some links "Bad Request"
            print err.read() + link

        # Save Image
        with open(filename + ext, 'wb') as local_file:
            local_file.write(img.read())
            print "Saved: " + filename


def main():
    url = raw_input("Image URL: ")  # TODO add valid url check
    links = image_lookup(url)   # search for similar
    image_scrape(links)         # save results

    end = time.time()   # Debug runtime
    print "Search Time: " + str(end - start) + ' seconds'

main()
