import json
import cherrypy

from _movie_database import _movie_database

class VotesController(object):
    def __init__(self, mdb=None):
        if mdb is None:
            self.mdb = _movie_database()
        else:
            self.mdb = mdb
        self.mdb.load_ratings('ml-1m/ratings.dat')
        self.mdb.load_votes('ml-1m/ratings.dat')

    def DELETE_RECOMMENDATIONS(self):
        output = {'result' : 'success'}
        try:
            self.mdb.delete_all_votes()
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)
        
        print("json dump output", json.dumps(output))
        return json.dumps(output)

    def PUT_RECOMMENDATIONS(self, user_id):
        output = {'result': 'success'}
        try:
            user_data = cherrypy.request.body.read()
            user_data = json.loads(user_data)
            self.mdb.set_vote(int(user_id), user_data)
        except Exception as ex:
            output['result'] = "error"
            output['message'] = str(ex)
        
        return json.dumps(output)

    def GET_RECOMMENDATIONS(self, user_id):
        output = {'result': 'success'}
        try:
            recommendation = self.mdb.get_user_recommendation(int(user_id))
            print("recommendation: ", recommendation)
            output['movie_id'] = recommendation
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)
        return json.dumps(output)