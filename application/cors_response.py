from flask import Response
import json

def cors_res(res=None):
	newRes = None
	if res is None:
		newRes = Response()
	else:
		js = json.dumps(res)
		newRes = Response(js, status=200, mimetype='application/json')
	
	newRes.headers['Access-Control-Allow-Origin'] = "http://localhost:8080"
	newRes.headers['Access-Control-Allow-Credentials'] = 'true'
	newRes.headers['Access-Control-Allow-Headers'] = "Content-Type"

	return newRes
