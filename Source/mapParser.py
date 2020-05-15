from datetime import datetime
from datetime import timedelta
import csv
import os

def IsOnlySpaces(myLine, initial, final):
  sectionToAnalize = myLine[initial:final]
  for i in sectionToAnalize:
    if(i != " "):
      return False
  return True

def GetAddressAndLength(myLine):
  countOfHexValues = myLine.count('0x')
  address = -1
  length = -1
  if(countOfHexValues == 2):
    if (IsOnlySpaces(myLine, myLine.find(" ", myLine.find("0x")), myLine.rfind("0x"))):
      address = myLine[myLine.find("0x") :myLine.find(" ", myLine.find("0x"))]
      length = myLine[myLine.rfind("0x") :myLine.find(" ", myLine.rfind("0x"))]

  return address , length
    

def IsSectionBreaker(myLine):
  if(myLine[0] == "."):
    return True
  else:
    return False

def IsValidAddress(myAddress, mySize):
  valueToReturn = False
  if(myAddress == -1):
    valueToReturn = False
  else:
    addressDecimal = int(myAddress,0)
    sizeDecimal = int(mySize,0)
    if((addressDecimal > 0) and (sizeDecimal > 0)):
      valueToReturn = True

  return valueToReturn

def GetMemoryType(myLine):
  memoryType = myLine[myLine.find(".") + 1 :myLine.find(" ")]
  return memoryType

def GetFolderName(myLine):
  levels = myLine.count('/')
  folderName = " "
  if (levels >= 2):
    lastDivider = myLine.rfind("/")
    otherDivider = myLine.rfind("/",0, lastDivider)
    folderName = myLine[otherDivider + 1 :lastDivider]
  return folderName

def GetObjectName(myLine):
  dividerLocation = myLine.rfind("/")
  par = myLine.rfind("(")
  fill = myLine.count('*fill*')
  levels = myLine.count('/')
  folderName = GetFolderName(myLine)
  if (fill > 0):
    objectName = "Padding"
  elif (dividerLocation < par):
    objectName = myLine[par + 1 :myLine.rfind(".")]
  else:
    objectName = myLine[dividerLocation + 1 :myLine.rfind(".")]

  return objectName, folderName

def append_list_as_row(fileName, listOfElem):
    with open(fileName, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(listOfElem)

def main():
  
  initialTime = datetime.now()
  smallSampleFile = open("MapParser/MapFiles/smallSampleFile.map", "r")
  count = len(open("MapParser/MapFiles/smallSampleFile.map").readlines(  ))

  if os.path.exists("output.csv"):
    os.remove("output.csv")


  rowContent = ["Line", "Memory Type", "Address", "Size" , "Name", "Folder Name"]
  append_list_as_row('output.csv', rowContent)


  if smallSampleFile.mode == 'r':
    sectionBreakerFound = False
    for x in range(0,count) :
      line = smallSampleFile.readline()
      if (IsSectionBreaker(line)):
        sectionBreakerFound = True
        memoryType = GetMemoryType(line)
        sectionAddressStart , sectionTotalSize = GetAddressAndLength(line)
      else:
        address , sizeHex =  GetAddressAndLength(line)
        if (sectionBreakerFound and IsValidAddress(address, sizeHex)):
          objectName , folderName= GetObjectName(line)
          size = int(sizeHex,0)
          # print("Line: "+ str(x) + " Memory Type " + memoryType + " Address "+ address + " Lenght: " + str(size) + " Object " + objectName )
          rowContent = [x, memoryType, address, size , objectName, folderName]
          append_list_as_row('output.csv', rowContent)

  print ("Total Processing time is : " + str(datetime.now() - initialTime)) 
  print ("Total analized lines are  : " + str(count)) 


if __name__ == "__main__":
  main();
