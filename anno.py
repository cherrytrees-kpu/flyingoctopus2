"""

anno.py - code for dealing with annotation text files

"""

import json

def get(filename):
    """
    importanno - from a file containing json.dumps annotation data, import it as
    a list of dictionaries
    Parameters: filename - name of file to open
    Return: a list of dictionaries of annotation data
    """

    inputfile_open = False
    listdata = []

    if filename == "": 
        filename = input("Please enter filename: ")

    #Open the file
    while inputfile_open == False:
        try:
            inputfile = open(filename, 'r')
            inputfile_open = True
        except IOError:
            print('File not found.\n')
            filename = input('Re-enter filename: ')
    #Import the data
    for line in inputfile:
        listdata.append(json.loads(line))
    #Export data
    inputfile.close()
    return listdata

def output(listanno, filename):
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
    for anno in listanno:
        outputfile.write(json.dumps(anno, sort_keys=True))
        #Check to see if the last element has been reached before entering a
        #newline character
        if listanno.index(anno) != (len(listanno)-1):
            outputfile.write('\n')
    outputfile.close()
    print('Export completed.' + '\n')

def gene(anno):

    listGenes = []

    if 'transcript_consequences' in anno:
        for transcript in anno['transcript_consequences']:
            gene = (transcript['gene_id'], transcript['gene_symbol'])
        if gene not in listGenes:
            listGenes.append(gene)
        return listGenes
    else: 
        return None

def combine():
    def vartype(idHGVS):
        """
        dumpvartype - determine the type of variant based on HGVS id
        Parameters: idHGVS - the HGVS id of variant being considered
        Return: vartype
        """
        vartype = ''
        if '>' in idHGVS:
            vartype = 'snv'
        elif 'del' in idHGVS:
            vartype = 'del'
        elif 'ins' in idHGVS:
            vartype = 'ins'
        return vartype
    anno = []

    #Import MVI file
    mviName = input("MVI filepath: ")
    vepName = input("VEP filepath: ")

    #Get list of annotations for both
    mvi = get(mviName)
    vep = get(vepName)

    if len(vep) == len(mvi): 
        print("Annotations being combined....")
        i = 0
        while i < len(mvi): 
            if mvi[i]['_id'] == vep[i]['id']:
                data = {'_id': mvi[i]['_id'],'mvi': mvi[i], 'vep':vep[i], 'vartype':vartype(mvi[i]['_id'])}
                anno.append(data)
            else: 
                print("Error: non-matching ID")
                print("MVI: " + mvi[i]['_id'])
                print("VEP: " + vep[i]['id'])
                print("Index " + str(i))
                i = len(mvi)
            i = i + 1
    else: 
        print("Error: different numbers of annotations in both files.")

    return anno