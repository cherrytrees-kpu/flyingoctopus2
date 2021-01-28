import myvariant
import vcf
import json

def getHGVS(filename):
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
            print('HGVS loaded.')
        except IOError:
            print('File not found.\n')
            filename = input('Re-enter filename: ')
    return listHGVS

def get(filename): 
    listvcf = []
    vcf_reader = vcf.Reader(open(filename, 'r'))

    for record in vcf_reader:
        listvcf.append(record)
    return listvcf

def output(listitem, filename):
    """
    exportanno - exports raw annotation data
    Parameters:
    listanno - list - list of dictionaries containing raw JSON data
    filename - string - name of the file to output to
    Returns: none; outputs to file with filename
    """
    #Create output file
    outputfile = open(filename, 'w')

    #For each annotation in the annotation list, dump the JSON data to file
    for item in listitem:
        outputfile.write(json.dumps(item, sort_keys=True))
        #Check to see if the last element has been reached before entering a
        #newline character
        if listitem.index(item) != (len(listitem)-1):
            outputfile.write('\n')
    outputfile.close()
    print('Export completed.' + '\n')
    
if __name__ == '__main__': 
    print ('This script will output three files: ')
    identifier = input('Please enter a job identifier: ')
    filename = input('Please enter filename: ')

    listHGVS = getHGVS(filename)
    listvcf = get(filename)
    listall = []

    for hgvs in listHGVS: 
        listall.append([hgvs, listvcf[listHGVS.index(hgvs)]])
    
    output(listHGVS, identifier + '_hgvs.txt')
    output(listvcf, identifier + '_vcf.txt')
    output(listall, identifier + '_all')