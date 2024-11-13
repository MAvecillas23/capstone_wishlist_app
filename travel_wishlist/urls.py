from django.urls import path
from . import views

# routing
# create url paths
urlpatterns = [
    path('', views.place_list, name='place_list'),  # if there is no admin path involved... takes you to wishlist template
    path('visited',views.places_visited, name='places_visited'), # url path for visited page
    path('place/<int:place_pk>/was_visited/', views.place_was_visited, name='place_was_visited'),
    path('about', views.about, name='about'),  # url path for about page
    path('place/<int:place_pk>', views.place_details, name='place_details'),
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place')
]

# for uploading images to page
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)