from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as to_login
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from .models import *
from .forms import *
from django.contrib import messages


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return home(request)


def home(request):
    if request.user.is_authenticated:
        return login(request)
    title_str = 'Technology Catalogue'
    show_title_bool = True
    show_search_bar_bool = False
    editing_mode_bool = False
    show_back_bool = False
    show_logo_bool = False
    context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
               'show_back': show_back_bool, 'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool}
    return render(request, 'home/home.html', context)


def login(request):
    if request.user.is_authenticated:
        return index(request)
    title_str = 'Technology Catalogue'
    show_title_bool = False
    show_search_bar_bool = False
    editing_mode_bool = True
    show_back_bool = True
    show_logo_bool = False
    if post := request.POST:
        try:
            # Process the request if posted data are available
            email = request.POST['email']
            password = request.POST['password']
            # Check username and password combination if correct
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Save session as cookie to login the user
                to_login(request, user)
                # Success, now let's login the user.
                show_search_bar_bool = True
                show_back_bool = False
                editing_mode_bool = False
                show_logo_bool = True
                context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
                           'show_back': show_back_bool, 'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool}
                return render(request, 'home/index.html', context)
            else:
                # Incorrect credentials, let's throw an error to the screen.
                context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
                           'show_back': show_back_bool, 'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool,
                           'error_message': 'Incorrect username and / or password.'}
                return render(request, 'home/login.html', context)
        except CatalogueUser.DoesNotExist:
            context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
                       'show_back': show_back_bool, 'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool,
                       'error_message': 'This user is not exist.'}
            return render(request, 'home/login.html', context)
        except ValueError:
            context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
                       'show_back': show_back_bool, 'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool,
                       'error_message': 'Incorrect value type of username and / or password.'}
            return render(request, 'home/login.html', context)
    context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
               'show_back': show_back_bool, 'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool}
    return render(request, 'home/login.html', context)


@login_required()
def index(request):
    title_str = 'Technology Catalogue'
    show_title_bool = False
    show_search_bar_bool = True
    editing_mode_bool = False
    show_back_bool = False
    show_logo_bool = True
    context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
               'show_back': show_back_bool,
               'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool}
    return render(request, 'home/index.html', context)


@login_required()
def items(request):
    labels = request.GET.getlist('label')
    item_list = Item.objects.all()
    if labels:
        item_list = Item.objects.filter(labels__in=labels).distinct()

    title_str = 'Technology Catalogue'
    show_title_bool = False
    show_search_bar_bool = False
    editing_mode_bool = False
    show_back_bool = False
    show_logo_bool = True
    context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
               'show_back': show_back_bool,
               'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool, 'item_list': item_list,
               'last_labels': labels}
    return render(request, 'home/items.html', context)


@login_required()
def details(request, item_id):
    title_str = 'Technology Catalogue'
    show_title_bool = False
    show_search_bar_bool = False
    editing_mode_bool = False
    show_back_bool = False
    show_logo_bool = True
    item_detail = Item.objects.get(pk=item_id)
    seller_mode = False
    if request.user.is_seller:
        seller_mode = True
    context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
               'show_back': show_back_bool,
               'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool, 'item_detail': item_detail,
               'seller_mode': seller_mode}
    return render(request, 'home/detail.html', context)


@login_required()
def search(request):
    title_str = 'Technology Catalogue'
    show_title_bool = False
    show_search_bar_bool = False
    editing_mode_bool = False
    show_back_bool = False
    show_logo_bool = True
    keyword = request.GET.get('keyword')
    item_list = Item.objects.annotate(search=SearchVector('title', 'description'), ).filter(search=keyword)
    context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
               'show_back': show_back_bool,
               'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool, 'item_list': item_list}
    return render(request, 'home/items.html', context)


@login_required()
def selected_items(request):
    labels = request.GET.get('filter')
    item_list = Item.objects.all()
    last_labels = request.GET.get('last_labels')
    last_labels_nums = last_labels[2:-2]
    if len(last_labels_nums) > 0:
        last_labels_nums = list(map(int, last_labels_nums.strip().split('\', \'')))
        item_list = item_list.filter(labels__in=last_labels_nums).distinct()
    if labels:
        item_list = item_list.filter(labels=labels).distinct()

    title_str = 'Technology Catalogue'
    show_title_bool = False
    show_search_bar_bool = False
    editing_mode_bool = False
    show_back_bool = False
    show_logo_bool = True
    context = {'title': title_str, 'show_title': show_title_bool, 'show_search_bar': show_search_bar_bool,
               'show_back': show_back_bool,
               'editing_mode': editing_mode_bool, 'show_logo': show_logo_bool, 'item_list': item_list,
               'last_labels': last_labels}
    return render(request, 'home/items.html', context)
