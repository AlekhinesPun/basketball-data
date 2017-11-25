from datetime import datetime
import urllib2
import xml.etree.ElementTree as et
import numpy as np 
import pandas as pd

def get_data_stat(string,stat):
	try:
		if stat == 'player':
			return string.split('data-stat="'+stat+'"')[1].split('>')[2].split('<')[0]
		elif stat == 'id':
			return string.split('data-append-csv="')[1].split('"')[0]
		return string.split('data-stat="'+stat+'"')[1].split('>')[1].split('<')[0]
	except:
		return

def get_player_stats(game_string,
	stats=['player','mp','trb','ast','stl','blk','tov','pts','plus_minus']):
	return_me = {}
	for z in game_string.split('Basic Box Score Stats</th>')[1].split('<tr') \
		   + game_string.split('Basic Box Score Stats</th>')[2].split('<tr'):
		y = z.split('</tr>')[0]
		if 'aria-label' in y:
			continue
		pid = get_data_stat(y,'id')
		if pid == None or pid in return_me:
			continue
		return_me[pid] = {}
		for s in stats:
			return_me[pid][s] = get_data_stat(y,s)
	return pd.DataFrame(return_me).transpose()


def get_score_data(game_string,stats):
	line_score = game_string.split('div_line_score')[1].split('</div>')[0]
	game_id = game_string.split('https://www.basketball-reference.com/boxscores/')[1].split('.html')[0]
	return_me = {}
	return_me['date'] = game_id[:4]+'-'+game_id[4:6]+'-'+game_id[6:8]
	return_me['away_team'] =  line_score.split('<a href="/teams/')[1].split('>')[1].split('<')[0]
	return_me['away_score'] =  line_score.split('<strong>')[1].split('</strong>')[0]
	return_me['home_team'] =  line_score.split('<a href="/teams/')[2].split('>')[1].split('<')[0]
	return_me['home_score'] =  line_score.split('<strong>')[2].split('</strong>')[0]
	return return_me

def all_scores(path='data/'):
	scores = {}
	for fn in os.listdir(path):
		with open(path+fn,'r') as f:
			gs = f.read()
			scores[fn.split('.')[0]] = get_score_data(gs)
	return pd.DataFrame(scores).transpose().sort_values('date')