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
    BASE_IMAGE_URL = "https://images.craigslist.org/.jpg{}_300*300.jpg"
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_="result-price"):
            post_price = post.find(class_='result-price').text
        else: post_price = "N/A"
    
    if post.find(class_='result-image').get('data-ids'):
        post_image_id = post.find(class_='result-image').get('data-ids')[0].split(',')[0].split[':'][1]
        post_image_url = BASE_IMAGE_URL.format(post_image_id)
    else:
        post_image_url = 'https://craigslist.org/images/peace.org'

    final_postings.append((post_title, post_url, post_price, post_image_url))

   
    stuff_for_frontend = {
        'search':search,
        'final_postings': final_postings,
        }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
