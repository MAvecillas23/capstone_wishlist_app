from django.test import TestCase
from django.urls import reverse
from .models import Place

# Create your tests here.

# tests for the homepage
class TestHomePage(TestCase):
    # checks if correct message is used when there is an empty list along with the write template
    def test_home_page_shows_empty_list_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')

# tests for wish list
class TestWishList(TestCase):
    fixtures = ['test_places']

    # checks whether place_list contains and doesn't contain correct places
    def test_wishlist_contains_not_visited(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

# tests for the visited paged
class TestVisitedPage(TestCase):

    def test_visited_page_shows_empty_list_message_for_empty_database(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet')

class VisitedList(TestCase):
    fixtures = ['test_places']
    # checks if visited places have the correct places
    def test_visited_list_shows_visited_places(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response,'San Francisco')
        self.assertContains(response, "Moab")
        self.assertNotContains(response, 'New York')
        self.assertNotContains(response, 'Tokyo')

# tests new places being added
class TestAddNewPlace(TestCase):
    # checks if new place is being added correctly and if being redirected after
    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)  # follow=True basically means once
                                                                            # once new place is added redirect like it normally should
                                                                            # unittests don't automatically do this
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        response_places = response.context['places']
        self.assertEqual(1, len(response_places))  # check only one place
        tokyo_from_response = response_places[0]

        tokyo_from_db = Place.objects.get(name='Tokyo', visited=False)

        self.assertEqual(tokyo_from_db, tokyo_from_response)


class TestVisitPlace(TestCase):
    fixtures = ['test_places']

    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, ))
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)

    def test_non_existent_place(self):
        visit_notexistent_place_url = reverse('place_was_visited', args=(1234, ))
        response = self.client.post(visit_notexistent_place_url,follow=True)
        self.assertEqual(404, response.status_code)


