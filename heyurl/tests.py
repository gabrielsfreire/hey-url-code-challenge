from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from heyurl.models import Url, Click


class IndexTests(TestCase):
    def test_index_render_without_stored_urls(self):
        """
        Test that the index page renders without stored URLS
        """
        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())
        # Call the index page
        response = self.client.get(reverse('index'))
        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)
        # Assert that the page contains the expected content
        self.assertContains(response, "HeyURL")
        self.assertContains(response, "There are no URLs in the system yet!")

        # Assert that the table header is not present
        self.assertNotContains(response, "Clicks Count")

    def test_index_render_with_stored_urls(self):
        """
        Test that the index page renders with stored URLS
        """
        # Create a URL
        url1 = Url.objects.create(
            original_url="https://www.google.com",
            clicks=2,
        )
        url2 = Url.objects.create(
            original_url="https://www.facebook.com",
            clicks=5,
        )
        # Assert that there are no URLs in the system
        self.assertEqual(Url.objects.count(), 2)
        # Call the index page
        response = self.client.get(reverse('index'))
        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)
        # Assert that the page contains the expected content
        self.assertContains(response, "HeyURL")
        self.assertNotContains(response, "There are no URLs in the system yet!")

        # Assert that the table header is present
        self.assertContains(response, "Clicks Count")

        # Assert that there are both URLs in the table
        self.assertContains(response, url1.short_url)
        self.assertContains(response, url1.original_url)

        self.assertContains(response, url2.short_url)
        self.assertContains(response, url2.original_url)

    def test_store(self):
        """
        Test that the store view will create a new URL
        """
        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())

        original_url = "https://www.google.com"
        # Call the store view
        response = self.client.post(reverse('store'), {
            'original_url': original_url,
        })
        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)
        # Assert that the table header is present
        self.assertContains(response, "Clicks Count")
        # Assert that the URL is in the table
        self.assertContains(response, original_url)
        # Assert that there is a new URL in the database
        self.assertEqual(Url.objects.count(), 1)

    def test_store_missing_required_field(self):
        """
        Test that the store view returns an error when the original_url field is missing
        """
        # Call the store view
        response = self.client.post(reverse('store'), {})
        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)
        # Assert that the required field error is present
        self.assertContains(response, "This field is required")
        # Assert that there are no URLs in the table
        self.assertContains(response, "There are no URLs in the system yet!")

    def test_store_invalid_url(self):
        """
        Test that the store view returns an error when the original_url is invalid
        """
        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())

        original_url = "this.is.an.invalid_url"
        # Call the store view
        response = self.client.post(reverse('store'), {
            'original_url': original_url,
        })
        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)
        # Assert that the error message is present
        self.assertContains(response, "The Original URL is not valid!")
        # Assert that there are no URLs in the table
        self.assertContains(response, "There are no URLs in the system yet!")
        # Assert that the table header is not present
        self.assertNotContains(response, "Clicks Count")
        # Assert that there are no URLs in the database
        self.assertEqual(Url.objects.count(), 0)

    def test_store_url_already_exists(self):
        """
        Test that the store view returns an error when the original_url already exists
        """
        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())

        original_url = "https://www.google.com"
        # Create a URL
        url = Url.objects.create(
            original_url=original_url,
            clicks=2,
        )

        # Assert that there is a URL in the system
        self.assertEqual(Url.objects.count(), 1)

        # Call the store view
        response = self.client.post(reverse('store'), {
            'original_url': original_url,
        })
        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)
        # Assert that the error message is present
        self.assertContains(response, "The Original URL already exists!")
        # Assert that the table header is present
        self.assertContains(response, "Clicks Count")
        # Assert that there is only one URL in the database
        self.assertEqual(Url.objects.count(), 1)

    def test_short_url_click(self):
        """
        Test that the short URL click view will increment the clicks count and create a new Click object
        """
        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())
        # Assert that there are no Clicks in the system
        self.assertFalse(Click.objects.exists())

        original_url = "https://www.google.com"
        # Create a URL
        url = Url.objects.create(
            original_url=original_url
        )
        # Assert that there is a URL in the system
        self.assertEqual(Url.objects.count(), 1)

        # Assert that the url has no clicks
        url.refresh_from_db()
        self.assertEqual(url.clicks, 0)

        # Call the short URL click view
        response = self.client.get(reverse('short_url', kwargs={'short_url': url.short_url}))

        # Assert that the click count was incremented
        url.refresh_from_db()
        self.assertEqual(url.clicks, 1)

        # Assert that there is a new Click related to the URL
        self.assertEqual(Click.objects.filter(url=url).count(), 1)

        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 302)

        # Assert that the user was redirected to the original URL
        self.assertEqual(response.url, original_url)

    def test_short_url_click_does_not_exist(self):
        """
        Test that the short URL click view will return a 404 when the short URL does not exist
        """
        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())
        # Assert that there are no Clicks in the system
        self.assertFalse(Click.objects.exists())

        short_url = "R4nd0m"

        # Call the short URL click view
        response = self.client.get(reverse('short_url', kwargs={'short_url': short_url}))

        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)

        # Assert that the 404 page was rendered
        self.assertContains(response, "404")
        self.assertContains(response, "Short URL not found!")
        self.assertContains(response, "Go back to homepage")

    def test_metric_panel(self):
        """
        Test that the metric_panel view will return the correct data
        """
        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())
        # Assert that there are no Clicks in the system
        self.assertFalse(Click.objects.exists())

        original_url = "https://www.google.com"
        # Create a URL
        url = Url.objects.create(
            original_url=original_url,
            clicks=3
        )
        # Assert that there is a URL in the system
        self.assertEqual(Url.objects.count(), 1)

        # Assert that the url has no clicks
        url.refresh_from_db()
        self.assertEqual(url.clicks, 3)

        dt_now = timezone.now()
        dt_20 = dt_now.replace(day=20)
        dt_21 = dt_now.replace(day=21)

        # Create 3 Clicks objects
        Click.objects.create(
            url=url,
            browser="Chrome",
            platform="Windows",
            created_at=dt_20,
            updated_at=dt_20,
        )
        Click.objects.create(
            url=url,
            browser="Chrome",
            platform="Windows",
            created_at=dt_20,
            updated_at=dt_20,
        )
        Click.objects.create(
            url=url,
            browser="Safari",
            platform="Mac OS X",
            created_at=dt_21,
            updated_at=dt_21,
        )

        # Assert that there are 3 Clicks in the system
        self.assertEqual(Click.objects.count(), 3)

        # Call the short URL click view
        response = self.client.get(reverse('metric-panel', kwargs={'short_url': url.short_url}))

        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)

        # Assert that the metric panel page was rendered for the correct URL
        self.assertContains(response, 'Metric Panel: {}'.format(url.short_url))
        self.assertContains(response, 'Total clicks per day during this {}'.format(dt_now.strftime('%B')))
        self.assertContains(response, '{}'.format(dt_20.strftime('%B %d, %Y')))
        self.assertContains(response, '{}'.format(dt_21.strftime('%B %d, %Y')))

        # Assert that the metric panel rendered the browser and platform data correctly
        self.assertContains(response, 'Chrome')
        self.assertContains(response, 'Safari')
        self.assertContains(response, 'Windows')
        self.assertContains(response, 'Mac OS X')
        self.assertContains(response, "Browsers and Platforms used to click on the '/{}' URL during this {}".format(
            url.short_url, dt_now.strftime('%B')
        ))

    def test_metric_panel_no_click_to_render(self):
        """
        Test that the metric_panel will render the metric panel page with no data to render
        """
        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())
        # Assert that there are no Clicks in the system
        self.assertFalse(Click.objects.exists())

        original_url = "https://www.google.com"
        # Create a URL
        url = Url.objects.create(
            original_url=original_url,
        )
        # Assert that there is a URL in the system
        self.assertEqual(Url.objects.count(), 1)

        # Assert that there are no Clicks in the system
        self.assertEqual(Click.objects.count(), 0)

        dt_now = timezone.now()

        # Call the short URL click view
        response = self.client.get(reverse('metric-panel', kwargs={'short_url': url.short_url}))

        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)

        # Assert that the metric panel page was rendered for the correct URL
        self.assertContains(response, 'Metric Panel: {}'.format(url.short_url))

        # Assert that the table was not rendered
        self.assertContains(response, "There are no clicks for the '/{}' URL in this {}.".format(
            url.short_url, dt_now.strftime('%B')
        ))
        self.assertContains(response, "There are no clicks for the '/{}' URL in this {}.".format(
            url.short_url, dt_now.strftime('%B')
        ))

    def test_metric_panel_does_not_exist(self):
        """
        Test that the metric panel URL click view will return a 404 when the short URL does not exist
        """
        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())
        # Assert that there are no Clicks in the system
        self.assertFalse(Click.objects.exists())

        short_url = "R4nd0m"

        # Call the short URL click view
        response = self.client.get(reverse('metric-panel', kwargs={'short_url': short_url}))

        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)

        # Assert that the 404 page was rendered
        self.assertContains(response, "404")
        self.assertContains(response, "Short URL not found!")
        self.assertContains(response, "Go back to homepage")


class UrlsViewSetTests(TestCase):

    def test_list(self):
        """
        Test that the url list view will return the correct data
        """
        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())
        # Assert that there are no Clicks in the system
        self.assertFalse(Click.objects.exists())

        original_url_1 = "https://www.google.com"
        # Create a URL
        Url.objects.create(
            original_url=original_url_1,
            clicks=0
        )
        original_url_2 = "https://www.google.com"
        # Create a URL
        url = Url.objects.create(
            original_url=original_url_2,
            clicks=1
        )
        dt_now = timezone.now()

        Click.objects.create(
            url=url,
            browser="Safari",
            platform="Mac OS X",
            created_at=dt_now,
            updated_at=dt_now,
        )

        # Assert that there are 2 URLs in the system
        self.assertEqual(Url.objects.count(), 2)
        # Assert that there is 1 Click in the system
        self.assertEqual(Click.objects.count(), 1)

        response = self.client.get(reverse('urls-list'))

        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)

        # Get the response data
        response_data = response.json()

        # Assert that the response data is a list
        self.assertIsInstance(response_data['data'], list)

        # Assert that the response data has 2 items
        self.assertEqual(len(response_data['data']), 2)

        # Assert that the response data has the correct data
        self.assertEqual(response_data['data'][0]['attributes']['original-url'], original_url_1)

        # Assert that the response data has the correct data
        self.assertEqual(response_data['data'][1]['attributes']['original-url'], original_url_2)

    def test_list_empty(self):
        """
        Test that the url list view will return an empty list when there are no URLs
        """

        # Assert that there are no URLs in the system
        self.assertFalse(Url.objects.exists())
        # Assert that there are no Clicks in the system
        self.assertFalse(Click.objects.exists())

        response = self.client.get(reverse('urls-list'))

        # Assert that the page was rendered successfully
        self.assertEqual(response.status_code, 200)

        # Get the response data
        response_data = response.json()

        # Assert that the response data is a list
        self.assertIsInstance(response_data['data'], list)

        # Assert that the response data has 0 items
        self.assertEqual(len(response_data['data']), 0)
