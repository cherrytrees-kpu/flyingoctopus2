"""

mvi.py - code for processing data from myvariant.info

"""
#Import modules
import myvariant
import requests

#Function definitions
def annotateMVI(HGVS):
    """
    annotmvi - accepts HGVS, returns data on mutation
    Parameters: listHGVS: list of HGVS IDs to retrieve annotations for
    Return: dictionary/list containing the json data from myvariant.info. Returns none if no entry is found.
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

    return annoMVI

#Function definitions
def annotateHPA(geneid):
    """
    annothpa - pulls expression data from the Human Protein Atlas
    Parameters: geneid - Ensembl gene id
    Returns: returns expression data
    """
    #expression - list that holds the return data from

    server = "http://www.proteinatlas.org/"

    try:
        r = requests.get(server + geneid + '.json', timeout=20)
    except requests.exceptions.ConnectionError:
        print('ConnectionError')
        try:
            r = requests.get(server + geneid + '.json', timeout=20)
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