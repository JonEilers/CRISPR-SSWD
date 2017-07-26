#!/usr/bin/env anaconda3

'''
script to extract tax_id from species.txt using the accession number found in the pVOG table

to-do
some files do not contain all the tax_ids that should be there and vog9999 is not being parsed
'''



import argparse

def increment_pvog(line, pvog):
    if 'VOG' in line:
        pvog_counter = 1
        pvog_counter += 1
        if 'VOG' in line:
            lp = len(pvog)
            lc = len(str(pvog_counter))
            pvog = pvog[0:lp-lc]+str(pvog_counter)
            if pvog != line[0:7]:
                pvog = line[0:7]
            return pvog

def get_accensions(line, accensions):
    if 'VOG' in line:
        accension_index1 = 0
        accension_index2 = 0
        counter1 = 0
        counter2 = 0
        while counter1<3 and counter2<1:
            for i,n in enumerate(line):
                if n == ':' and counter1 < 3:
                    counter1 += 1
                    accension_index1 = i
                if n == '|' and counter2 <1:
                    counter2 += 1
                    accension_index2 = i
            accensions.append(line[accension_index1+1:accension_index2])
        #print(accensions)
        return accensions

def get_tax_id(line, tax_id):
    if 'VOG' in line:
        reversed_line = line[::-1]
        a = 0
        b = 0
        for i,n in enumerate(reversed_line):
            t = i
            m = n
            if n == ']' and a==0:
                a = len(line)-i-1
            if n =='[' and b==0:
                b = len(line)-i
        tax_id.append(line[b:a])
        print(tax_id)
        return tax_id

def write_tax_id(accensions, tax_id, pvog):
    seq_dict = {}
    #print(accensions)
    #print(tax_id)
    for i in range(0,len(accensions)):
        seq_dict[accensions[i]]=tax_id[i]
    seq_names = open('seq_names/'+pvog+'.seqnames.csv', 'w')
    taxonomy = open('tax_id/'+pvog+'.tax.txt', 'w')
    seq_names.write('seqname'+','+'tax_id'+'\n')
    #print(len(seq_dict))
    for i in tax_id:
        #print(i)
        taxonomy.write(str(i)+'\n')
    for i in seq_dict:
        seq_names.write(str(i)+ ',' + str(seq_dict[i])+'\n')
    seq_names.close()
    taxonomy.close()

def main(file):
    table_handle = open(file, 'r')
    handle = table_handle.readlines()
    pvog = 'VOG0001'
    tax_id = []
    accensions = []
    counter = 0
    for line in handle:
        counter += 1
        #print(line)
        if pvog in line:
            tax_id = get_tax_id(line, tax_id)
            accensions = get_accensions(line, accensions)
        elif pvog not in line:
            write_tax_id(accensions, tax_id, pvog)
            pvog = increment_pvog(line, pvog)
            tax_id = []
            accensions = []
            tax_id = get_tax_id(line, tax_id)
            accensions = get_accensions(line, accensions)
    table_handle.close()
    #print(counter)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'extract taxonomic information from pVOG Protein Table for use in making reference packages')
    parser.add_argument('-file', help='location of pVOG Protein Table', required=True)

    args=parser.parse_args()
    main(file = args.file)



