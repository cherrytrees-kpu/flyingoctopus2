"""

annotation.py - code for accession of databases

"""
#Import modules
import myvariant
import requests
import sys
import json
import time

#Function definitions
def MVI(HGVS):
    """
    MVI - accepts HGVS, returns data on mutation
    Parameters: HGVS - HGVS ID
    Return: dictionary containing the json data from myvariant.info. Returns a dictionary with just the HGVS ID if myvariant.info returns None
    """
    mv = myvariant.MyVariantInfo()

    #For each HGVS ID in the list, retrieve the annotation
    annoMVI = mv.getvariant(HGVS, fields = [
        'cadd', 
        'clinvar',
        'dbnsfp',
        'dbsnp',
        'gnomad_exome',
        'gnomad_genome',
        ])

    if annoMVI is None:
        dict = {'_id': HGVS}
        return dict
    else:
        return annoMVI

def HPA(geneID):
    """
    HPA - pulls expression data from the Human Protein Atlas
    Parameters: geneID - Ensembl gene id
    Returns: returns expression data as a dictionary
    """
    #expression - list that holds the return data from

    server = "http://www.proteinatlas.org/"

    try:
        r = requests.get(server + geneID + '.json', timeout=20)
    except requests.exceptions.ConnectionError:
        print('ConnectionError')
        try:
            r = requests.get(server + geneID + '.json', timeout=20)
        except requests.exceptions.ConnectionError:
            print('Connection Error again')
            return "connectionError"
        else: 
            return r.json()
    except requests.exceptions.TooManyRedirects:
        print('Too Many Redirects')
        return 'tooManyRedirects'
    else:
        return r.json()

def VEP(listHGVS):
    """
    VEP - from a list of HGVS IDs, retrieve all VEP annotations
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