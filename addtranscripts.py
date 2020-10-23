import sqlite3
import anno

def getTranscriptInfo (transcript, hgvs):

    data = [
        hgvs,
        transcript['gene_symbol'], 
        transcript['gene_id'],
        transcript['transcript_id'],
        transcript['consequence_terms'][0],
        transcript['strand'],
    ]
    if 'canonical' in transcript: 
        data.append(transcript['canonical'])
    else: 
        data.append(0)

    if 'cdna_start' in transcript:
        data.append(transcript['cdna_start'])
        data.append(transcript['cdna_end'])
    else:
        data.append(None)
        data.append(None)

    if 'cds_start' in transcript:
        data.append(transcript['cds_start'])
        data.append(transcript['cds_end'])
    else:
        data.append(None)
        data.append(None)

    if 'protein_start' in transcript:
        data.append(transcript['protein_start'])
        data.append(transcript['protein_end'])
    else:
        data.append(None)
        data.append(None)

    if 'amino_acids' in transcript:
        data.append(transcript['amino_acids'])
    else: 
        data.append(None)

    return tuple(data)

#Database access
filename = input('Please enter database name: ')
connection = sqlite3.connect(filename)
cursor = connection.cursor()

#Import annotations
annoList = anno.get("")

for anno in annoList: 
    if 'transcript_consequences' in anno['vep']:
        #Get transcript info
        for transcript in anno['vep']['transcript_consequences']:
            transcriptInfo = getTranscriptInfo(transcript, anno['vep']['id'])
            #Add to table
            cursor.execute('INSERT INTO Transcripts(HGVS, Gene, EnsemblGene, EnsemblTranscript, Consequence, Canonical, Strand, cdna_start, cdna_end, cds_start, cds_end, protein_start, protein_end, amino_acids) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', transcriptInfo)

connection.commit()
connection.close()