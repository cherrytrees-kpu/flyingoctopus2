import sqlite3
import anno

#Database access
connection = sqlite3.connect('family_M.db')
cursor = connection.cursor()

#Import annotations
annoList = anno.get("")

#Write to table
for variant in annoList: 
    #HGVS, vartype --> root
    #RSID, gnomADE, gnomADG --> mvi
    #Gene, EnsemblGene --> vep
    #Default fields
    hgvs = variant['_id']
    vartype = variant['vartype']
    rsid = None
    msc = None
    gnomADE = None
    gnomADG = None

    try: 
        #MVI
        if 'dbsnp' in variant['mvi']:
            rsid = variant['mvi']['dbsnp']['rsid']
        if 'gnomad_exome' in variant['mvi'] and 'af' in variant['mvi']['gnomad_exome']['af']:
            gnomADE = variant['mvi']['gnomad_exome']['af']['af']
        if 'gnomad_genome' in variant['mvi'] and 'af' in variant['mvi']['gnomad_genome']['af']:
            gnomADG = variant['mvi']['gnomad_genome']['af']['af']
        #VEP 
        genes = anno.gene(variant['vep'])
        msc = variant['vep']['most_severe_consequence']
    except: 
        print(variant['_id'])

    if genes is None:
        #Create tuple
        data = (hgvs, rsid, vartype, msc, gnomADE, gnomADG, None, None)
        cursor.execute('INSERT INTO GeneralInformation(HGVS, RSID, VarType, MostSevereConsequence, gnomADE, gnomADG, Gene, EnsemblGene) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)
        connection.commit() 
    else: 
        for gene in genes: 
            #Create tuple
            data = (hgvs, rsid, vartype, msc, gnomADE, gnomADG, gene[0], gene[1])
            cursor.execute('INSERT INTO GeneralInformation(HGVS, RSID, VarType, MostSevereConsequence, gnomADE, gnomADG, Gene, EnsemblGene) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)
            connection.commit()

connection.close()