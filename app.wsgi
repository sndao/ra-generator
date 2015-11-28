import bottle
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json
import random
from bottle import error

def rag():

    username = "hearthdao"
    password = "vdighzomctdbiodg"
    docid = "1vG1UbY0414FS1ytxBBusk4Il8Md4CIq877buicuF5Xo"

    json_key = json.load(open('/home/stevendao/webapps/ragbottle/stevennguyendao-129d370e8efa.json'))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open("DSA Problems")

    data = spreadsheet.get_worksheet(0).get_all_values()
    rag = random.randint(1, len(data) - 1)
    
    for x in data[rag]:
    	x.replace('\n', '<br>')
    
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

    if len(completed) > 0:
    	completed = '[Completed]'

    if 'http' in source:
    	source = '<a target="_blank" href="{0}">{0}</a>'.format(source)

    algorithm = """
    <title>Random Algorithm Generator</title>

    <h1>{0} <i>{6}</i></h1>
   	<b>Problem #{5}:</b>
   	<br>{1}<br><br>
   	Context: {2}<br><br>
   	Source: {3} {4}<br><br>
   	<a href=\"/\"><h1>Give me a new problem!</h1></a>
    """.format(task, desc, context, source, algo[7], algo_id,completed)

    return algorithm

@error(500) 
def custom500(error):
    return '<meta http-equiv="refresh" content="0; url=/" />'
    #return '<a href=\"/\"><h1>Give me a new problem!</h1></a>'





application = bottle.default_app()