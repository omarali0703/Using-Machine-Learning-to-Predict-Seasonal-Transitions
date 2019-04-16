import os
import re
def get_choices():
    data_choices = os.listdir('/met_office_data')
    choices = []
    for name in data_choices:
        if name.endswith(".txt"):
            choices.append(name)
    return choices

def convert_all():
    choices = get_choices()

    for choice in choices:
        convert(choice)


def convert(file):   
    raw_text = open(file, 'r').read()
    text = 'yyyy,mm ,maxC, minC, r, r, r,'
    text+= raw_text.split("hours",1)[1]
    text= text.replace('mm ', 'mm')
    text= text.replace(' minC', 'minC')
    
    text=re.sub('[ \t]+', ' ', text)

    text=re.sub('[ \t]+[mm][ \t]+', 'mm', text)
    text=re.sub('[ \t]+[maxC][ \t]+', 'maxC', text)
    text=re.sub('[ \t]+[minC][ \t]+', 'minC', text)
    text=re.sub('[ \t]+[yyyy][ \t]+', 'yyyy', text)
    
    text=re.sub('[0]{1}[\ ]', '0,', text)
    text=re.sub('[1]{1}[\ ]', '1,', text)
    text=re.sub('[2]{1}[\ ]', '2,', text)
    text=re.sub('[3]{1}[\ ]', '3,', text)
    text=re.sub('[4]{1}[\ ]', '4,', text)
    text=re.sub('[5]{1}[\ ]', '5,', text)
    text=re.sub('[6]{1}[\ ]', '6,', text)
    text=re.sub('[7]{1}[\ ]', '7,', text)
    text=re.sub('[8]{1}[\ ]', '8,', text)
    text=re.sub('[9]{1}[\ ]', '9,', text)

    text = text.replace('---', '0,')
    text = text.replace('Provisional', '')
    text = text.replace('#', ',')
    text = text.replace('*', ',')
    
    
    file = open("rawdata/" + file.replace('data.txt', '_raw_data.csv'), 'w')
    file.write(text)
    print(text)

convert_all()
