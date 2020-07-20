#script translates CAN raw gates to human and puts them in db
import sys
import numpy as np
import json
from datetime import date, time, datetime

# "constatnt" variables used for printing result 
CELS = str("\u00b0C")  #sign for Celsius degrees
PERC = str("%")        #sign for humidity

def obtainMeasurement():
    dataS = sys.stdin.readline()
    print(dataS)
    
    dataL = dataS.split()
    #print(dataL)
    
    #extract data to human format
    canDate = dataL[0][1:]
    canTime = dataL[1][:-1]
    canId = int(dataL[3], 16) << 3
    canLen = int(dataL[4][1:-1])
    
    #measurements (last 6 bytes) as bytearray()
    canData= bytearray()
    for i in range(5, 5+canLen):
        canData.append(int(dataL[i], 16))
    print(canData)
    
    #measurements split to list and represented binarily
    measurement = " ".join(format(x, "08b") for x in canData)
    print(measurement)
    measurementSplit = measurement.split(" ")
    print(measurementSplit)

    #calculate Temperature
    tempHB = measurementSplit[2] #hard-coded position of temp(H)igh (B)its
    tempLB = measurementSplit[3]  #hard-coded posiotion of temp(L)ow (B)its
    tempWholeB = tempHB + tempLB
    temperature = int(tempWholeB,2)/100.0
    print(str(temperature) + CELS)
    
    #calculate Humidity
    humHB = measurementSplit[4]
    humLB = measurementSplit[5]
    humWholeB = humHB + humLB
    humidity = int(humWholeB,2)/100.
    print(str(humidity) + PERC)

    datetime_str = canDate + " " + canTime

    #pack to dict, then dump as json
    dataDict = {
            "datetime": datetime_str,
            "time": {
                "timeStamp": canTime,
                "dateStamp": canDate
                },
            "frameId": canId, 
            "temp": temperature,
            "hum": humidity
            }
    return dataDict



while 1:
    measurementDict = obtainMeasurement()
    measurementJson = json.dumps(measurementDict)
    print(measurementJson)

    # canDate2 = "2020-07-20"

    # d = date.fromisoformat(canDate2)
    # print("Datetime: " + str(d))
    # print(type(d))
    
    #print("Hello:" + " ".join(format(x, "02x") for x in dataB) + '\n' + "type(dataB):" + str(type(dataB)))
    
    
