from bs4 import BeautifulSoup
import requests
import click
import re
import sys
from clint.textui import progress


urls = [
    'http://crusader.pp.ua/anime/',
    'http://booksaz.space/s1/Anime/',
    'http://booksaz.space/s1/Anime/Ended/',
    'http://booksaz.space/s1/Anime/OVA/',
    'http://booksaz.space/s1/Anime/2017/',
    'http://booksaz.space/s1/Anime/2015/',
    'http://booksaz.space/s1/Anime/2016/',
    'http://chise.ludost.net/Anime/'
]

@click.command(help = "It checks the given anime can be downloaded if it is, It download that :)")
@click.option('-url', type = click.Path(), help = "Url on which anime is present", default = '')
@click.argument('name_of_anime', type = click.Path())
@click.pass_context


def animename(ctx, name_of_anime, url):
    dir_link = []
    print "Finding you anime"
    for i in urls:
        r  = requests.get(i)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        list = soup.findAll('a', href=re.compile(name_of_anime))
        if len(list):
            for j in list:
                dir_link.append(i + j.get('href'))
    if(len(dir_link)):
        opendir(dir_link)
    else:
        print 'You anime not found'

def opendir(dir_link):
    download_link = []
    for i in dir_link:
        r = requests.get(i)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        list = soup.findAll('a', href=re.compile('.mkv'))
        if len(list):
            for j in list:
                download_link.append(i + j.get('href'))
    print "There are total %r files to be downloaded" % len(download_link)

    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}

    choice = raw_input('Do you want to continue?(y/n) ').lower()
    if choice in yes:
        downloadfiles(download_link)
    elif choice in no:
        print "Sayonara"
    else:
        sys.stdout.write("Please respond with 'yes' or 'no'")


def downloadfiles(download_link):
    j = 1
    for i in download_link:
        print 'Downloading %r file' % j
        r = requests.get(i, stream=True)
        path = 'anime.mkv'
        with open(path, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
        print '%r file downloaded' % j
        j += 1


if __name__ == '__main__':
    animename(obj={})







