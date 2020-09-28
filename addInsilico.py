import sqlite3
import anno

#Database access
connection = sqlite3.connect('family_M.db')
cursor = connection.cursor()

#Import annotations
annoList = anno.get("")

#Write to table
for variant in annoList: 
    #Variable list
    hgvs = variant['_id']
    gene = None
    upACC = None
    upEntry = None
    proveanP = None
    proveanS = None
    proveanR = None
    pp2P = None
    pp2S = None
    pp2R = None
    siftP = None
    siftS = None
    siftR = None
    caddRaw = None
    caddPhred = None

    try: 
        if 'dbnsfp' in variant['mvi']:
            if type(variant['mvi']['dbnsfp']['genename'] is list):
                #Take only first element
                if 'genename' in variant['mvi']['dbnsfp']:
                    gene = variant['mvi']['dbnsfp']['genename'][0]
                if 'uniprot' in variant['mvi']['dbnsfp']:
                    upACC = variant['mvi']['dbnsfp']['uniprot'][0]['acc']
                    upEntry = variant['mvi']['dbnsfp']['uniprot'][0]['entry']
                if 'provean' in variant['mvi']['dbnsfp']:
                    proveanP = variant['mvi']['dbnsfp']['provean']['pred'][0]
                    proveanS = variant['mvi']['dbnsfp']['provean']['score'][0]
                    proveanR = variant['mvi']['dbnsfp']['provean']['rankscore']
                if 'polyphen2' in variant['mvi']['dbnsfp']:
                    pp2P = variant['mvi']['dbnsfp']['polyphen2']['hvar']['pred'][0]
                    pp2S = variant['mvi']['dbnsfp']['polyphen2']['hvar']['score'][0]
                    pp2R = variant['mvi']['dbnsfp']['polyphen2']['hvar']['rankscore']
                if 'sift' in variant['mvi']['dbnsfp']:
                    siftP = variant['mvi']['dbnsfp']['sift']['pred'][0]
                    siftS = variant['mvi']['dbnsfp']['sift']['score'][0]
                    siftR = variant['mvi']['dbnsfp']['sift']['converted_rankscore']
                if 'cadd' in variant['mvi']:
                    caddRaw = variant['mvi']['cadd']['rawscore']
                    caddPhred = variant['mvi']['cadd']['phred']
            else: 
                #Take roots
                if 'genename' in variant['mvi']['dbnsfp']:
                    gene = variant['mvi']['dbnsfp']['genename']
                if 'uniprot' in variant['mvi']['dbnsfp']:
                    upACC = variant['mvi']['dbnsfp']['uniprot']['acc']
                    upEntry = variant['mvi']['dbnsfp']['uniprot']['entry']
                if 'provean' in variant['mvi']['dbnsfp']:
                    proveanP = variant['mvi']['dbnsfp']['provean']['pred']
                    proveanS = variant['mvi']['dbnsfp']['provean']['score']
                    proveanR = variant['mvi']['dbnsfp']['provean']['rankscore']
                if 'polyphen2' in variant['mvi']['dbnsfp']:
                    pp2P = variant['mvi']['dbnsfp']['polyphen2']['hvar']['pred']
                    pp2S = variant['mvi']['dbnsfp']['polyphen2']['hvar']['score']
                    pp2R = variant['mvi']['dbnsfp']['polyphen2']['hvar']['rankscore']
                if 'sift' in variant['mvi']['dbnsfp']:
                    siftP = variant['mvi']['dbnsfp']['sift']['pred']
                    siftS = variant['mvi']['dbnsfp']['sift']['score']
                    siftR = variant['mvi']['dbnsfp']['sift']['converted_rankscore']
                if 'cadd' in variant['mvi']:
                    caddRaw = variant['mvi']['cadd']['rawscore']
                    caddPhred = variant['mvi']['cadd']['phred']
    except KeyError as e:
        print(variant['_id'])
        print(e)

    data = (hgvs, gene, upACC, upEntry, proveanP, proveanS, proveanR, pp2P, pp2S, pp2R, siftP, siftS, siftR, caddRaw, caddPhred)
    cursor.execute('INSERT INTO InSilicoModel(HGVS, Gene, UniprotACC, UniprotEntry, ProveanPred, ProveanScore, ProveanRank, Polyphen2Pred, Polyphen2Score, Polyphen2Rank, SIFTPred, SiftScore, SiftRank, CADDRaw, CADDPhred) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    connection.commit() 

connection.close()