import schemaField
import sliceDB
import sliceEnv
import sliceRecord


def createDatabase(name, count, colInfo, index):
    dbSchema = createSchema(count, colInfo)
    env = sliceEnv.sliceEnv()
    if name not in env.dbInfo:
        env.createDB(name, dbSchema, index)   
        msg = "create successfully."
    else:
        msg = "this table name has already exist."
    env.close(name)
    return msg
    
def createSchema(count,colInfo):
    schema = []
    for i in range(count):
        fieldList = colInfo[i].split("|",colInfo[i].count("|"))
        name = fieldList[0].lower()
        colType = fieldList[1].upper()
        field = schemaField.schemaField(name, colType)
        schema.append(field)
    return schema

def checkDB(dbName):
    env = sliceEnv.sliceEnv()
    if dbName in env.dbInfo :
        return True
    else:
        return False

def keyExist(dbName):
    env = sliceEnv.sliceEnv()
    db = env.dbInfo[dbName]
    indexCol = db.indexColumn
    if indexCol == "" :
        return False
    else:
        return True

def getSchema(dbName):
    env =sliceEnv.sliceEnv()
    if dbName in env.dbInfo:
        db = env.dbInfo[dbName]
        schema = db.schema
    return schema

def getIndCol(dbName):
    env =sliceEnv.sliceEnv()
    db = env.dbInfo[dbName]
    index = db.indexColumn
    return index

def updateRecord(dbName, values, key):
    #print(values)
    temp=[]
    for i in range(len(values)):
        info = values[i].split("|",1)
        if info[1]!="":
            temp.append(values[i])
    #print(temp)
    env = sliceEnv.sliceEnv()
    sliceDB = env.open(dbName)
    if key in sliceDB.database:
        record = sliceDB.getRecord(key)
        msg = record.setValue(temp)
        if msg == "":
            sliceDB.setRecord(record)
            env.close(dbName)
            return "update record successfully!"
        else:
            return msg
    else:
        return "The key of the update record was wrong! There is no such record."

def addRecord(dbName,values):
    env = sliceEnv.sliceEnv()
    sliceDB = env.open(dbName)
    schema = sliceDB.schema
    indCol = sliceDB.indexColumn
    ''' if is for the Database with no index column, else is for the database with index column.'''
    if indCol == "":
        record = sliceDB.createRecord()
        msg =  record.setValue(values)
        if msg == "":
            sliceDB.setRecord(record)
            env.close(dbName)
            return "add record successfully!"
        else:
            return msg
    else:        
        for i in range(len(schema)):
            if schema[i].getName() == indCol:
                v = values[i].split("|",1)
                v1= v[1]
        if v1 not in sliceDB.database:
            if v1!= "":
                record = sliceDB.createRecord()
                msg =  record.setValue(values)
                if msg == "":
                    sliceDB.setRecord(record)
                    env.close(dbName)
                    return "add record successfully!"
                else:
                    return msg
            else:
                return "Failed. The key cannot be empty."
        else:
            return "Failed. This key has already exist, please check.\n If you want to update the record, please choose update."
           
def deleteRecord(dbName, key):
    env = sliceEnv.sliceEnv()
    sliceDB = env.open(dbName)
    if key in sliceDB.database:
        msg = sliceDB.deleteRecord(key)
        if msg == "":
            env.close(dbName)
            return "delete record successfully!"
        else:
            return msg
    else:
        return "The key of the delete record was wrong! There is no such record."

def lookupRecord(dbName,key):
    env = sliceEnv.sliceEnv()
    sliceDB = env.open(dbName)
    if key in sliceDB.database:
        rec = sliceDB.getRecord(key)
        schema = rec.schema
        recordValue = rec.record
        strShow = ""
        for i in range(len(schema)):
            strShow += schema[i].getName()+": "+ str(recordValue[i])+"\n" 
        return strShow           
    else:
        return "The key of the lookup record was wrong! There is no such record."

def bulkLoad(dbName,fileName):
    env = sliceEnv.sliceEnv()
    sliceDB= env.open(dbName)
    msg = sliceDB.load(fileName)
    if msg == "":
        env.close(dbName)
        return "load file successfully!"
    else:
        return msg
    
    
def join(dbName1, dbName2, joinCol):
    env = sliceEnv.sliceEnv()
    db1 = env.open(dbName1)
    db2 = env.open(dbName2)
    result = db1.join(db2,joinCol)
    newSchema = result[0]
    joinDB = result[1]
    strShow=""
    tempSch = []
    for field in newSchema:
        name = field.getName()
        tempSch.append(name)
    var = "|"
    schStr = var.join(tempSch)
    strShow += schStr+"\n"
    for key in joinDB.keys():
        recordObj = joinDB[key]    
        var = "|"
        temp = []
        for i in range(len(recordObj.record)):
            tempValue = str(recordObj.record[i])
            temp.append(tempValue)
        recStr = var.join(temp)
        strShow += recStr+"\n"
    return strShow

def runQuery(dbName, displayCol, condition):
    env = sliceEnv.sliceEnv()
    sliceDB = env.open(dbName)
    condList = condition.split("|", condition.count("|"))
    seleCol = condList[0]
    literal = condList[2]
    displayList = displayCol.lower().split("|",condition.count("|"))
    fieldType = ""
    nameList = []
    for i in range(len(sliceDB.schema)):
        field = sliceDB.schema[i]
        nameList.append(field.getName())
        if field.getName() == seleCol:
            fieldType = field.getType()
    if seleCol not in nameList:
        return "there is no such select column" 
    for disCol in displayList:
        if disCol not in nameList:
            return "there is no such display column"  
    if ((fieldType == "INT") and (literal.isdigit())):
        dispCol = displayCol.lower()
        result = sliceDB.query(dispCol, condition)
        strR = displayCol+"\n"
        for i in range(len(result)):
            strR += result[i]+"\n"
        return strR
    elif ((fieldType == "FLOAT") and (isFloat(literal))):
        dispCol = displayCol.lower()
        result = sliceDB.query(dispCol, condition)
        strR = displayCol
        for i in range(len(result)):
            strR += result[i]+"\n"
        return strR
    elif (fieldType == "STRING"):
        dispCol = displayCol.lower()
        result = sliceDB.query(dispCol, condition)
        strR = displayCol+"\n"
        for i in range(len(result)):
            strR += result[i]+"\n"
        return strR
    else:
         return "The literal should be with the same type as the select column."

def isFloat(number):
    return number.replace('.','',1).isdigit()

def saveAllDB():
    env = sliceEnv.sliceEnv()
    for key in env.dbInfo.keys():
        db = env.dbInfo[key]
        db.writeIntoFile()

    
    
    
    
    
    
    
    
    
    