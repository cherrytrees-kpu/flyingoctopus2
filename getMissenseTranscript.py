from Bio.Seq import Seq
import sqlite3
import requests

def getsequence(transcriptid):
    server = 'https://grch37.rest.ensembl.org'
    ext = '/sequence/id/' + transcriptid + '?'

    xheaders={'Content-Type':'application/json'}
    xparams = {'type':'protein','object_type':'transcript'}

    r = requests.get(server+ext, headers=xheaders, params=xparams)

    if r.status_code == 200:
        return r.json()['seq']
    else:
        print('protein for ' + transcriptid + ' could not be found.')
        print(r.status_code)
        return None

if __name__ == '__main__':
    
    #filename = input('Please enter database name: ')
    filename = 'family_D.db'

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()

    cursor.execute(
        '''
        SELECT * FROM Transcripts WHERE
        HGVS IN
        (
        SELECT HGVS From GeneralInformation WHERE
        MostSevereConsequence IN ('missense_variant', 'inframe_insertion', 'splice_region_variant', 'regulatory_region_variant', 'stop_gained', 'frameshift_variant', 'splice_acceptor_variant', 'splice_donor_variant', 'stop_retained_variant', 'start_lost', 'stop_lost', 'inframe_deletion')
        AND (gnomADE < 0.001 OR gnomADG < 0.001 OR (gnomADG IS NULL AND gnomADE IS NULL))
        )
        AND
        Canonical = 1
        AND
        Consequence IN ('missense_variant')
        '''
    )
    
    listData = []
    listProtein = []

    #Pull data
    for row in cursor:
        #HGVS, Gene, EnsemblTranscript, Protein Start, Protein End, Amino Acids
        listData.append((row[0], row[1], row[3], row[11], row[12], row[13]))

    #Get Transcript
    for transcript in listData: 
        protein = getsequence(transcript[2])
        listProtein.append(protein)
    
    outputfile = open('output.txt', 'w')

    print ('All transcripts downloaded')

    i = 0

    print ('Outputting file...')

    while i < len(listData): 
        aa = listData[i][5].split('/')
        outputfile.write(
            '>'
            + listData[i][0]
            + '_'
            + listData[i][1]
            + ' '
            + aa[0]
            + str(listData[i][3])
            + aa[1]
            + '\n'
            )
        outputfile.write(listProtein[i] + '\n')
        i = i + 1
    
    outputfile.close()


    #print(len(listData))
    #print(listData[17][0])
    #print(listData[19][0])

    #i = 0
    #for row in cursor:
    #    i = i + 1
    #print(i)

    connection.close()
