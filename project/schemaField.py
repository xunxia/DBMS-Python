
class schemaField(object):
    '''
    this class is to define the details of every fields of the schema
    '''

    def __init__(self, name, dataType):
        '''
        Constructor
        '''
        self.name = name
        self.dataType = dataType
        
    def getName(self):
        return self.name
    
    def getType(self):
        return self.dataType
