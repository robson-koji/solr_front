import logging
logger = logging.getLogger(__name__)

class GetSolarDataException(Exception):
    """ Throw this on any exception caused by solr_front component to get Solr data """
    pass


class GenericLoggerException(Exception):
    """Exception basica para logar no sistema o erro"""
    def __init__(self, classe, error, inspect=None):

        super(GenericLoggerException, self).__init__(error)
        self.classe = classe
        self.message = []
        self.message.append("---------------------------------------------")
        self.message.append(str(error))
        self.message.append("Class Error: %s" %(self.classe.__class__.__name__))
        if not inspect is None:
                self.message.append( "Method: %s" % (inspect[0][3]) )
                self.message.append( "Line: %s" % (inspect[0][2]) )
        self.message.append("---------------------------------------------")
        for line in self.message:
            logger.error(line)
        self.message = '\n'.join(self.message)

    def __str__(self):
        return self.message
