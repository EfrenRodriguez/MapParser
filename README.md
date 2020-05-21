# MapParser
Learning Project To Parse a Map File into a Json

Build in Pyton 3 

## Inputs
You need to provide the following inputs
   - configuration.json - See example [here](https://github.com/EfrenRodriguez/MapParser/blob/master/Configuration/configuration.json)
      - You should provide the mapFile name to parse
      - Here you can specify "alias" to rename section names.
      - Also you can specifiy sections to ignore.


## Outputs
The scrip will provide you with 3 output files
   - output.csv This file includes every single object analized
      - The line where it was found
      - The memory type
      - Base address
      - Size in decimal
      - Object name
      - Object Path
   - summary.csv This file provdes a summary by object here you can find
      - Memory type
      - Object name
      - Total object size in bytes
   - summary.json. Similar information than summary.csv but in json format.

Created By Efren Rodriguez. 
