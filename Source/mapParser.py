from datetime import datetime
from datetime import timedelta

def IsValidLine(myLine):
  initialDot = 0
  for x in myLine:
    if x != " ":
      if x == ".":
        return initialDot
      else:
        return -1
    initialDot = initialDot + 1

def GetMemoryType(initialDot, myLine):
  dot = myLine.find(".",initialDot + 1, len(myLine)-1)
  space = myLine.find(" ",initialDot + 1, len(myLine)-1)
  lastCharacter = 0
  memoryType = ""
  if dot < space:
    if dot > 0:
      lastCharacter = dot
      memoryType = myLine[initialDot + 1: lastCharacter]
    else:
      lastCharacter = space 
      memoryType = myLine[initialDot + 1: lastCharacter]
  elif space > 0:
    lastCharacter = space 
    memoryType = myLine[initialDot + 1: lastCharacter]
 
  return memoryType, lastCharacter + 1


def main():
  initialTime = datetime.now()
  
  smallSampleFile = open("MapFiles/smallSampleFile.map", "r")

  if smallSampleFile.mode == 'r':
    # contents = smallSampleFile.read()
    # print(contents)
    # fl = smallSampleFile.readlines()
    for x in range(0,200) :
      line = smallSampleFile.readline()
      initialDot = IsValidLine(line)
      if initialDot >= 0:
        if x == 120:
          counterOfLevels = line.count('/')

        memoryType, methodDivider = GetMemoryType(initialDot, line)
        method = line[methodDivider : line.find(" ", methodDivider)]
        
        # method = line[line.find(" ") + len(".text") +1: line.find("0x")]
        countOfHexValues = line.count('0x')
        
        if countOfHexValues > 1: ## This is the case for when all in same line.
          if countOfHexValues > 2:
            print("Line: "+ str(x)+ "Warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
          elif countOfHexValues ==2:
            address = line[line.find("0x") :line.find(" ", line.find("0x"))]
            length = line[line.rfind("0x") :line.find(" ", line.rfind("0x"))]
            fileName = line[line.rfind("/") +1 :line.rfind(".o")]
            print("Line: "+ str(x)+ " Memory type: " + memoryType +  " method: "+ method + " Address "+ address + " Lenght: " + length + " File Name: " + fileName)
              # firstHex = line.find("0x")
            
            # print("Line: "+ str(x)+ " Memory type: " + memoryType +  " method: "+ method + " Count of Hex "+ str(countOfHexValues)))
          # else ## Here is the case for when info is in the next line


          # print("Line: "+ str(x)+ " Memory type: " + memoryType +  " method: "+ method + " Count of Hex "+ str(countOfHexValues))
          # print("Line: "+ str(x)+ " Second Dot Position "+ str(secondDot)+ " method: "+ method +"  Number of lelves is " + str(counterOfLevels) + " in " + line.strip())



  print ("Total Processing time is : " + str(datetime.now() - initialTime))


if __name__ == "__main__":
  main();
