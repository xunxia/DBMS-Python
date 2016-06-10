import sliceRecord
import schemaField

class sliceDB(object):
    '''
    classdocs
    '''
    def __init__(self, name, schema, indexColumn):
        '''
        Constructor
        '''
        self.database = {}
        self.name = name
        self.schema = schema
        self.indexColumn = indexColumn
        self.recordNum = 0
        
    def createRecord(self):
        record = sliceRecord.sliceRecord(self.schema) 
        return record
    
    def setRecord(self, record):
        if self.indexColumn == "":
            self.database[self.recordNum] = record
            self.recordNum = self.recordNum+1
        else:            
            keyIndex = 0
            for i in range(len(self.schema)):
                if self.indexColumn == self.schema[i].getName():
                    keyIndex = i
                    break        
            key = str(record.record[keyIndex])     
            if key not in self.database:
                self.database[key] = record  
        
    def getRecord(self, index):
        record = self.database[index]
        return record
    
    def deleteRecord(self,key):
        if key in self.database:
            del self.database[key]
            return ""
        else:
            return "there is no such record"
        
    
    def load(self,fileName):
        self.database.clear()
        file= open(fileName, "r")
        while True:
            line = file.readline()
            if not line:
                break
            else:
                line = line.rstrip("\n")
                info = line.split("|", line.count("|"))
                tempRecoValue = []
                for i in range(len(self.schema)):
                    name = self.schema[i].getName()
                    fieldValue = name+"|"+info[i]
                    tempRecoValue.append(fieldValue)
                record = self.createRecord()                
                msg = record.setValue(tempRecoValue)
                if msg == "":
                    self.setRecord(record)
                else:
                    return msg               
                tempRecoValue.clear()
        file.close()
        return ""
    def join(self, db2,joinCol):
        schema2 = db2.schema
        for i in range(len(self.schema)):
            field = self.schema[i]
            if field.getName() == joinCol:
                type1 = field.getType()
                break
        joinColIndex1 = i
                        
        for j in range(len(schema2)):
            field2 = schema2[j]
            if field2.getName() == joinCol:
                type2 = field.getType()
                break
        joinColIndex2 = j

        temp = []
        if type1 == type2:
            newSchema = self.schema + schema2            
            for i in range(len(newSchema)):
                for j in range(i+1, len(newSchema)):
                    f1 = newSchema[i]
                    name1 = f1.getName()
                    f2 = newSchema[j]
                    name2 = f2.getName()                    
                    if (name1 == name2):
                        temp.append(j)
                    else:
                        continue
            for index in temp:
                del newSchema[index]
        
            joinDB = {}
            recoNum = 1
            for oldRecKey in self.database.keys():
                oldRec = self.database[oldRecKey]    
                joinValue = oldRec.record[joinColIndex1] 
                
                for key2 in db2.database.keys():
                    oldRec2 = db2.database[key2]
                    joinValue2 = oldRec2.record[joinColIndex2]
                             
                    if joinValue == joinValue2:
                        newRecord = sliceRecord.sliceRecord(newSchema)
                        for i in range(len(oldRec.schema)):
                            fie = oldRec.schema[i]
                            name = fie.getName()
                            value = oldRec.record[i]
                            newRecord.fillEle(name, value)
                        for j in range(len(oldRec2.schema)):
                            fie2 = oldRec2.schema[j]
                            name2 = fie2.getName()
                            value2 = oldRec2.record[j]
                            newRecord.fillEle(name2, value2)
                            
                        joinDB[recoNum] = newRecord 
                        recoNum = recoNum+1
        result = [newSchema,joinDB]                                 
        return result
                
    def query(self,displayCol,condition):
        dispColList = displayCol.split("|", displayCol.count("|"))
        disp = []
        for i in range(len(self.schema)):
            field = self.schema[i]
            for j in range(len(dispColList)):
                if field.getName() == dispColList[j].lower():
                    disp.append(i)
        
        result = []
                                
        condList = condition.split("|", condition.count("|"))
        seleCol = condList[0].lower()
        op = condList[1].upper()
        literal = condList[2]
        
        for i in range(len(self.schema)):
            field = self.schema[i]
            if field.getName() == seleCol:
                fieldType = field.getType()
                break
        seleIndex = i
        
        if fieldType == "STRING" :
            for key in self.database.keys():
                reStr = ""
                rec = self.database[key]
                if op.upper() == "EQ":
                    if rec.record[seleIndex] == literal :
                        recoDispValue = []
                        for j in range(len(disp)):
                            recoDispIndex = disp[j]
                            recoDispValue.append(str(rec.record[recoDispIndex]))
                            var = "|"
                            reStr = var.join(recoDispValue)
                        result.append(reStr)
                        #recoDispIndex.clear() 
                elif op.upper()=="LT":
                    if rec.record[seleIndex] < literal :
                        recoDispValue = []
                        for j in range(len(disp)):
                            recoDispIndex = disp[j]
                            recoDispValue.append(str(rec.record[recoDispIndex]))
                            var = "|"
                            reStr = var.join(recoDispValue)
                        result.append(reStr)
                elif op.upper()=="GT":
                    if rec.record[seleIndex] > literal :
                        recoDispValue = []
                        for j in range(len(disp)):
                            recoDispIndex = disp[j]
                            recoDispValue.append(str(rec.record[recoDispIndex]))
                            var = "|"
                            reStr = var.join(recoDispValue)
                        result.append(reStr)
        
        elif fieldType == "INT":
            literInt = int(literal)
            if op.upper() == "EQ":
                for key in self.database.keys():
                    reStr = ""
                    rec = self.database[key]                
                    if rec.record[seleIndex] == literInt : 
                        recoDispValue = []
                        for j in range(len(disp)):
                            recoDispIndex = disp[j]
                            recoDispValue.append(str(rec.record[recoDispIndex]))
                            var = "|"
                            reStr = var.join(recoDispValue)
                        result.append(reStr)
                        #recoDispIndex.clear() 
            elif op.upper() == "LT":
                for key in self.database.keys():
                    reStr = ""
                    rec = self.database[key]
                    if rec.record[seleIndex] < literInt : 
                        recoDispValue = []
                        for j in range(len(disp)):
                            recoDispIndex = disp[j]
                            recoDispValue.append(str(rec.record[recoDispIndex]))
                            var = "|"
                            reStr = var.join(recoDispValue)
                        result.append(reStr)
                        #recoDispIndex.clear() 
            elif op.upper() == "GT":
                for key in self.database.keys():
                    reStr = ""
                    rec = self.database[key]
                    if rec.record[seleIndex] > literInt : 
                        recoDispValue = []
                        for j in range(len(disp)):
                            recoDispIndex = disp[j]
                            recoDispValue.append(str(str(rec.record[recoDispIndex])))
                            var = "|"
                            reStr = var.join(recoDispValue)
                        result.append(reStr) 
                        #recoDispIndex.clear()                
        
        elif fieldType == "FLOAT":
            literInt = float(literal)
            if op.upper() == "EQ":
                for key in self.database.keys():
                    reStr = ""
                    rec = self.database[key]                
                    if rec.record[seleIndex] == literInt : 
                        recoDispValue = []
                        for j in range(len(disp)):
                            recoDispIndex = disp[j]
                            recoDispValue.append(str(str(rec.record[recoDispIndex])))
                            var = "|"
                            reStr = var.join(recoDispValue)
                        result.append(reStr)
                        #recoDispIndex.clear() 
            elif op.upper() == "LT":
                for key in self.database.keys():
                    reStr = ""
                    rec = self.database[key]
                    if rec.record[seleIndex] < literInt : 
                        recoDispValue = []
                        for j in range(len(disp)):
                            recoDispIndex = disp[j]
                            recoDispValue.append(str(str(rec.record[recoDispIndex])))
                            var = "|"
                            reStr = var.join(recoDispValue)
                        result.append(reStr)
                        #recoDispIndex.clear() 
            elif op.upper() == "GT":
                for key in self.database.keys():
                    reStr = ""
                    rec = self.database[key]
                    if rec.record[seleIndex] > literInt : 
                        recoDispValue = []
                        for j in range(len(disp)):
                            recoDispIndex = disp[j]
                            recoDispValue.append(str(str(rec.record[recoDispIndex])))
                            var = "|"
                            reStr = var.join(recoDispValue)
                        result.append(reStr)
                        #recoDispIndex.clear() 
        return result

    def writeIntoFile(self):
        f = open(self.name+".slc.txt", "w")      
        restr = ""
        for key in self.database.keys():
            value = self.database[key]
            rec = value.record
            temp = []
            for ele in rec:
                ele = str(ele)
                temp.append(ele)
            var = "|"
            recoStr = var.join(temp)
            restr += recoStr+"\n"
        f.write(restr)
        f.flush()
        f.close()
 
                         
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        