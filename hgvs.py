def convert(idHGVS):
    """
    converthgvs - convert a HGVS ID into a format that can be used in a filename
    or directory
    Parameters: idHGVS - the HGVS ID as a string
    Return: a string with the converted HGVS ID
    """
    def findchr(idHGVS):
        if idHGVS[3:5].isnumeric() is True:
            return idHGVS[3:5]
        else:
            return idHGVS[3]
    def findpos(idHGVS, marker):
        pos_start = idHGVS.index(marker) + 1
        pos_end = pos_start + 1
        pos_complete = False

        while pos_complete is False:
            if idHGVS[pos_start:pos_end].isnumeric() is False:
                pos_chr = idHGVS[pos_start:(pos_end-1)]
                pos_complete = True
            else:
                pos_end = pos_end + 1
        return pos_chr
    #For substitution
    if '>' in idHGVS:
        #Identify chromosome number
        num_chr = findchr(idHGVS)
        #Identify position
        pos_chr = findpos(idHGVS, '.')
        #Identify allele 1 and 2
        allele1 = idHGVS[idHGVS.index('>') - 1]
        allele2 = idHGVS[idHGVS.index('>') + 1]
        return (num_chr + '-' + pos_chr + '-' + allele1 + '-' + allele2)

    #For deletion and insertion
    elif 'delins' in idHGVS:
        #Identify chromosome numbers
        num_chr = findchr(idHGVS)
        #Identify position
        pos_chr = findpos(idHGVS, '.')
        #Identify inserted sequence
        seq_delins = idHGVS[idHGVS.index('s') + 1:]
        #Debug
        return(num_chr + '-' + pos_chr + '-delins-' + seq_delins)

    #For deletion
    elif 'del' in idHGVS:
        #Identify chromosome number
        num_chr = findchr(idHGVS)
        #Identify position 1
        if '_' in idHGVS:
            pos1_chr = idHGVS[(idHGVS.index('.') + 1):idHGVS.index('_')]
            #Identify position 2
            pos2_chr = findpos(idHGVS, '_')
            return (num_chr + '-' + str(pos1_chr) + '_' + str(pos2_chr) + '-del')
        else:
            pos_chr = findpos(idHGVS, '.')
            return (num_chr + '-' + str(pos_chr) + '-del')

    #For insertion
    elif 'ins' in idHGVS:
        #Identify chromosome number
        num_chr = findchr(idHGVS)
        #Identify positions
        pos1_chr = idHGVS[(idHGVS.index('.') + 1):idHGVS.index('_')]
        pos2_chr = findpos(idHGVS, '_')
        #Identify inserted sequences
        seq_ins = idHGVS[idHGVS.index('s') + 1:]
        return (num_chr + '-' + str(pos1_chr) + '_' + str(pos2_chr) + '-ins' + seq_ins)

def output(listHGVS, name = ""):
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

def get(filename):
    """
    importHGVS - imports HGVS into the program
    Parameters: none
    Return: list containing the imported HGVS ids
    """

    inputfile_open = False
    listHGVS = []

    #Open the file
    while inputfile_open == False:
        try:
            inputfile = open(filename, 'r')
            inputfile_open = True
        except IOError:
            print('File not found.\n')

            filename = input('Re-enter filename: ')

    #Import data into listHGVS
    for line in inputfile:
        listHGVS.append(line.strip('\n'))

    inputfile.close()