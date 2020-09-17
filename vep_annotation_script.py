import anno
import hgvs
import annotation

if __name__ == "__main__":
    filename = input('Please enter HGVS filename: ')
    listHGVS = hgvs.get(filename)
    listVEP = annotation.VEP(listHGVS)
    anno.output(listVEP, 'vep_annotation')