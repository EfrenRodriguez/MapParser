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

def GetObjectName(myLine):
  dividerLocation = myLine.rfind("/")
  par = myLine.rfind("(")
  if (dividerLocation < par):
    initial = par
  else:
    initial = dividerLocation
  objectName = myLine[initial + 1 :myLine.rfind(".")]
  return objectName

def append_list_as_row(fileName, listOfElem):
    with open(fileName, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(listOfElem)

def main():
  
  smallSampleFile = open("MapParser/MapFiles/smallSampleFile.map", "r")
  count = len(open("MapParser/MapFiles/smallSampleFile.map").readlines(  ))
  initialTime = datetime.now()

  if os.path.exists("output.csv"):
    os.remove("output.csv")


  rowContent = ["Line", "Memory Type", "Address", "Size" , "Name"]
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
        address , size =  GetAddressAndLength(line)
        if (sectionBreakerFound and IsValidAddress(address, size)):
          objectName = GetObjectName(line)
          print("Line: "+ str(x) + " Memory Type " + memoryType + " Address "+ address + " Lenght: " + size + " Object " + objectName )
          rowContent = [x, memoryType, address, size , objectName]
          append_list_as_row('output.csv', rowContent)
        # else:
        #   print("Line: "+ str(x)+ "Warning Invalid Address at !!!!!!!!!!!!!!!!!!!!!!!!!!!!")





      # line = smallSampleFile.readline()
      # initialDot = IsValidLine(line)
      # if initialDot >= 0:
      #   if x == 120:
      #     counterOfLevels = line.count('/')

      #   memoryType, methodDivider = GetMemoryType(initialDot, line)
      #   method = line[methodDivider : line.find(" ", methodDivider)]
        
      #   # method = line[line.find(" ") + len(".text") +1: line.find("0x")]
      #   countOfHexValues = line.count('0x')
        
      #   if countOfHexValues > 1: ## This is the case for when all in same line.
      #     if countOfHexValues > 2:
      #       print("Line: "+ str(x)+ "Warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      #     elif countOfHexValues ==2:
      #       address = line[line.find("0x") :line.find(" ", line.find("0x"))]
      #       length = line[line.rfind("0x") :line.find(" ", line.rfind("0x"))]
      #       fileName = line[line.rfind("/") +1 :line.rfind(".o")]
      #       print("Line: "+ str(x)+ " Memory type: " + memoryType +  " method: "+ method + " Address "+ address + " Lenght: " + length + " File Name: " + fileName)
              # firstHex = line.find("0x")
            
            # print("Line: "+ str(x)+ " Memory type: " + memoryType +  " method: "+ method + " Count of Hex "+ str(countOfHexValues)))
          # else ## Here is the case for when info is in the next line


          # print("Line: "+ str(x)+ " Memory type: " + memoryType +  " method: "+ method + " Count of Hex "+ str(countOfHexValues))
          # print("Line: "+ str(x)+ " Second Dot Position "+ str(secondDot)+ " method: "+ method +"  Number of lelves is " + str(counterOfLevels) + " in " + line.strip())



  print ("Total Processing time is : " + str(datetime.now() - initialTime)) 
  print ("Total analized lines are  : " + str(count)) 


if __name__ == "__main__":
  main();
