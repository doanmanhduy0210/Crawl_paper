from bs4 import BeautifulSoup
import requests
import argparse
import os
import sys


def CreateURl(Conference="", Keywork="", Year=None):
    urlparser_first = 'https://arxiv.org/search/?query='
    urlparser_last = '&searchtype=all&source=header'
    if Year is not None:
        Year = str(Year)
    else:
        Year = ""
    Conference = Conference.strip()
    Keywork = Keywork.strip()
    Year = Year.strip()
    conference = Conference.replace(" ", "+")
    new_keywork = Keywork.replace(" ", "+")
    year = Year
    url_ = urlparser_first + "+" + new_keywork + "+" + conference + "+" + year + "+" + urlparser_last
    if Conference + Keywork + Year == "":
        return None
    else:
        return url_


def CrawlPaper(num_of_paper=None, url=None):

    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'lxml')
    except OSError:
        print('cannot open your requests URL, maybe something wrong. Please check again !')
        return
    all_paper = soup.find_all("li", {"class": "arxiv-result"})
    if len(all_paper) is 0:
        print("Sorry!. Your query has no results.")
        return
    maxsize = len(all_paper)
    if num_of_paper != None:
        maxsize = min(int(num_of_paper),maxsize)
    # print("number of paper need search {} and size of list paper {}".format(num_of_paper, len(all_paper)))

    for index, paper in enumerate(all_paper):
        if index >= maxsize:
            return
        print("{} Title: {}".format(index + 1,
                                    paper.find('p', {"class": "title is-5 mathjax"}).text.replace("\n", "").strip()))
        print(paper.find('p', {"class": "authors"}).text.replace("\n", ""))
        print(paper.find('p', {"class": "abstract mathjax"}).text.replace("\n", ""))
        for link in paper.find_all("a"):
            if link.get('href'):
                if link['href'].split('/')[-2] == 'pdf':
                    print("link paper: {} ".format(link['href']))
                if link['href'].split("/")[-2] == 'format':
                    print("link Summary paper: {}".format(link['href']))
        print("======================================================================================")


def _main_(args):
    keyword_search = args.keyword
    conference_search = args.conference
    year_search = args.year
    num_of_paper = args.number_of_paper
    url_origin = CreateURl(Conference=conference_search, Keywork=keyword_search, Year=year_search)
    CrawlPaper(num_of_paper=num_of_paper, url=url_origin)



if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='test crawl paper')

    argparser.add_argument(
        '-k',
        '--keyword',
        default="",
        help='pass keyword')

    argparser.add_argument(
        '-c',
        '--conference',
        default="",
        help='pass conference need search')

    argparser.add_argument(
        '-n',
        '--number_of_paper',
        default=None,
        help='number of paper need search')

    argparser.add_argument(
        '-y',
        '--year',
        default=None,
        help='pass year need search')

    args = argparser.parse_args()
    _main_(args)