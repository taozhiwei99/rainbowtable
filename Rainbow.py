#import the libaries
from hashlib import md5
import sys

#read file
inFile = sys.argv[1]

#global variable
usedPass = []

#function to read file
def getFile(file):
    global lineCount
    global plaintext
    plaintext = []
    lineCount = 0
    try:
        with open(file, 'r') as file:
            for line in file:
                lineCount = lineCount + 1
                plaintext.append(line.strip())
            file.close()
            return lineCount
    except Exception as e:
        print(f'Failed to open : {e}')
        exit(1)

#hash function
def hash(password):
    h = ""
    h = md5(password.encode("utf-8")).hexdigest()
    return h

#reduction function
def reduction(hexDec):
    reduc = 0
    tempNo = int(hexDec,16)
    reduc = tempNo % lineCount
    return reduc

#check if pass marked or not
def iswordUsed(password):
    if password in usedPass:
        return True
    else:
        return False

#hash-list for md5
def rainbow():
    #list for rainbow table
    global rainbowTable
    rainbowTable = []  
    #temp holder
    tempPass = []
    tempHash = []
    #loop tru all the password
    for word in plaintext:
        #conditon to check if pass used
        if not iswordUsed(word):
            usedPass.append(word)  #if un-used, marked it
            tempPass.append(word)  #put curret pass into temp holder 
            tempHash.append(hash(word))
            tempNo = hash(word)
            tempIndex = reduction(tempNo)  #get the reduction value
            
            loopCounter = 0
            while loopCounter != 4:  #inner for loop to repeat 4 times for the next 4 value
                usedPass.append(plaintext[tempIndex])
                tempPass.append(plaintext[tempIndex])
                tempHash.append(hash(tempPass[loopCounter+1]))
                tempNo2 = hash(tempPass[loopCounter+1])
                tempIndex = reduction(tempNo2)
                loopCounter += 1
            #once exist while loop, append to rainbow lists
            a = tempPass[0]
            b = tempHash[4]
            rainbowTable.append([a,b])
            tempPass.clear() #clear the temp holder for next pass loop
            tempHash.clear()
    rainbowTable = sorted(rainbowTable, key=lambda x:x[1])  #sort rainbow table

#write to rainbow text
def writeTo():
    with open ("Rainbow.txt" , "w") as f:
        header = "{:<14} : {:>19}\n".format("Password","Hash")
        f.write(header)
        lineWrote = 0
        for sublist in rainbowTable:
            line = "{:<14} : {:>12}\n".format(sublist[0], sublist[1])
            f.write(line)
            lineWrote+=1
        print("Total lines wrote:",lineWrote)
    f.close()
    
#function to get and validate hash enter by user
def getInput():
    global user_input
    user_input = ""
    while True:
        user_input = input("Please enter a hash: ")
        inputCount = len(user_input)
        if inputCount != 32:
            print("Wrong hash, try again.")
            continue
        else:
            break

#compare two variables
def compare(aHash, value):
    if aHash == value:
        return True
    else:
        return False

#function to find pre-image password
def findPass():
    findHash = user_input
    finalPass = ""

    #loop rainbow table to find a match
    for i in rainbowTable:
        if findHash == i[1]: #if input match a rainbow row
            tempPass = i[0]
            tempHash = hash(tempPass)
            #if this is same as input output original pass
            if compare(tempHash,findHash):
                finalPass = tempPass
                return finalPass
    
            else:
                #reduction loop
                for k in range(0,4):
                    tempPass = plaintext[reduction(tempHash)]
                    tempHash = hash(tempPass)
                    if compare(tempHash, findHash):
                        finalPass = tempPass
                        return finalPass
                                
        else:
            #if input not found in rainbow table
            #perform reduction 
            tempPass = plaintext[reduction(findHash)]
            tempHash = hash(tempPass)
            if tempHash == i[1]:
                tempPass = i[0]
                tempHash = hash(tempPass)
                if compare(tempHash, findHash):
                    finalPass = tempPass
                    return finalPass
    
                else:
                    for n in range(0,4):
                        tempPass = plaintext[reduction(tempHash)]
                        tempHash = hash(tempPass)
                        if compare(tempHash, findHash):
                            finalPass = tempPass
                            return finalPass
                                    
            else:
                for o in range(0,4):
                    tempPass = plaintext[reduction(tempHash)]
                    tempHash = hash(tempPass)
                    if tempHash == i[1]:
                        tempPass = i[0]
                        tempHash = hash(tempPass)
                        if compare(tempHash, findHash):
                            finalPass = tempPass
                            return finalPass
    
                        else:
                            for q in range(0,4):
                                tempPass = plaintext[reduction(tempHash)]
                                tempHash = hash(tempPass)
                                if compare(tempHash,findHash):
                                    finalPass = tempPass
                                    return finalPass
                                
    #return error message, if nothing is found
    errormsg = "Nothing found, something might be wrong with your hash!"
    return errormsg

#main function
def run():
    print("Total words read:",getFile(inFile))
    rainbow()
    writeTo()
    getInput()
    print("Pre-Image is :",findPass())

def main():
    run()
    
if __name__ == '__main__':
    main()