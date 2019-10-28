import json
import cherrypy

from _movie_database import _movie_database

class VotesController(object):
    def __init__(self, mdb=None):
        if mdb is None:
            self.mdb = _movie_database()
        else:
            self.mdb = mdb

    def DELETE_RECOMMENDATIONS(self):
        output = {'result' : 'success'}
        try:
            self.mdb.delete_all_votes()
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)
        return json.dumps(output)

    def GET_RECOMMENDATIONS(self, user_id):
        output = {'result': 'success'}
        try:
            recommendation = self.mdb.get_user_recommendation(int(user_id))
            output['movie_id'] = recommendation
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)
        return json.dumps(output)