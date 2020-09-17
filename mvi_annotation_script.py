import anno
import hgvs
import annotation

if __name__ == "__main__":
    filename = input('Please enter HGVS filename: ')
    listHGVS = hgvs.get(filename)
    
    listMVI = []

    for HGVS in listHGVS: 
        listMVI.append(annotation.MVI(HGVS))
        if listHGVS.index(HGVS)%1000 == 0: 
            print (str(listHGVS.index(HGVS)) + 'out of ' + str(len(listHGVS)) + 'completed')

    anno.output(listMVI, 'mvi_annotation.txt')