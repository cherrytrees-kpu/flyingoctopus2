def outputHGVS(listHGVS, name = ""):
    """
    outputHGVS - outputs a file with the name 'HGVS_*name.txt' containing the
    list of HGVS ids
    Parameters:
    listHGVS - list - contains list ids
    Returns: nothing; outputs to file 'HGVS_*name.txt'

    """
    i = 0

    #Accept name for output file from user
    if name != "":
        name = input('Please enter an identifier for your file: ')
    outputfile = open('HGVS_' + name + '.txt', 'w')

    #Write to file
    while(len(listHGVS)) > i:
        outputfile.write(listHGVS[i])
        if i != (len(listHGVS)-1):
            outputfile.write('\n')
        i = i + 1

    outputfile.close()

def filteraffected(listAffected, listControl):
    """
    filteraffected - filters from lists of HGVS IDs of affected and control
                     individuals
    Parameters:
    listaffected - list - contains the list of HGVS ids of affected individuals
    listcontrol - list - contains the list of HGVS ids of unaffected individuals
    Returns: list containing candidate mutations only
    """
    i = 0
    listFiltered = []

    print('Filtering starting...')

    while i < len(listAffected[0]):
        candidate = True

        #Check if HGVS is in all listAffected. If not, set candidate to false
        for a in listAffected:
            if (listAffected[0][i] in a) == False:
                candidate = False

        #Check if HGVS is in listControl. If yes, set candidate to False
        for c in listControl:
            if listAffected[0][i] in c:
                candidate = False

        #Write to file
        if candidate == True:
            listFiltered.append(listAffected[0][i].strip('\n'))

        if i%1000 == 0:
            print(str(i) + '/' + str(len(listAffected[0])) + ' completed...')

        i = i + 1

    print('Filtering completed.')
    return listFiltered

if __name__ == '__main__': 

    listAffected = []
    listControl = []
    listFiltered = []

    numFiles = int(input('Number of individuals: '))

    for i in range(numFiles):
        #Open file 
        filename = input('Please enter the name of the file listing HGVS IDs to be imported: ')
        inputFile = open(filename, 'r')
        #Define file as affected or control
        cat = input('Enter "a" for affected, "c" for control')
        #Import list
        listHGVS = []
        for line in inputFile:
            listHGVS.append(line.strip('\n'))
        #Append list to correct list
        if cat == 'a':
            listAffected.append(listHGVS)
        else: 
            listControl.append(listHGVS)

    listFiltered = filteraffected(listAffected, listControl)

    outputHGVS(listFiltered, "candidate")