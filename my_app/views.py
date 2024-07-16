from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_URL =  'https://losangeles.craigslist.org/search/?query={}'

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('a', {'class': 'result_title'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_price = post.find(class_='result-price').text
    
    final_postings.append((post_title, post_url, post_price))


    stuff_for_frontend = {
        'search':search,
        }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
