#!/usr/bin/env python
'''
upload protein accession and download fasta from ncbi
'''

import os
from Bio import Entrez
import pandas as pd
import argparse

def get_pvog_name(file):
    file_name = os.path.basename(file)
    pvog_name = file_name.split('.')[0]
    return pvog_name

def upload_id_to_entrez_history(file, database):
    id_list= pd.read_csv(file)
    accessions = id_list['seqname']
    search_results = Entrez.epost(database, id= ','.join(accessions))
    webenv = search_results['WebEnv']
    query_key = search_results['QueryKey']
    return webenv, query_key


def _get_fasta_(file, email, database):
    Entrez.email = email
    entrez_history_handle = upload_id_to_entrez_history(file, database)
    webenv = entrez_history_handle[0]
    query_key = entrez_history_handle[1]
    count = len(pd.read_csv(file)['seqname'])

    try:
        from urllib.error import HTTPError # python 3
    except ImportError:
        from urllib2 import HTTPError # python 2

    batch_size = 3
    out_handle = open(get_pvog_name(file)+'.fasta', 'w')
    for start in range(0, count, batch_size):
        end = min(count, start+batch_size)
        print("Going to download record %i to %i" % (start + 1, end))
        attempt = 0
        while attempt < 3:
            attempt =+ 1
            try:
                fetch_handle = Entrez.efetch(db=database,
                                             rettype="fasta", retmode="text",
                                             retstart=start, retmax=batch_size,
                                             webenv=webenv, query_key=query_key,
                                             idtype="acc")
            except HTTPError as err:
                if 500 <= err.code <= 599:
                    print("Received error from server %s" % err)
                    print("Attempt %i of 3" % attempt)
                    time.sleep(15)
                else:
                    raise
        data = fetch_handle.read()
        fetch_handle.close()
        out_handle.write(data)
    out_handle.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'download protein sequences from NCBI using accessions')
    parser.add_argument('-file', help='location of pVOG Protein Table', required=True)
    parser.add_argument('-email', help='Email for accessing NCBI Entrez. Please use a real email address')
    parser.add_argument('-database', help='Database you wish to retrieve sequences from')

    args=parser.parse_args()
    _get_fasta_(seq_names = args.file, email = args.email, database = args.database)