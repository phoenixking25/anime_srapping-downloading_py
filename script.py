from bs4 import BeautifulSoup
import requests
import click
import re


urls = [
    'http://crusader.pp.ua/anime/',
    'http://booksaz.space/s1/Anime/',
    'https://archives.eyrie.org/anime/',
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
    print dir_link
    download_link = []
    for i in dir_link:
        r = requests.get(i)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        list = soup.findAll('a', href=re.compile('.mkv'))
        if len(list):
            for j in list:
                download_link.append(i + j.get('href'))
    print download_link


if __name__ == '__main__':
    animename(obj={})







