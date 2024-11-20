from urllib.error import HTTPError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required # login needs to be required for each view
from django.http import HttpResponseForbidden
from django.contrib import messages
# Create your views here.


# render wishlist html template
# @login_required need a login to access
@login_required()
def place_list(request):
    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)   # creating a form from data in the request
        place = form.save(commit=False) # creating a model object from form
        place.user = request.user
        if form.is_valid(): # validation against DB constraints
            place.save()   # daves place to db
            return redirect('place_list')   # reloads home page

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name') # from db get only places that were not visited and order by name
    new_place_form = NewPlaceForm()  # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form}) # display wishlist html webpage

# about page
@login_required()
def about(request):
    author = 'Michael'
    about = 'A website to create a list of places to visit'

    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

# places visited... visited page
@login_required()
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

# this function is for when the visited button is pressed for a place
@login_required()
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden

        return redirect('place_list')  # redirect to wishlist places

@login_required()
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # does this place belong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden

    # is this a GET request or a POST request?
    # if POST request, validate form data and update.
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk)
    else:
        # if GET request, show Place info and form
        # if place is visited, show form; if place is not visited, no form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place,
                                                                               'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place,})

# delete a place from wishlist
@login_required()
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    # if user wanting to delete place is the correct user delete place
    print(place)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    # don't delete place
    else:
        return HttpResponseForbidden()
