
def readSPI (channel):  #Capture the data from the max31855 SPI device
  #open the datastream
  f = open('/dev/spidev0.'+str(channel),'r')
  #capture the data
  rawCapture=f.read(4)
  #close the datastream
  f.close()
  rawData=int(rawCapture.encode("hex"),16)
  return rawData;

def readErrors (rawData):
  #grab error data discard everything else
  errorData=rawData & 0x7
  #read each error bit into variable for later use
  ocBit=errorData & 0x1
  errorData=errorData >> 1
  scgBit=errorData & 0x1
  errorData=errorData >> 1
  scvBit=errorData & 0x1
  #look for error flag
  rawData = rawData >> 16
  errorFlag=rawData & 0x1
  #if error, which bit? and raise exception
  if errorFlag == 1:
    if ocBit == 1:
      raise StandardError("The thermocouple is not detected")
    elif scgBit == 1:
      raise StandardError("The thermocouple is shorted to ground")
    elif scvBit == 1:
      raise StandardError("The thermocouple is shorted to power")
  return

def readInternal (rawData):  #get internal temp
  #strip off error Data
  rawData = rawData >> 4
  internalData=rawData & 0x7FF
  internalTemp = internalData * 0.0625
  #check sign
  b=rawData & 0x800 
  if b == 1:
    internalTemp = internalTemp * -1
  return internalTemp; 

def readExternal (rawData): #get External Temp Data
  #strip off error data and  internal temp 
  rawData = rawData >> 18
  externalData=rawData & 0x3FFF
  externalTemp=externalData * .25
  c=rawData & 0x20000
  if c == 1:
    externalTemp = externalTemp * -1
  return externalTemp;

def convertCtoF (tempData): #simple conversion to return Farenheit
  fTemp=((tempData * 9)/5)+ 32
  return fTemp

#start of program
def getExternal(channel):
  rawData=readSPI(channel) # Get Data from channel variable
  readErrors(rawData)#check for any errors
  externalTemp=readExternal(rawData) #Crunch Data for External temp
  fTemp=convertCtoF(externalTemp)
  return fTemp

def getInternal(channel):

  rawData=readSPI(channel) # Get Data from channel variable
  readErrors(rawData)#check for any errors
  internalTemp=readInternal(rawData) #Crunch Data for Internal temp
  fTemp=convertCtoF(internalTemp)
  return fTemp
