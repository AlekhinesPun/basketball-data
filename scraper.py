from datetime import datetime
import urllib2
import xml.etree.ElementTree as et
import numpy as np 
import pandas as pd

def zero_pad_str(s,length=2):
	s = str(s)
	while len(s) < length:
		s = '0'+s
	return s

def path_gen(year,month,day):
	return 'https://www.basketball-reference.com/boxscores/?month=' \
			+ zero_pad_str(month)+'&day=' \
			+ zero_pad_str(day)+'&year=' \
			+ str(year)
			
def path_box(game):
	return 'https://www.basketball-reference.com/boxscores/'+game+'.html'

def get_games(path):
	req = urllib2.Request(path)
	schedule_page = urllib2.urlopen(req).read()
	if 'No games played on this date.' in schedule_page:
		return []
	games_page = schedule_page.split('<div class="game_summaries">')[1]
	gstrs = [z.split('.html')[0] for z in games_page.split('/boxscores/')[1:]]
	games = list(set(filter(lambda x: '/' not in x,gstrs)))
	return games

def get_box(path):
	req = urllib2.Request(path)
	page = urllib2.urlopen(req).read()
	return page

def get_data_stat(string,stat):
	try:
		return string.split('data-stat="'+stat+'"')[1].split('>')[1].split('<')[0]
	except:
		return

if __name__ == '__main__':
	all_games = [z[1] for z in pd.read_csv('games.csv').values.tolist()]
	print len(all_games)
	start_time = datetime.now()
	for n,game in enumerate(all_games):
		with open('data/'+game+'.txt','w') as f:
			f.write(get_box(path_box(game)))
		print n,len(all_games),game,(datetime.now()-start_time).total_seconds(),(len(all_games) - n - 1)*(datetime.now()-start_time).total_seconds()/(n+1.)
