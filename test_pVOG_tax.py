#!/usr/bin/ env anaconda3
from pVOG_tax import increment_pvog, get_tax_id, get_accensions

test_handle = open('VOGProteinTable.txt', 'r')
handle = test_handle.readlines()

pvogs = ['VOG0001','VOG0001','VOG0002','VOG0002','VOG0005','VOG0005','VOG0005','VOG0005','VOG0006','VOG0006','VOG0006']
test_accensions = {0:'NC_025824-YP_009111299.1',1:'NC_007189-YP_257152.1',2:'J02448-AAA32214.1', 3:'GQ153919-ACY07161.1',4:'NC_001956-NP_047372.1',5:'NC_003287-NP_510894.1',6:'NC_021562-YP_008130282.1',7:'NC_025824-YP_009111306.1', 8:'AB012574-BAA33517.1',9:'AB572858-BAJ12059.1',10:'NC_001956-NP_047369.1'}
test_tax_id = {0:'10864',1:'334856',2:'10863',3:'10870',4:'83201',5:'10870',6:'1340745',7:'10864',8:'127511',9:'867695',10:'83201'}

'''
def test_pvogs():
    test_pvogs = []
    for line in test_handle.readlines():
        if 'VOG' in line:
            test_pvogs.append(line[0:7])
    assert test_pvogs == pvogs
'''
def test_increment_pvog():
    pvog = 'VOG0001'
    inc_pvog = pvogs
    test_pvogs = []
    for line in handle:
        if 'VOG' in line:
            vog = increment_pvog(line, pvog)
            test_pvogs.append(vog)
    assert test_pvogs == inc_pvog

def test_get_accensions():
    accensions = []
    acc = {}
    for index,item in enumerate(handle):
        if 'VOG' in item:
            acc[index]= get_accensions(item, accensions)[index]
    assert test_accensions == acc

def test_get_tax_id():
    tax_id = []
    tax = {}
    for index,item in enumerate(handle):
        if 'VOG' in item:
          tax[index] = get_tax_id(item,tax_id)[index]
    assert test_tax_id == tax




