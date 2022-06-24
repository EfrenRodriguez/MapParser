from datetime import datetime
from datetime import timedelta
import csv
import os
import json
from collections import defaultdict

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

def GetMemoryName(rawMemoryType, myJsonConfigurationData):
  memoryName = rawMemoryType
  for i in myJsonConfigurationData["aliasConfiguration"]:
    if i["name"] == rawMemoryType:
      memoryName = i["alias"]
      break
  return memoryName

def WantToDisplayMemoryTypeName(memoryType, myJsonConfigurationData):
  for i in myJsonConfigurationData["ignoreConfiguration"]:
    if i["ignore"] == memoryType:
      return False
  return True

def GetMemoryType(myLine, myJsonConfigurationData):
  memoryType = myLine[myLine.find(".") + 1 :myLine.find(" ")]
  memoryType = GetMemoryName(memoryType, myJsonConfigurationData)
  return memoryType

def GetFolderName(myLine):
  levels = myLine.count('/')
  folderName = " "
  array = [ ]
  if (levels >= 2):
    lastDivider = myLine.rfind("/")
    initialDivider = myLine.find("/")
    initial = myLine.rfind(" ")

    for x in range(0, levels):
      array.append(myLine[initial + 1 :initialDivider])
      initial = initialDivider
      initialDivider = myLine.find("/",initial +1)

    otherDivider = myLine.rfind("/",0, lastDivider)
    folderName = myLine[otherDivider + 1 :lastDivider]
  return folderName , array

def GetObjectName(myLine):
  dividerLocation = myLine.rfind("/")
  par = myLine.rfind("(")
  fill = myLine.count('*fill*')
  folderName ,path = GetFolderName(myLine)
  if (fill > 0):
    objectName = "Padding"
  elif (dividerLocation < par):
    objectName = myLine[par + 1 :myLine.rfind(".")]
  else:
    objectName = myLine[dividerLocation + 1 :myLine.rfind(".")]

  return objectName, folderName, path

def append_list_as_row(fileName, listOfElem):
    with open(fileName, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(listOfElem)

def IsValidObjectName(myObjectName):
  countOfHexValues = myObjectName.count('0x')
  if(countOfHexValues > 1):
    return False
  return True

def ExportSummaryToCsv(myDictionary):
  topLevelKeys = list(myDictionary.keys())
  lowLevelKeys = list(myDictionary[topLevelKeys[0]].keys())

  if os.path.exists("Outputs/summary.csv"):
    os.remove("Outputs/summary.csv")

  rowContent = ["Memory Type", "Name", "Size"]
  append_list_as_row('Outputs/summary.csv', rowContent)

  for i in range(topLevelKeys.__len__()):
    lowLevelKeys = list(myDictionary[topLevelKeys[i]].keys())
    for j in range (lowLevelKeys.__len__()):
      rowContent = [topLevelKeys[i], lowLevelKeys[j], myDictionary[topLevelKeys[i]] [lowLevelKeys[j]] ]
      append_list_as_row('Outputs/summary.csv', rowContent)

def ExportSummaryToJson(myDictionary):
  jsonOutput = json.dumps(myDictionary, indent=4)

  with open ("Outputs/summary.json", "w") as outfile:
    outfile.write(jsonOutput)


def main():

  initialTime = datetime.now()

  with open('Configuration/configuration.json') as json_file:
    theJsonConfigurationData = json.load(json_file)

  inputFile = theJsonConfigurationData["inputFile"]

  mapFileToParse = open(inputFile, "r")
  count = len(open(inputFile).readlines(  ))

  if os.path.exists("Outputs/output.csv"):
    os.remove("Outputs/output.csv")

  if not os.path.exists("Outputs"):
    os.makedirs("Outputs")


  rowContent = ["Line", "Memory Type", "Address", "Size" , "Name", "Folder Name", "Path1", "Path 2", "Path 3"]
  append_list_as_row('Outputs/output.csv', rowContent)

  directory = defaultdict(lambda: defaultdict(int))


  if mapFileToParse.mode == 'r':
    sectionBreakerFound = False
    for x in range(0,count) :
      line = mapFileToParse.readline()
      if (IsSectionBreaker(line)):
        sectionBreakerFound = True
        memoryType = GetMemoryType(line, theJsonConfigurationData)
      else:
        address , sizeHex =  GetAddressAndLength(line)
        if (sectionBreakerFound and IsValidAddress(address, sizeHex)):
          objectName , folderName, path = GetObjectName(line)
          size = int(sizeHex,0)
          if (IsValidObjectName(objectName) and WantToDisplayMemoryTypeName(memoryType, theJsonConfigurationData)):
            rowContent = [x, memoryType, address, size , objectName, folderName]
            pathLen = len(path)
            for x in range(0, pathLen):
              rowContent.append(path[pathLen -1 - x])
            append_list_as_row('Outputs/output.csv', rowContent)
            directory[str(memoryType)][str(objectName)] += size

  ExportSummaryToCsv(directory)
  ExportSummaryToJson(directory)

  print ("Total Processing time is : " + str(datetime.now() - initialTime))
  print ("Total analized lines are  : " + str(count))


if __name__ == "__main__":
  main();
