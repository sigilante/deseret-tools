# Convert IPA phoneme to Deseret letter.
ipa2des = {
    'i':'ð',    'oÊ':'ð',    'Ã¦':'ð',    'aÉª':'ð',
    'h':'ð',    'd':'ð',     'g':'ð',    'Ã°':'ð',
    'Ê':'ð ',    'n':'ð¤',     'eÉª':'ð',   'u':'ð',
    'É':'ð',    'aÊ':'ð',    'p':'ð',    'tÊ':'ð',
    'f':'ð',    's':'ð',     'r':'ð¡',    'Å':'ð¥',
    'É':'ð',    'Éª':'ð',     'Ê':'ð',    'w':'ð',
    'b':'ð',    'dÊ':'ð',    'v':'ð',    'z':'ð',
    'l':'ð¢',    'ÉÉª':'ð¦',    'É':'ð',    'É':'ð',                                                                                                                                                                                                                                                                        
    'Ê':'ð',    'j':'ð',     't':'ð',    'k':'ð',
    'Î¸':'ð',    'Ê':'ð',     'm':'ð£',    'ju':'ð§',
    # below this line are the hacks
    'É¹':'ð¡',    'É':'ðð¡'
}

# Convert Deseret letter to IPA phoneme.
des2ipa = {ipa2des[key]:key for key in ipa2des}

# Convert ARPA-style phoneme to IPA phoneme.
arpa2ipa = {
    'AA':'É',    'AE':'Ã¦',    'AH':'Ê',    'AO':'É',
    'AW':'aÊ',   'AY':'aÉª',   'B':'b',     'CH':'tÊ',
    'D':'d',     'DH':'Ã°',    'EH':'É',    'ER':'É',
    'EY':'eÉª',   'F':'f',     'G':'g',     'HH':'h',
    'IH':'Éª',    'IY':'i',    'JH':'dÊ',   'K':'k',
    'L':'l',     'M':'m',     'N':'n',     'NG':'Å',
    'OW':'oÊ',   'OY':'ÉÉª',   'P':'p',     'R':'É¹',
    'S':'s',     'SH':'Ê',    'T':'t',     'TH':'Î¸',
    'UH':'Ê',    'UW':'u',    'V':'v',     'W':'w',
    'WH':'Ê',    'Y':'j',     'Z':'z',     'ZH':'Ê'
}

# Convert IPA phoneme to ARPA-style phoneme.
ipa2arpa = {arpa2ipa[key]:key for key in arpa2ipa}

# Read in English wordlist with ARPA-style phonetic pronunciation.
with open('cmudict.txt', 'r') as wordfile:
    worddata = wordfile.readlines()

latinwords = {}
englishprons = {}
for line in worddata:
    # Prepare key
    if '(' in line: continue
    word = line.split('  ')[0].split('(')[0]

    # Prepare phonetic value
    phonemes = line.strip().split('  ')[1:][0]
    for digit in range(10):
        phonemes = phonemes.replace(str(digit), '')
    ipaphoneme = []
    for ph in phonemes.split(' '):
        ipaphoneme.append(arpa2ipa[ph])
    latinwords[word] = ipaphoneme
    englishprons[word] = ''.join(phonemes)

deseretwords = {}
for word in latinwords:
    deseretword = ''
    for phoneme in latinwords[word]:
        deseretword += ipa2des[phoneme]
    deseretwords[word] = deseretword
deseretwords['THE'] = 'ð'

__puncs__ = '.,:;/?\|`~!@#$%^&*()[]{}"\'-+_='
__puncs_rspace__ = '.,:;?!%)]}'
__puncs_lspace__ = '#$([{'
for p in __puncs__:
    deseretwords[p] = p

import re
def latin2des(lat):
    '''
    Convert a Latin-alphabet phrase to the Deseret alphabet.
    '''
    lat = re.findall(r"\w+|[^\w\s]", lat, re.UNICODE)
    des = [deseretwords[s.upper()] for s in lat]
    for i in range(len(lat)):
        if lat[i].isupper():
            des[i] = des[i].upper()
        elif lat[i].islower():
            des[i] = des[i].lower()
        elif lat[i].istitle():
            des[i] = des[i].title()
        else:
            des[i] = des[i]
    text = ' '.join(des)
    for p in __puncs_rspace__:
        text = text.replace(f' {p}', p)
    for p in __puncs_lspace__:
        text = text.replace(f'{p} ', p)
    return text

def des2latin(des):
    '''
    Convert a Deseret-alphabet phrase to the Latin alphabet phonetically.
    '''
    pass

def checkPangram(lat):
    des = latin2des(lat)
    not_in = []
    for k in des2ipa:
        if (k.upper() not in des) and (k not in __puncs__):
            not_in.append(k)
    return not_in

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert Latin to Deseret alphabet.')
    parser.add_argument('phrase', metavar='p', type=str, nargs='+',
                        help='a Latin-alphabet phrase to translate into Deseret')
    args = parser.parse_args()
    print(latin2des(args.phrase[0]))
