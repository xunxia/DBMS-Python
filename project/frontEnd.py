import sys
import actions
import os

def showMenu():
    print("\nSlice DB Menu\n")
    print("1.Create Database")
    print("2.Update Record")
    print("3.Add record")
    print("4.Delete Record")
    print("5.Bulk load")
    print("6.Display Join")
    print("7.Run Query")
    print("8.Report 1")
    print("9.Report 2") 
    print("10.Lookup Record")  
    print("11.Exit")
    return

cust = actions.createDatabase("CustDB", 5, ["cust|int","name|string","age|int","phone|string","address|string"], "cust")
sales = actions.createDatabase("SalesDB", 4, ["order|int","cust|int","date|string","total|float"], "order")
order = actions.createDatabase("OrderDB", 2, ["order|int","item|string"], "")

showMenu()
while(True):
    choice = input("\nSelect:")           
    if choice =="1":
        storeList = []
        name = input("please enter the new table name:")
        while(True):
            count = input("please enter the count of the number of fields:")
            if count.isdigit():
                c = int(count)
                break
            else:
                print("please input an number.")
        for i in range(c):
            while(True):
                col = input("please enter No. %d column's name and type \n with this format: \"column name|column type\": " %(i+1))
                if ( col.upper().endswith("|STRING") or col.upper().endswith("|INT") or col.upper().endswith("|FLOAT") ) :
                    storeList.append(col)
                    break
                else:
                    print("please enter full info which includes the Type.")
        while(True):
            indexCol = input("please enter the index column name:")
            nameList = []
            for i in range(len(storeList)):
                temp = storeList[i].split("|",storeList[i].count("|"))
                nameList.append(temp[0])
            if indexCol=="" :
                break
            elif not (indexCol in nameList) :
                print("the index column you entered is not one of the existing columns")
            elif indexCol in nameList:
                break  
        msg = actions.createDatabase(name, c, storeList, indexCol)    
        print(msg)            
        showMenu()
        continue
    elif choice=="2":
        dbName = input("please enter the database name:")
        check = actions.checkDB(dbName)            
        if check :
            keyExist = actions.keyExist(dbName)
            if keyExist :
                schema = actions.getSchema(dbName)
                indexCol = actions.getIndCol(dbName)
                indexKey = input("please enter the key value:")
                v = []
                for i in range(len(schema)):
                    field = schema[i]
                    name = field.getName()
                    if name == indexCol:
                        v.append(name+"|"+"")
                    else:
                        value = input("please enter the %s (if you don't want to update this value, just hit the enter key):" %name)
                        v.append(name+"|"+value)
                msg = actions.updateRecord(dbName, v, indexKey)
                print(msg)
            else:
                print("This database have no key, so you cannot update a record.")
        else:
            print("there is no such database, please create database first.")        
        showMenu()
        continue
    elif choice=="3":
        dbName = input("please enter the database name:")
        check  = actions.checkDB(dbName)
        if check :
            schema = actions.getSchema(dbName)
            v = []
            for i in range(len(schema)):
                field = schema[i]
                name = field.getName()
                value = input("please enter the %s :" %name)
                v.append(name+"|"+value)
            msg = actions.addRecord(dbName, v)   
            print(msg)
        else:
            print("there is no such database, please create database first.")                     
        showMenu()
        continue
    elif choice=="4":
        dbName = input("please enter the database name:")
        check = actions.checkDB(dbName)
        if check:
            keyExist = actions.keyExist(dbName)
            if keyExist :
                key = input("please enter the delete key:")
                result = actions.deleteRecord(dbName, key)
                print(result)
            else:
                print("This database have no key, so you cannot update a record.")
        else:
            print("there is no such database.")   
        showMenu()
        continue
    elif choice=="5":
        dbName = input("please enter the database name:")
        check = actions.checkDB(dbName)
        if check:
            fileName = input("please enter the upload file name(include the suffix, like \".txt\"):")
            msg = actions.bulkLoad(dbName, fileName)
            print(msg)
        else:
            print("there is no such database.")               
        showMenu()
        continue
    elif choice=="6":
        dbName1 = input("please enter the first database name:")
        check = actions.checkDB(dbName1)
        if check :
            dbName2 = input("please enter the second database name:")
            check2 = actions.checkDB(dbName2)
            if check2 :
                joinCol = input("please enter the join column name:")
                strShow = actions.join(dbName1, dbName2, joinCol)
                print(strShow)
            else:
                print("there is no such database")
        else:
            print("there is no such database")        
        showMenu()
        continue
    elif choice=="7":
        dbName = input("please enter the database name:")
        check = actions.checkDB(dbName)
        if check:            
            dispCol = input("please enter the display columns, use \"|\" to delimited: ")
            condition = input("please enter the condition with the following format: column|condition|literal value :" )
            msg = actions.runQuery(dbName, dispCol, condition)
            print(msg)
        else:
            print("there is no such database")
        showMenu()
        continue
    elif choice=="8":
        actions.saveAllDB()
        os.system('Report1.exe')      
        showMenu()
        continue
    elif choice=="9":
        actions.saveAllDB()
        os.system('Report2.exe')       
        showMenu()
        continue
    elif choice=="10":
        dbName = input("please enter the database name:")
        check = actions.checkDB(dbName)            
        if check :
            keyExist = actions.keyExist(dbName)
            if keyExist :
                key = input("please enter the key value:")
                msg = actions.lookupRecord(dbName, key)
                print(msg)
            else:
                print("This database have no key, so you cannot get a record.")
        else:
            print("there is no such database, please create database first.") 
        showMenu()
        continue
    elif choice=="11":
        actions.saveAllDB()
        print("Good Bye")
        exit()
    else:
        print("invalid input, enter an integer between 1-11.\n")
        showMenu()
        continue