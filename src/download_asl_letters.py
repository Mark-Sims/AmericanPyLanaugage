import urllib, os

alphabet = map(chr, range(97, 123))
assets_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), u'..\\assets\\')

for letter in alphabet:
	filename = '{}_labelled.png'.format(letter)
	filepath = os.path.join(assets_dir, filename)
	urllib.urlretrieve("https://www.wpclipart.com/sign_language/American_ABCs/{}".format(filename), filepath)
	print "Downloaded {}".format(filepath)