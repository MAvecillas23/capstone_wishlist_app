from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.


# render wishlist html template
def place_list(request):
    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)   # creating a form from data in the request
        place = form.save() # creating a model object from form
        if form.is_valid(): # validation against DB constraints
            place.save()   # daves place to db
            return redirect('place_list')   # reloads home page

    places = Place.objects.filter(visited=False).order_by('name') # from db get only places that were not visited and order by name
    new_place_form = NewPlaceForm()  # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form}) # display wishlist html webpage

# about page
def about(request):
    author = 'Michael'
    about = 'A website to create a list of places to visit'

    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

# places visited... visited page
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

# this function is for when the visited button is pressed for a place
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()

        return redirect('place_list')  # redirect to wishlist places
