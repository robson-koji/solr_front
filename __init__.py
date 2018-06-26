import os
import re, json
import logging

from django.core.files import File

logger = logging.getLogger(__name__)

PROJECT_PATH = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_NAME = os.path.basename(PROJECT_PATH)


class ConfigurationError(Exception):
    pass


class SolrFrontStructure(object):
    def __init__(self):
        def custom_import(name):
            components = name.split('.')
            mod = __import__(components[0])
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod

        # Try to locate a custom configuration folder on the settings.py of the project
        settings = custom_import(PROJECT_NAME + '.settings')
        try:
            self.config_path = settings.SORL_FRONT_CONFIG_PATH
        except AttributeError:
            self.config_path = os.path.dirname(__file__) + '/conf/sample/'
        self.collections_path = self.config_path + 'collections/'


    def remove_comments(self, string):
        string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
        return string


    def get_structure(self):
        """ Get main configuration file """
        logger.info("Loading graph structure from: %s",  self.config_path)
        with open(self.config_path + 'solr_front_conf.json', 'r') as f:
            # solr_front_conf= File(f)
            try:
                data = ''
                for line in f:
                    data += line
                    data = self.remove_comments(data)
                self.solr_front_conf = json.loads(data)
                logger.info("Solr Front JSON structure loaded: %s",  self.solr_front_conf)
            except ValueError as e:
                logger.exception(e)
                raise ValueError

        GRAPH = self.solr_front_conf['GRAPH']
        EDGES = self.solr_front_conf['EDGES']
        return (GRAPH, EDGES)


    def get_collections(self):
        """ Get all collections configuration files """
        logger.info("Loading collections: %s",  self.collections_path)
        collections = {}
        self.vertices_config_files = []
        for root, dirs, files in os.walk(self.collections_path):
            files = [file for file in files if os.path.splitext(file)[1] == '.json']

            if not files:
                logger.exception("No collection config file found at: %s", self.collections_path)
            for file in files:
                collection = file.replace('.json', '')
                self.vertices_config_files.append(collection)
                with open(self.collections_path + file, 'r') as f:
                    data = ''
                    for line in f:
                        data += line
                        data = self.remove_comments(data)
                    try:
                        collections[collection] = json.loads(data)
                    except ValueError as e:
                        logger.error('Collection JSON config error: %s' %(collection) )
                        logger.error(e)



            return collections


    def graph_valid(self):
        """ Check graph vertices against vertices configuration files. """
        graph = self.solr_front_conf['GRAPH']
        graph_vertices = set(graph.keys())

        for vertice in graph.keys():
            graph_vertices.update(graph[vertice])

        diff_1 = graph_vertices - set(self.vertices_config_files)
        diff_2 = set(self.vertices_config_files) - graph_vertices

        try:
            if bool(diff_1) and list(diff_1) > 0:
                raise ConfigurationError("""Missing collection configuration files: %s.
                These collections are defined vertices or required vertices.
                Reconfigure the Graph structure or create missing config files.""" % (str(diff_1)))
            elif bool(diff_2) and list(diff_2) > 0:
                raise ConfigurationError("Collections configuration files exist but are not defined at the Graph structure: %s. Delete remaining config files or add them to the Graph structure." % (str(diff_2)))
            else:
                logger.info("Initial configuration is ok. Graph structure and collections configuration files are the same: %s" %(str(graph_vertices)))
        except ConfigurationError as e:
            logger.error(e)
            raise

        return True


    def collection_fields_valid(self):
        """ Check if fields of a giver collection match solr collection """
        # TODO OR NOT TODO. A little bit complex to get all fields from a collection config file.
        pass


sfs_object = SolrFrontStructure()
(GRAPH, EDGES) = sfs_object.get_structure()
COLLECTIONS = sfs_object.get_collections()
sfs_object.graph_valid()
