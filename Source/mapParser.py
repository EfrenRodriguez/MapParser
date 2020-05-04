from datetime import datetime
from datetime import timedelta

def main():
  initialTime = datetime.now()
  
  smallSampleFile = open("MapFiles/smallSampleFile.map", "r")

  if smallSampleFile.mode == 'r':
    contents = smallSampleFile.read()
    print(contents)
  # fl = f.readlines()
  # for x in fl :
  #   print(x)



  print ("Total Processing time is : " + str(datetime.now() - initialTime))


if __name__ == "__main__":
  main();
