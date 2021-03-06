import os
import logging
import re
import gzip
import simplejson as json

import settings
from datetime import datetime
import nltk.data

logging.basicConfig(level=logging.INFO)

class SentenceStream(object):
        def __init__(self, filename):
                self.filename = filename
		self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        def __iter__(self):
                logging.info("begin streaming corpus")

                for review in open(self.filename,'r'):
			data = json.loads(review)
			text = data['reviewText']
			raw_sentences = self.tokenizer.tokenize(text.strip())

			for raw_sentence in raw_sentences:
				if len(raw_sentence) > 0:
					yield process(raw_sentence).split()

def unzip_files():

	file_name = os.path.join(settings.DATA_ROOT,'reviews_Electronics.json.gz')
	
	gz_file = gzip.open(file_name,'r')
	s = gz_file.read()
	gz_file.close()

	f = open(os.path.join(settings.DATA_ROOT,'reviews_Electronics.json'), 'w')
	f.write(s)
	f.close()

	logging.info("done unzipping")

	return gz_file


def read_file(limit = None):
	logging.info("begin reading files")

	sentences = []
	rev_count = 0

	file_name = os.path.join(settings.DATA_ROOT,'reviews_Electronics.json')

	if os.path.isfile(file_name) is False:
		unzip_files()

	with open(file_name,'r') as f:
		for review in f:
			data = json.loads(review)

			text = data['reviewText']

			sentences.append(process(text).split())

			rev_count+=1

			if rev_count>limit and limit:
				break

	logging.info("reviews read: {0}".format(rev_count))
def process(string):
	exclude = set(['[','^',']','\"','(','&','!','\'',':','+',')',';','?','.','-','+','#'])

	x = string.lower()
	x = re.sub("[0-9]","DG",x)

	try:
		x = "".join(ch for ch in x if ch not in exclude)
	except:
		e = sys.exc_info()[0]
		logging.error("error {0}".format(e))

	return x







