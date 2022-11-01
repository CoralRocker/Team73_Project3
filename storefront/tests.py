from django.test import TestCase, SimpleTestCase

class SimpleTests(SimpleTestCase):
    # tests to see if the status code returned by the home
    # page is equal to 200, which means the page exists.
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
