import schemaField
class sliceRecord(object):
    def __init__(self, schema):
        '''
        Constructor
        '''
        self.schema = schema # schema is a list
        self.record = [] 
        
        for i in range(len(self.schema)):
            self.record.append('')
    
    def fillEle(self, fieldName, value):
        for index in range(len(self.schema)):
            field = self.schema[index]
            name = field.getName()
            if name == fieldName:
                self.record[index]=value
                
    def get(self, fieldName):
        for index in range(len(self.schema)):
            field = self.schema[index]
            name = field.getName()
            if name == fieldName:
                return self.record[index]
            
    def isFloat(self,number):
            return number.replace('.','',1).isdigit()
    
    def setValue(self,values):
        msg = ""
        for i in range(len(values)):
            schField = self.schema[i]
            info = values[i].split("|",1)
            if info[0]==schField.getName():
                schType = schField.getType()
                if (schType == "FLOAT") :   
                    if self.isFloat(info[1]) :
                        v = float(info[1])
                        self.fillEle(info[0], v)                         
                    elif (info[1] == "") :
                        continue
                    else:                        
                        msg = "there is an invalid value whose type should be Float."
                        break
                elif (schType == "INT") :
                    if (info[1].isdigit()):
                        v = int(info[1])
                        self.fillEle(info[0], v)                         
                    elif (info[1] == ""):
                        continue
                    else:                        
                        msg = "there is an invalid value whose type should be Int." 
                        break   
                elif (schType == "STRING") :
                    if (info[1] == ""):
                        continue
                    else:
                        self.fillEle(info[0],info[1])                                    
            else:
                for i in range(len(self.schema)):
                    if info[0] == self.schema[i].getName():
                        if (self.schema[i].getType() == "FLOAT") :   
                            if (self.isFloat(info[1])) :
                                v = float(info[1])
                                self.fillEle(info[0], v)                               
                            elif (info[1] == "") :
                                continue
                            else:                                
                                msg = "there is an invalid value whose type should be Float."
                                break
                        elif (self.schema[i].getType() == "INT") :
                            if (info[1].isdigit()):
                                v = int(info[1])
                                self.fillEle(info[0], v)                                  
                            elif(info[1] == ""):
                                continue 
                            else:
                                msg = "there is an invalid value whose type should be Int."    
                                break
                        elif (self.schema[i].getType() == "STRING") :
                            if (info[1] == ""):
                                continue
                            else:
                                self.fillEle(info[0],info[1])       
        return msg
                                              
                    
            
            
            
            
            
        
    