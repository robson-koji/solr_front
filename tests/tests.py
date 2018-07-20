import unittest

from django.test.runner import DiscoverRunner
from django.test import TestCase
from django.test import Client

from django.core.urlresolvers import reverse
from django.conf import settings



class HomePageTestCase(unittest.TestCase):
    def setUp(self):
        settings.DEBUG = True
        settings.TEST_RUNNER = 'tests.tests_with_no_db.NoDbTestRunner'
        self.client = Client()

        # When set kwargs['template'] = 'any' the system wont find the template folder
        # and will use the default template.
        self.home_url = reverse('home_sf', kwargs={'template':'any'})

    def test_details(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)



class SearchTestCase(unittest.TestCase):
    def setUp(self):
        settings.DEBUG = True
        settings.TEST_RUNNER = 'tests.tests_with_no_db.NoDbTestRunner'
        self.client = Client()

        # When set kwargs['template'] = 'any' the system wont find the template folder
        # and will use the default template.
        self.entrypoint_url = reverse('params_id', kwargs={'collection':'graph_auxilios', 'id':'123456', 'template':'any'})

    def test_params(self):
        response = self.client.get(self.entrypoint_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['id_collection'])



class InitialCongigurationsTestCase(unittest.TestCase):
    from solr_front.views import SolrFrontStructure
    sfs_object = SolrFrontStructure()

    def test_get_structure(self):
        assert len(self.sfs_object.get_structure()) == 2, "Returned 2 elements on the Graph structure. Probably Graph and Edges."

    def test_get_collections(self):
        COLLECTIONS = self.sfs_object.get_collections()
        assert len(COLLECTIONS.keys()) > 0, "At least one collection is defined."

    def test_graph_valid(self):
        from solr_front.views import ConfigurationError
        self.assertTrue(self.sfs_object.graph_valid())


if __name__ == '__main__':
    unittest.main()
