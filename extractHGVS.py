import myvariant

def vcftoHGVS(filename):
    """
    vcftoHGVS - calls the myvariant.info get_hgvs_from_vcf function
    Parameters: None
    Returns: none; outputs a file containing all of the HGVS IDs
    """
    listHGVS = []

    inputfile_open = False

    while inputfile_open == False:
        try:
            listHGVS = list(myvariant.get_hgvs_from_vcf(filename))
            inputfile_open = True
        except IOError:
            print('File not found.\n')
            filename = input('Re-enter filename: ')

    #Accept name input from user
    name = input('Please enter an identifier for your file: ')
    outputfile = open('HGVS_' + name + '.txt', 'w')

    #Write to file
    print('Writing to file...')
    #for idHGVS in listHGVS:
    length = len(listHGVS)
    i = 0
    while i < (length - 1):
        outputfile.write(listHGVS[i])
        outputfile.write ('\n')
        i = i + 1
    outputfile.write(listHGVS[i])
    print('Done.')

    outputfile.close()

if __name__ == '__main__': 
    filename = input('Please enter filename: ')
    vcftoHGVS(filename)