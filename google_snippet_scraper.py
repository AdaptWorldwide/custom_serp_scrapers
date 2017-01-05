import requests
from bs4 import BeautifulSoup
from random import choice
from random import randint
from time import sleep

keyword_list = []
failed_keywords = []

user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36']

base_url = 'https://www.google.co.uk/search?site=&source=hp&q='

def feed_keywords():
    with open('input.txt','r',encoding='utf-8') as input_file:
        for line in input_file:
            line = line.strip()
            keyword_list.append(line)

def random_user_agent():
    UserAgent = choice(user_agent_list)
    UserAgent = {'User-Agent':UserAgent}
    return UserAgent

def make_request(keyword):
    keyword = keyword.replace(' ','+')
    try:
        r = requests.get('{}{}'.format(base_url,keyword), headers=random_user_agent())
        return r
    except:
        failed_keywords.append(keyword)

def parse_snippet(response):
    soup = BeautifulSoup(response.text,'lxml')
    snippet = soup.find('div',attrs={'class':'xpdopen'})
    if snippet != None:
        links = snippet.find_all('a', href=True)
        snippet_link = links[0]['href']
        return snippet_link
    else:
        return None

def parse_results(response):
    urls = []
    soup = BeautifulSoup(response.text,'lxml')
    soup2 = soup.find('div',attrs={'class':'srg'})
    h3s = soup.find_all('h3',attrs={'class':'r'})
    for h3 in h3s:
        result = h3.find('a')
        result = result['href']
        urls.append(result)
    return urls

def output(keyword,snippet,urls):
    if snippet != None:
        with open('Results.csv','a',encoding='utf-8') as output_file:
            output_file.write('"{}","Snippet","{}"\n'.format(keyword,snippet))
    else:
        pass
    if len(urls) > 0:
        r = len(urls)
        i = 0
        while i < r:
            with open('Results.csv','a',encoding='utf-8') as output_file:
                output_file.write('"{}","{}","{}"\n'.format(keyword,i+1,urls[i]))
            i += 1
    else:
        failed_keywords.append(keyword)

def main():
    for keyword in keyword_list:
        r = make_request(keyword)
        link = parse_snippet(r)
        urls = parse_results(r)
        output(keyword,link,urls)
        sleep(randint(30,60))
    for keyword in failed_keywords:
        r = make_request(keyword)
        link = parse_snippet(r)
        urls = parse_results(r)
        output(keyword, link, urls)
        sleep(randint(40,80))

feed_keywords()
main()
