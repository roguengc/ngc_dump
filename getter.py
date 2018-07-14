import requests  # btw install requests

from os import path, stat
from time import sleep
from tqdm import tqdm  # btw install tqdm for a progress bar

xml_dir = './xml'

def get_xml(num):
  '''
  For a given NGC guideline number, ensure that the XML file for that guideline has been downloaded.

  :param num: the NGC guideline number
  :type num: int
  :return: whether the file has been gotten
  :rtype: bool
  '''
  # check if we already have the file and it is non-zero in length
  filename = 'ngc-{}.xml'.format(num)
  filepath = path.join(xml_dir, filename)
  if path.isfile(filepath) and stat(filepath).st_size > 0:
    return True  # already got it and it's maybe not bad

  url = 'https://www.guideline.gov/summaries/downloadcontent/ngc-{}?contentType=xml'.format(num)
  r = requests.get(url)

  # validate the response code
  if r.status_code < 200 or r.status_code >= 300:
    return False

  # validate the content type
  if 'text/xml' not in r.headers.get('content-type'):
    return False

  # validate the content length
  if r.headers.get('content-length') == 0:
    return False

  with open(filepath, 'wb') as xml_file:
    xml_file.write(r.content)

  # yay
  return True

def main():
  start = 1
  end = 12000

  good = 0
  bad = 0

  for i in tqdm(range(start, end)):
    if get_xml(i):
      good += 1
    else:
      bad += 1
    sleep(0.1)  # don't be a jerk

  print('got {} successfully!'.format(good))
  print('{} seemed to fail for some reason.'.format(bad))

if __name__ == '__main__':
  main()

