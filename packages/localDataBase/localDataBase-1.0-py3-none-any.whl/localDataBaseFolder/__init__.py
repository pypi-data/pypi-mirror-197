
"""
LocalDataBase
-----------

Information
-----------
Version: 0.1.50
Developer: Thiago Stilo
GitHub: github.com/thiagostilo2121

"""

__all__= [
    "createData",
    "removeData",
    "findData",
    "createChase",
    "setChase",
    "findChase",
    "removeChase",
    "readChase",
    "setChaseNumber",
    "setDataName",
    "setChaseName",
    "findDataCreate",
    "findChaseCreate",
    "createArray"
]

class Errors(ExceptionGroup):
    class DataFolderError(ExceptionGroup):
        class NotExist(Exception):
               def __init__(self): print("The DataFolder dosen't exists")
    class ChaseError(ExceptionGroup):
        class NotExist(Exception):
            def __init__(self): print("The Chase dosen't exists")       

Array = list[tuple]


class dataClass():

     def __init__(self, x= None) -> None: ...

     def createData(self, dataFolder: str) -> bool:
         """
         Create a DataFolder
         """
         import os
         path_folder= findData(f"{dataFolder}")

         if path_folder == True:
             raise TypeError("The DataFolder already exist")
         else: 
             os.mkdir(f"{dataFolder}")
         return True
             
         
     def removeData(self, dataFolder: str) -> bool: 
         """
         Remove a DataFolder document
         """
         import os 
         if os.path.exists(f"{dataFolder}") == False:
             raise Errors.DataFolderError.NotExist()
         _D = os.remove(f"{dataFolder}")
         return True
     
     def findData(self, dataFolder: str) -> bool:
         """
         Find a DataFolder and return boolean (True or False)
         """

         import os 

         _F = os.path.exists(f"{dataFolder}")
         if _F == False:
             _F = False
         elif _F == True:
             _F = True

         return _F        

     def setDataName(self, dataFolder: str, __newName: str) -> bool | object:
         import os 

         if findData(dataFolder) == False:
             raise Errors.DataFolderError.NotExist()
         try:
             __NN = os.system(f"rename {dataFolder} {__newName}")
             return True
         except Exception as err:
             print(err)    
             return False
     def findDataCreate(self, dataFolder: str) -> bool | object:
         if findData(dataFolder) == True:
             return True    
         if findData(dataFolder) == False:
             _C = createData(dataFolder)
             return _C  

                  
class chaseClass():
     def __init__(self) -> None: ...
     def createChase(self, dataFolder: str, chase: str) -> object:
         if findData(f"{dataFolder}") == False:
             raise Errors.DataFolderError.NotExist
         with open(f"{dataFolder}/{chase}.txt", "a") as local:
             local.write("")
         
     def setChase(self, dataFolder: str, chase: str, __newContent: str, editType: str) -> object:

         edit = editType.lower()

         if edit != "a":
             if edit != "w":
                  raise TypeError(f"Edit Type: {edit} has not supported! only 'a' or 'w'")
         if findData(dataFolder) == False:
                raise Errors.DataFolderError.NotExist()
         if findData(f"{dataFolder}/{chase}.txt") == False:
                raise Errors.ChaseError.NotExist()
         with open(f"{dataFolder}/{chase}.txt", edit) as local:
                rt = local.write(__newContent)
                return rt
         
     def setChaseNumber(self, dataFolder: str, chase: str, __newContent: int | float, editType: str) -> object:
         edit = editType.lower()

         if edit != "a":
             if edit != "w":
                 raise TypeError(f"Edit Type: \"{edit}\" has not supported! onli 'a' or 'w'")    
         if findData(dataFolder) == False:
             raise Errors.DataFolderError.NotExist()
         if open(f"{dataFolder}/{chase}.txt") == False:
             raise Errors.ChaseError.NotExist()
         with open(f"{dataFolder}/{chase}.txt", edit) as local:
            rt = local.write(str(__newContent))
            return rt
         
     def findChase(self, dataFolder: str, chase: str) -> bool:
         if findData(f"{dataFolder}") == False:
             raise Errors.DataFolderError.NotExist()
         if findData(f"{dataFolder}/{chase}.txt") == False:
             _GHd = False
             return _GHd
         elif findData(f"{dataFolder}/{chase}.txt") == True:
             _GHd = True
             return _GHd
     def removeChase(self, dataFolder: str, chase: str) -> object: 
         if findData(f"{dataFolder}") == False:
             raise Errors.DataFolderError.NotExist()
         if findData(f"{dataFolder}/{chase}.txt") == False:
             raise Errors.ChaseError.NotExist()
         import os 
         os.remove(f"{dataFolder}/{chase}.txt")        
     def readChase(self, dataFolder: str, chase: str) -> str:
         if findData(f"{dataFolder}") == False:
             raise Errors.DataFolderError.NotExist()
         if findData(f"{dataFolder}/{chase}.txt") == False:
             raise Errors.ChaseError.NotExist()
         with open(f"{dataFolder}/{chase}.txt", "r") as local:
             _READs = local.read()    
             return _READs       
     def setChaseName(self, dataFolder: str, chase: str, __newName: str) -> bool | object:
         if findData(f"{dataFolder}") == False:
             raise Errors.DataFolderError.NotExist()
         if findChase(dataFolder, chase) == False:
             raise Errors.ChaseError.NotExist()
         import os
         try:
             os.system(f"rename {dataFolder}\{chase}.txt {__newName}.txt")
             return True
         except Exception as err:
             print(err)
             return False    
     def findChaseCreate(self, dataFolder: str, chase: str) -> bool | object:
         if findData(dataFolder) == False:
             raise Errors.DataFolderError.NotExist()
         if findChase(dataFolder, chase) == True:
             return True
         if findChase(dataFolder, chase) == False:
             _C = createChase(dataFolder, chase)
             return _C 

class Array():
    def createArray(self, *args) -> Array:
        Array = f"Array[{str(args)}]"
        return Array   


         
_inst = dataClass() 
createData = _inst.createData
removeData = _inst.removeData
findData = _inst.findData
setDataName = _inst.setDataName
findDataCreate = _inst.findDataCreate
_chst = chaseClass()
createChase = _chst.createChase
setChase = _chst.setChase
findChase = _chst.findChase
removeChase = _chst.removeChase
readChase = _chst.readChase
setChaseNumber = _chst.setChaseNumber
setChaseName = _chst.setChaseName
findChaseCreate = _chst.findChaseCreate
_array = Array()
createArray = _array.createArray
