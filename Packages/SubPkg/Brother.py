import requests
from bs4 import BeautifulSoup

'''
Since Brother does not provide enough information (at least for me so far) to design a snmp request to get
all information wanted (especialy the toner fill values that only provide a handful states).

Thats why the Brother Methods use Web Scraping of the clients hosted web interface its codewise a bit
tidius since the html on that pages obviously wasnt designed for that and doesnt provide unique tag id or name
further brother seems to follow a certain concept for this page but still different series/models can differ from
slight changes to completly different.

Future Idea´s: there is a Export function on many (known to me) nodels, on the webinterface that will download
the data displayed on the interface as a .csv file what would sidestep the need of extract the data entirely
and since csv format is widely used anyway in this project would help to get a clean single methode for all models
with this function
'''


class Brother(object):
	'''
  	The Request class for Brother since the Webinterface isnt consistent there are multiple but they will get chosen
  	during initializing by Model, the use is simple the get method that will return a dict with only the datetime missing
  	what is added by the Main Request class
  	'''
	def __new__(cls, *args):
    	'''
    	args = str(ip), str(model) 
    	'''
    	if args[0] in ('MFC-9142CDN', 'MFC-L3750CDW series', 'MFC-L3770CDW', 'MFC-9332CDN', 'MFC-L8650CDW', 'MFC-9342CDW'):
			return super().__new__(cls)
		if args[0] in ('MFC-9460CDN',):
			cls = _BrotherAlt1
			return super().__new__(cls)
		
	def __init__(self, *args):
		ip = args[1]
		self.url = f'http://{ip}/general/status.html', f'http://{ip}/general/information.html?kind=item'
		self.toner_mul = 100 / 56
		
	def _get_soup(self, i):
		req = requests.get(self.url[i])
		return BeautifulSoup(req.content, 'html.parser')
	
	def _get_toner(self):
		soup = self._get_soup(0)
		result = soup.find_all(name='img', class_='tonerremain')
		result = [(a[1].split('=')[1][1], a[3].split('=')[1].strip('"')) for a in [str(t).split(' ') for t in result]]
		result = [(r[0], int(r[1].replace('px', ''))) for r in result]
		return {r[0]: int(r[1] * self.toner_mul) for r in result}
		
	def _get_pages(self):
		soup = self._get_soup(1)
		divs = soup.find_all(name='div', class_='contentsGroup')
		for div in divs:
			if 'Total Pages Printed' in str(div):
				result, key_, key = {}, ['Copy', 'Print'], ''
				for t, d in zip(div.find_all(name='dt'), div.find_all(name='dd')):
					key = str(t.text) if 'class="unit"' in str(d) else key
					
					if key in key_ and str(t.text) in ['Colour', 'Color', 'B&W']:
						temp = str(t.text).replace('u', '').replace('B&W', '') + key.replace('y', 'ie') + 's'
						result[temp] = int(d.text)
						if len(result.keys()) == 4:
							return result
	
	def get(self):
		result = self._get_toner()
		result.update(self._get_pages())
		return result


class _BrotherAlt1(Brother):
	def __init__(self, *args):
		super().__init__(*args)
		ip = args[1]
		self.url = (f'http://{ip}/etc/mnt_info.html?kind=item', f'http://{ip}/etc/mnt_info.html?kind=item')
		self.toner_mul = 10
		self.temp = {'C': 29, 'M': 30, 'Y': 31, 'B': 32, 'ColorCopies': 51, 'Copies': 52, 'ColorPrints': 54, 'Prints': 55}
		
	def get(self):
		soup = self._get_soup(0)
		table = soup.find(name='table', cellspacing='10')
		for n, tds in enumerate([tr.find_all(name='td') for tr in table.find_all(name='tr')]):
			if n in self.temp.values():
				line = [v for v in ''.join([str(td.text) for td in tds]).strip().splitlines() if v != '']
				if n <= 32:
					key = [k for k, v in self.temp.items() if v == n][0]
					self.temp[key] = line[1].count('■') * self.toner_mul
				else:
					key = [k for k, v in self.temp.items() if v == n][0]
					self.temp[key] = int(line[1])
			if n == 55:
				return self.temp
