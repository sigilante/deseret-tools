  # Convert IPA phoneme to Deseret letter.
  ipa2des = {
      'i':'𐐀',    'oʊ':'𐐄',    'æ':'𐐈',    'aɪ':'𐐌',
      'h':'𐐐',    'd':'𐐔',     'g':'𐐘',    'ð':'𐐜',
      'ʒ':'𐐠',    'n':'𐐤',     'eɪ':'𐐁',   'u':'𐐅',
      'ɒ':'𐐉',    'aʊ':'𐐍',    'p':'𐐑',    'tʃ':'𐐕',
      'f':'𐐙',    's':'𐐝',     'r':'𐐡',    'ŋ':'𐐥',
      'ɑ':'𐐂',    'ɪ':'𐐆',     'ʌ':'𐐊',    'w':'𐐎',
      'b':'𐐒',    'dʒ':'𐐖',    'v':'𐐚',    'z':'𐐞',
      'l':'𐐢',    'ɔɪ':'𐐦',    'ɔ':'𐐃',    'ɛ':'𐐇',                                                                                                                                                                                                                                                                        
      'ʊ':'𐐋',    'j':'𐐏',     't':'𐐓',    'k':'𐐗',
      'θ':'𐐛',    'ʃ':'𐐟',     'm':'𐐣',    'ju':'𐐧',
      # below this line are the hacks
      'ɹ':'𐐡',    'ɝ':'𐐆𐐡'
  }
   
  # Convert Deseret letter to IPA phoneme.
  des2ipa = {ipa2des[key]:key for key in ipa2des}
   
  # Convert ARPA-style phoneme to IPA phoneme.
  arpa2ipa = {
      'AA':'ɑ',    'AE':'æ',    'AH':'ʌ',    'AO':'ɔ',
      'AW':'aʊ',   'AY':'aɪ',   'B':'b',     'CH':'tʃ',
      'D':'d',     'DH':'ð',    'EH':'ɛ',    'ER':'ɝ',
      'EY':'eɪ',   'F':'f',     'G':'g',     'HH':'h',
      'IH':'ɪ',    'IY':'i',    'JH':'dʒ',   'K':'k',
      'L':'l',     'M':'m',     'N':'n',     'NG':'ŋ',
      'OW':'oʊ',   'OY':'ɔɪ',   'P':'p',     'R':'ɹ',
      'S':'s',     'SH':'ʃ',    'T':'t',     'TH':'θ',
      'UH':'ʊ',    'UW':'u',    'V':'v',     'W':'w',
      'WH':'ʍ',    'Y':'j',     'Z':'z',     'ZH':'ʒ'
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
