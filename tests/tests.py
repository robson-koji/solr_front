import unittest
from django.test import Client
from django.test import TestCase
from django.test.runner import DiscoverRunner
from django.conf import settings



class HomePageTestCase(unittest.TestCase):
    def setUp(self):
        settings.DEBUG = True
        settings.TEST_RUNNER = 'tests.tests_with_no_db.NoDbTestRunner'
        self.client = Client()

    def test_details(self):
        response = self.client.get('/pt/buscador/bv/')
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        # self.assertEqual(len(response.context['customers']), 5)

#"""

class SearchTestCase(unittest.TestCase):

    def setUp(self):
        settings.DEBUG = True
        settings.TEST_RUNNER = 'tests.tests_with_no_db.NoDbTestRunner'
        self.client = Client()

    def test_params(self):
        response = self.client.get('/pt/buscador/bv/graph_auxilios/44480903/params/')

        dando erro no teste aqui.

        # print(response['location'])

        # import pdb; pdb.set_trace()
        # Check that the response is 200 OK.

        # !!! Corrigir aqui e a URL inicil tirando as referencias da BV.
        self.assertEqual(response.status_code, 302)

        # Check that the rendered context contains 5 customers.
        # self.assertEqual(len(response.context['customers']), 5)
#"""



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
