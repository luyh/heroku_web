import requests
import time

def get_fear_greed_index(limit = 1):
    url = 'https://api.alternative.me/fng/?limit={}'.format(limit)
    #print(url)
    r = requests.get(url)

    if r.status_code != 200:
        print( 'fail get fear_greed_index', r.status_code, r.text )
        return
    r = r.json()['data']

    for i in range( len( r ) ):
        times_tamp = int( r[i]['timestamp'] )
        time_local = time.localtime( times_tamp )
        time_str = time.strftime( "%Y-%m-%d", time_local )
        r[i]['time'] = time_str
        r[i]['value'] = int( r[i]['value'] )

    return r