# import unittest

from django.test.runner import DiscoverRunner
from django.test import TestCase
from django.test import Client

from django.core.urlresolvers import reverse
from django.conf import settings

import json



class HomePageTestCase(TestCase):

    # fixtures = ['geral.json','portal.json']
    #fixtures = ['portal/fixtures/caixa_pesquisa.json']

    def setUp(self):

        settings.DEBUG = True
        settings.TEST_RUNNER = 'tests.tests_with_no_db.NoDbTestRunner'
        self.client = Client()

        # When set kwargs['template'] = 'any' the system wont find the template folder
        # and will use the default template.
        self.home_url = reverse('home_sf', kwargs={'template':'open_data'})

    def test_details(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)



class FirstLoadTestCase(TestCase):

    # fixtures = ['geral.json','portal.json']
    #fixtures = ['portal/fixtures/caixa_pesquisa.json']

    def setUp(self):
        settings.DEBUG = True
        settings.TEST_RUNNER = 'tests.tests_with_no_db.NoDbTestRunner'
        self.client = Client()#(SERVER_NAME="shedar.fapesp.br:9001")

        """
        Load initial page, receive the whole HTMLs.
        On the html file there are many Ajax calls which fills data on the page.
        """
        # When set kwargs['template'] = 'any' the system wont find the template folder
        # and will use the default template.
        self.params_url = reverse('params_id', kwargs={'collection':'enem', 'id':'123456', 'template':'test'})
        response = self.client.get(self.params_url, follow=True)
        self.assertEqual(response.status_code, 200)

        # This is the id stored on the Django session at the server side.
        self.id_collection = response.context['id_collection']
        self.assertTrue(self.id_collection)

        # This is a basic empty payload used on the Ajax calls.
        self.payload = {
            'enem': {'query': 'null', 'ordem': 0, 'collection': "enem", 'selected_facets_col1': {'filtro': {}, 'wordcloud': {}}},
            'collection': "enem", 'ordem': 0,
            'query': 'null',
            'selected_facets_col1': {'filtro': {}, 'wordcloud': {}},
            'filtro': {},
            'wordcloud': {},
        }



    def test_search(self):
        """ Test main ajax request based on the collection id """
        self.entrypoint_url = reverse('search', kwargs={'collection':'enem', 'id':self.id_collection, 'template':'test'})
        response = self.client.post(self.entrypoint_url,
                                    json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content)

        # Assert some data
        self.assertEqual(len(json_data.keys()), 4)
        self.assertEqual(json_data['response']['numFound'], 6731341)
        self.assertEqual( json_data['facets']['count'], 6731341 )
        self.assertEqual( json_data['facets']['TP_LINGUA']['buckets'][0]['val'], 'Espanhol')
        self.assertEqual( json_data['facets']['TP_LINGUA']['buckets'][0]['count'], 3749674)
        self.assertEqual( json_data['facets']['TP_LINGUA']['buckets'][1]['val'], 'Ingles')
        self.assertEqual( json_data['facets']['TP_LINGUA']['buckets'][1]['count'], 2981667)


    def test_outcomes(self):
        """ Test ajax request - outcomes """
        self.outcomes_url = reverse('totalizadores', kwargs={'collection':'enem', 'id':self.id_collection, 'template':'test'})
        response = self.client.post(self.outcomes_url,
                                    json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content)
        self.assertEqual(len(json_data.keys()), 5)
        self.assertEqual(json_data['facet']['1']['numFound'], 6731341)
        self.assertEqual(json_data['facet']['1']['label'], 'Total de inscritos')


    def test_sankey_chart(self):
        """ Test ajax request - sankey chart """
        self.sankey_chart_url = reverse('multidimensional_chart', kwargs={'collection':'enem', 'chart_type':'sankey', 'id':self.id_collection, 'template':'test'})

        # Add chart selection data to payload
        self.payload['enem']['json_levels_list'] = [{'nivel_1': "REGIAO_PROVA_facet"}, {'nivel_2': "TP_ESCOLA"}]
        self.payload['enem']['0'] = {'nivel_1': "REGIAO_PROVA_facet"}
        self.payload['enem']['1'] = {'nivel_2': "TP_ESCOLA"}

        response = self.client.post(self.sankey_chart_url,
                                    json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content)

        # Assert some data
        self.assertEqual(len(json_data['nodes']), 129)
        self.assertEqual(json.loads( json_data['links'])[0]['source'], 0)
        self.assertEqual(json.loads( json_data['links'])[0]['target'], 1)
        self.assertEqual(json.loads( json_data['links'])[0]['value'], 1707754)


    def test_bubble_chart(self):
        """ Test ajax request - bubble chart """
        self.bubble_chart_url = reverse('multidimensional_chart', kwargs={'collection':'enem', 'chart_type':'bubble', 'id':self.id_collection, 'template':'test'})

        # Add chart selection data to payload
        self.payload['enem']['json_levels_list'] = [{'nivel_1': "REGIAO_PROVA_facet"}, {'nivel_2': "TP_ESCOLA"}]
        self.payload['enem']['0'] = {'nivel_1': "REGIAO_PROVA_facet"}
        self.payload['enem']['1'] = {'nivel_2': "TP_ESCOLA"}

        response = self.client.post(self.bubble_chart_url,
                                    json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content)

        # Assert some data
        self.assertEqual(len(json_data['result']), 20)
        self.assertEqual( json_data['result'][0]['count'], 319)
        self.assertEqual( json_data['result'][0]['name'], 'label')
        self.assertEqual( json_data['result'][0]['x_elemen'], 'Centro-Oeste')
        self.assertEqual( json_data['result'][0]['y_elemen'], 'Exterior')
        self.assertEqual( json_data['result'][0]['x_tick'], 0)
        self.assertEqual( json_data['result'][0]['y_tick'], 0)




    def test_boxplot_chart(self):
        """ Test ajax request - boxplot chart """
        self.boxplot_chart_url = reverse('multidimensional_chart', kwargs={'collection':'enem', 'chart_type':'boxplot', 'id':self.id_collection, 'template':'test'})

        # Add chart selection data to payload
        self.payload['enem']['json_levels_list'] = [{'nivel_1': "SG_UF_RESIDENCIA"}, {'nivel_2': "NU_IDADE"}]
        self.payload['enem']['0'] = {'nivel_1': "SG_UF_RESIDENCIA"}
        self.payload['enem']['1'] = {'nivel_2': "NU_IDADE"}

        response = self.client.post(self.boxplot_chart_url,
                                    json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content)

        # Assert some data
        self.assertEqual(len(json_data['result']), 27)
        self.assertEqual( json_data['result'][0]['x_axis'], 'SP')
        self.assertEqual( json_data['result'][0]['y_axis']['count'], 1133824)

        self.assertGreaterEqual( json_data['result'][0]['y_axis']['quartile1'], 15)
        self.assertLessEqual( json_data['result'][0]['y_axis']['quartile1'], 18)
        self.assertGreaterEqual( json_data['result'][0]['y_axis']['quartile3'],  23)
        self.assertLessEqual( json_data['result'][0]['y_axis']['quartile3'],  24)
        self.assertGreaterEqual( json_data['result'][0]['y_axis']['median'], 19)
        self.assertLessEqual( json_data['result'][0]['y_axis']['median'], 20)
        self.assertGreaterEqual( json_data['result'][0]['y_axis']['mean'], 21)
        self.assertLessEqual( json_data['result'][0]['y_axis']['mean'], 22)






class InitialCongigurationsTestCase(TestCase):
    """ Test the init functions of app, on __init__.py """
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

#
# if __name__ == '__main__':
#     unittest.main()
