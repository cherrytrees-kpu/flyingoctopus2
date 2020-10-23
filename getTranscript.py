from Bio.Seq import Seq
import sqlite3

if __name__ == '__main__':
    
    filename = input('Please enter database name: ')

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
        Consequence IN ('missense_variant', 'inframe_insertion', 'splice_region_variant', 'regulatory_region_variant', 'stop_gained', 'frameshift_variant', 'splice_acceptor_variant', 'splice_donor_variant', 'stop_retained_variant', 'start_lost', 'stop_lost', 'inframe_deletion')
        '''
    )
    
    listData = []

    for row in cursor:
        print (row[3])

    #i = 0
    #for row in cursor:
    #    i = i + 1
    #print(i)

    connection.close()
