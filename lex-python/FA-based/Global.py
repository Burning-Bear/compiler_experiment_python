#!usr/bin/env python
#coding=utf-8
#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.2
# Modified    :   2017.1.2
# Version     :   1.0


DFA_hash_dic = {
    '0':{
        'i':'1','t':'2','w':'3','f':'4','d':'6',
        '+':'e7','-':'e7','*':'e7','/':'e7',
        '>':'7','<':'8','!':'9','=':'e7',
        ' ':'e14','\t':'e14','\n':'e14',
        ',':'e17',';':'e17',
        '(':'e19',')':'e19',
        '{':'e21','}':'e21',
        'digit':'e23','letter':'e24'},
    '1':{'f':'e27','n':'26','letter':'e24'},
    '2':{'h':'29','letter':'e24'},
    '3':{'h':'30','letter':'e24'},
    '4':{'f':'31','letter':'e24'},
    '6':{'o':'e32','letter':'e24'},
    'e7':{'=':'e42'},
    '7':{'=':'e42'},
    '8':{'=':'e42'},
    '9':{'=':'e42'},
    'e42':{},
    'e14':{' ':'e14','\t':'e14','\n':'e14'},
    'e17':{},
    'e19':{},
    'e21':{},
    'e23':{'digit':'e23'},
    'e24':{'digit':'e24','letter':'e24'},
    'e27':{'letter':'e24'},
    '26':{'t':'e33','letter':'e24'},
    '29':{'e':'34','letter':'e24'},
    '30':{'i':'39','letter':'e24'},
    '31':{'o':'35','letter':'e24'},
    'e32':{'letter':'e24'},
    'e33':{'letter':'e24'},
    '34':{'n':'e36','letter':'e24'},
    '39':{'l':'40','letter':'e24'},
    '35':{'a':'37','letter':'e24'},
    'e36':{'letter':'e24'},
    '40':{'e':'e41','letter':'e24'},
    '37':{'t':'e38','letter':'e24'},
    'e41':{'letter':'e24'},
    'e38':{'letter':'e24'}
}

node_reg_mapping={
    'e27':{'level':1,'info':'if keyword'},
    'e33':{'level':1,'info':'type'},
    'e36':{'level':1,'info':'then keyword'},
    'e41':{'level':1,'info':'while keyword'},
    'e32':{'level':1,'info':'do keyword'},
    'e7':{'level':0,'info':'operator'},
    'e42':{'level':1,'info':'relational operator'},
    'e14':{'level':0,'info':'whitespace'},
    'e17':{'level':1,'info':'delimiter'},
    'e19':{'level':1,'info':'brackets'},
    'e21':{'level':1,'info':'block'},
    'e23':{'level':2,'info':'digits'},
    'e24':{'level':2,'info':'identfier'},
}
key_mapping_regex={
    'letter':ur'[A-Za-z]',
    'digit':ur'[0-9]'
}