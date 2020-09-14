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

    inputfile.close()

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
        outputfile.write(json.dumps(anno))
        #Check to see if the last element has been reached before entering a
        #newline character
        if listanno.index(anno) != (len(listanno)-1):
            outputfile.write('\n')
    outputfile.close()
    print('Export completed.' + '\n')