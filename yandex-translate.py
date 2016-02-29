import requests
import rpmfile
import argparse
import os
import sys

parser = argparse.ArgumentParser(prog='SuperPuperMegaTranslator',
								 description='Translate all shit',
								 epilog='Do not forget to give thanks')

parser.add_argument('-s', '--s', help='PATH to directory with source packages', required=True )
parser.add_argument('-d', '--d', help='PATH to directory with translated files', required=True)
args = parser.parse_args()
source = args.s
destination = args.d


def translate(source_dir, dest_dir):
	# Directory with source rpm packages. Conver to abspath
	source_dir = os.path.abspath(source_dir)

	# Directory to save translates. Convert to abspath
	dest_dir = os.path.abspath(dest_dir)

	#URL for yandex-translate API
	Url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

	# API key for yandex-translate. You can get it from your yandex account
	ApiKey = 'your API-key'

	# Translate direction
	Lang = 'en-ru'

	# Output format. Can be html or plain
	Format = 'plain'

	if os.path.isdir(source_dir) and os.path.isdir(dest_dir):
		os.chdir(source_dir)
		for file in os.listdir(source_dir):
			with rpmfile.open(file) as rpm:
				orig_text = rpm.headers.get('description', None).decode('utf-8')
				pkg_name = rpm.headers.get('name', None).decode('utf-8')
			Data = {'key' : ApiKey, 'text' : orig_text, 'lang' : Lang, 'format' : Format}
			Request = requests.get(Url, params=Data)
			Response = Request.json()
			tr_text = Response.get('text', None)
			with open(dest_dir + os.path.sep + pkg_name + '.txt', 'w') as f:
				f.writelines(tr_text)
	else:
		print("Check your source and destination directories")
		sys.exit(1)

translate(source, destination)
