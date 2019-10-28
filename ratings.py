import json
import cherrypy

from _movie_database import _movie_database

class RatingsController(object):
    def __init__(self, mdb=None):
        if mdb is None:
            self.mdb = _movie_database()
        else:
            self.mdb = mdb

    def GET_RATING(self, movie_id):
        output = {"result": "success"}
        try:
            rating = self.mdb.get_rating(int(movie_id))
            output["movie_id"] =  int(movie_id)
            output["rating"] = rating
        except KeyError as ex:
            output['result'] = 'error'
            output['message'] = 'there was a key error'
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)
        
        return json.dumps(output)
