from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import requests
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import *

admin.site.register(Categorylist)
admin.site.register(Item)
admin.site.register(Bids)

base_url = 'auction'

def home(request):
    
    """response = requests.get('https://fakestoreapi.com/products')
    for i in range(5, 8):
        
        title = response.json()[i]['title']
        starting_bid = response.json()[i]['price']
        category_name = response.json()[i]['category']
        description = response.json()[i]['description']
        image = response.json()[i]['image']
        
        category = Categorylist.objects.get(name=category_name)
        
        users = User.objects.all()
        for user in users :
            if user.is_authenticated:
                user = request.user
        
        items = Item.objects.get_or_create(user=user, title=title, starting_bid=starting_bid, category=category, description=description, image=image)"""
        

    
        
    items = Item.objects.filter(active=True)
    category_list =  Categorylist.objects.all()
    
    return render(request, f'{base_url}/home.html', {
        'category_list': category_list,
    })
    
def items(request, category):
    if category == "all":
        items = Item.objects.filter(active=True)
    else :
        cat = Categorylist.objects.get(name=category)
        items = Item.objects.filter(category=cat, active=True)
        
    category_list =  Categorylist.objects.all()
    
    paginator = Paginator(items, 6)  
    page_number = request.GET.get('page')
    page_items = paginator.get_page(page_number)

    return render(request, f'{base_url}/items.html', {
        'items': items,
        'category_list': category_list,
        'page_items': page_items,
        })

def item_page(request, item_title):
    if request.method == 'GET':
        item = Item.objects.get(title=item_title, active=True)
        
        category_list =  Categorylist.objects.all()
        
        largest_bid = Bids.objects.order_by('bid').filter(item=item).last()
        if largest_bid:
            min_bid = max(largest_bid.bid, item.starting_bid)
        else:
            min_bid = item.starting_bid
        
        return render(request, f'{base_url}/item-page.html', {
            'item': item,
            'category_list': category_list,
            'bid': largest_bid,
            'min_bid': min_bid,
        })
    
    elif request.method == 'POST':
        bid = request.POST['Bid']
        
        item = Item.objects.get(title=item_title, active=True)
        
        users = User.objects.all()
        for user in users :
            if user.is_authenticated:
                user = request.user
                
        b = Bids.objects.create(user=user, item=item, bid=bid)
        
        return HttpResponseRedirect(reverse("itempage", args=(item_title,)))
    
@login_required
def end_auction(request, item_title):
    if request.method == 'POST':
        item = get_object_or_404(Item, title=item_title, user=request.user)
        item.active = False
        item.save()
        
        return HttpResponseRedirect(reverse("items", args=('all',)))
    
def login_page(request):
    category_list =  Categorylist.objects.all()
    
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        
        user = authenticate(request, username=username, password=password)
        
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auction_home"))
            
        else:
            return render(request, f'{base_url}/login.html', {
                'category_list': category_list,
            })
        
    else:
        return render(request, f'{base_url}/login.html', {
            'category_list': category_list,
        })

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

@login_required
def user_items(request):
    
    users = User.objects.all()
    for user in users :
        if user.is_authenticated:
            user = request.user
    
    items = Item.objects.filter(user=user)
    
    category_list =  Categorylist.objects.all()

    return render(request, f'{base_url}/user-items.html', {
        'items': items,
        'category_list': category_list,
        })

def signup_view(request):
    
    category_list =  Categorylist.objects.all()
    
    if request.method == 'POST':
        username = request.POST['Username']
        email = request.POST['Email']
        password = request.POST['Password']
        password2 = request.POST['Password2']
        fname = request.POST['Firstname']
        lname = request.POST['Lastname']
        

        if password == password2:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = fname
            user.last_name = lname
            user.save()
        else: 
            messages.error(request, 'Passwords Do Not Match')
            return HttpResponseRedirect('signup')
            
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auction_home"))
        else:
            return render(request, f'{base_url}/signup.html')
    
    else:
        return render(request, f'{base_url}/signup.html',{
            'category_list': category_list,
        })
    
def post_item(request):
    if request.method == 'POST':
        title = request.POST['Title']
        starting_bid = request.POST['Starting-Bid']
        category_name = request.POST['Category']
        description = request.POST['Description']
        image = request.POST['Image-URL']
        
        category = Categorylist.objects.get(name=category_name)
        
        users = User.objects.all()
        for user in users :
            if user.is_authenticated:
                user = request.user
    
        item = Item.objects.create(user=user, title=title, starting_bid=starting_bid, category=category, description=description, image=image)
        
        return HttpResponseRedirect(reverse("auction_home"))
        
    elif request.method == 'GET':
        
        category_list = Categorylist.objects.all()
        
        return render(request, f'{base_url}/post-item.html', {
            'category_list': category_list,
        })
        
def api_item(request):
    if request.method == 'GET':
        
        category_list =  Categorylist.objects.all()
        
        api_item_list = requests.get('https://fakestoreapi.com/products?limit=30').json()
        
        paginator = Paginator(api_item_list, 6)  
        page_number = request.GET.get('page')
        page_items = paginator.get_page(page_number)
        
        return render(request, f'{base_url}/apiitems.html', {
            'category_list': category_list,
            'items' : api_item_list,
            'page_items': page_items,
        })
        
    elif request.method == 'POST':
        
        title = request.POST['title']
        starting_bid = request.POST['price']
        description = request.POST['description']
        category = Categorylist.objects.get_or_create(name=request.POST['category'])
        category = Categorylist.objects.get(name=request.POST['category'])
        image = request.POST['image']
        
        users = User.objects.all()
        for user in users :
            if user.is_authenticated:
                user = request.user
                
        item = Item.objects.create(user=user , title=title, starting_bid=starting_bid, description=description, category=category, image=image)
        item.save()
        
        return HttpResponseRedirect(reverse("items", args=('all',)))

def about_page(request):
    
    category_list =  Categorylist.objects.all()
    
    return render(request, f'{base_url}/about.html',{
        'category_list': category_list,
    })
