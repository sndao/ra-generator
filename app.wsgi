import bottle
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json
import random
from bottle import error

def rag():
    
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open("DSA Problems")

    data = spreadsheet.get_worksheet(0).get_all_values()
    
    rag = random.randint(1, len(data) - 1)

    while len(data[rag][4]) > 0:
        rag = random.randint(1, len(data) - 1)
    
    for i, x in enumerate(data[rag]):
    	data[rag][i] = x.replace('\n', '<br>')
    
    #return '<br>'.join(data[rag])
    return data[rag]

@bottle.route('/')

def index():
    algo = rag()

    algo_id = algo[0]
    task = algo[1]
    desc = algo[2]
    context = algo[3]
    completed = algo[4]
    time_taken = algo[5]
    source = algo[6]
    problem_no = algo[7]

    if len(context) > 0:
        context = "<b>Context:</b> " + context

    if 'http' in source:
    	source = '<a target="_blank" href="{0}">{0}</a>'.format(source)

    algorithm = """
    <title>Random Algorithm Generator</title>

    <h1>{0} <i>{6}</i></h1>
   	<b>Problem #{5}:</b>
   	<br>{1}<br><br>
   	{2}<br><br>
   	<b>Source:</b> {3} {4}<br><br><br><br>
   	<a href=\"/\"><h1><center>NEXT PROBLEM</h1></a>
    """.format(task, desc, context, source, algo[7], algo_id,completed)

    return algorithm

@error(500) 
def custom500(error):
    return '<meta http-equiv="refresh" content="0; url=/" />'


application = bottle.default_app()
