import sliceDB

class sliceEnv(object):
    '''
    classdocs
    '''
    
    dbInfo = {}

    def __init__(self):
        '''
        Constructor
        '''
        pass
    def createDB(self, name, schema, indexColumn):

        db = sliceDB.sliceDB(name, schema, indexColumn)
        #info = db
        sliceEnv.dbInfo[name] = db
        
    def open(self, name):       
        db = sliceEnv.dbInfo[name]
        return db
        
    def close(self,name):
        db = sliceEnv.dbInfo[name]
        db.writeIntoFile()
        
        
        