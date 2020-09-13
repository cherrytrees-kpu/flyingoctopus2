import requests
import json
import time
import sys

def importHGVS(filename):
    
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

    return listHGVS

def exportanno(listanno, filename):
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
        outputfile.write(json.dumps(anno))
        #Check to see if the last element has been reached before entering a
        #newline character
        if listanno.index(anno) != (len(listanno)-1):
            outputfile.write('\n')
    outputfile.close()
    print('Export completed.' + '\n')

def annotateVEP(listHGVS):
    """
    annotateVEP - from a list of HGVS IDs, retrieve all VEP annotations
    Paramters:
    listHGVS - list - list of HGVS ids
    Return: a list of dictionaries of VEP data
    """
    #Processing time tracker
    start = time.time()

    #indexes for list traversal
    i = 0
    u = 200

    #VEP REST API
    server = "http://grch37.rest.ensembl.org"
    ext = "/vep/human/hgvs"
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    parameters = {"canonical":"1", "uniprot":"1"}

    #listvep - will store all of the data
    listvep = []

    #Annotation process
    print('Initiating annotation...')
    while i < len(listHGVS):

        #Retrieve 200 HGVS IDs - maximum for the batch query to the VEP REST API
        if u != (len(listHGVS) - 1):
            rangeHGVS = listHGVS[i:u]
        if u == (len(listHGVS) - 1):
            rangeHGVS = listHGVS[i:]
        p_rangeHGVS = str(rangeHGVS).replace("'", '"')

        #Retrieval of data from VEP REST API
        r = requests.post(server+ext, headers=headers, data=('{ "hgvs_notations" : ' + p_rangeHGVS + ' }'), params = parameters)

        #Error handling
        if not r.ok:
            r.raise_for_status()
            sys.exit()

        #Store as list of dictionaries
        decoded = r.json()

        #Check for missing annotations
        if len(rangeHGVS) != len(decoded):
            print(str(len(rangeHGVS)
                    - len(decoded))
                    + ' annotations are missing')
            try:
                q = 0
                for idHGVS in rangeHGVS:
                    if rangeHGVS.index(idHGVS) < len(decoded):
                        if idHGVS != decoded[q]['id']:
                            decoded.insert(rangeHGVS.index(idHGVS), None)
                        q = q + 1

                    if rangeHGVS.index(idHGVS) >= len(decoded):
                        decoded.append(None)
            except:
                print('Issue between '
                        + str(rangeHGVS[0])
                        + 'and '
                        + str(rangeHGVS[len(rangeHGVS)-1]))
                print(len(decoded))

        #Add these results to annot list
        for anno in decoded:
            listvep.append(anno)

        print (str(u) + ' out of ' + str(len(listHGVS)) + ' completed...')

        i = i + 200
        u = u + 200

        if u > len(listHGVS):
            u = len(listHGVS) - 1

    #Processing time tracker
    end = time.time()
    print('Processing time: ' + str(end - start))

    return listvep

if __name__ == "__main__":
    filename = input('Please enter HGVS filename: ')
    listHGVS = importHGVS(filename)
    
    listVEP = annotateVEP(listHGVS)

    exportanno(listVEP, 'vep_annotation')