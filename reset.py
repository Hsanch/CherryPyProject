import cherrypy
import json

from _movie_database import _movie_database

class ResetController(object):
    def __init__(self, mdb=None):
        if mdb is None:
            self.mdb = _movie_database()
        else:
            self.mdb = mdb

    def PUT_RESET(self):
        output = {'result' : 'success'}
        try:
            self.mdb.load_movies('ml-1m/movies.dat')
            self.mdb.load_users('ml-1m/users.dat')
            self.mdb.load_ratings('ml-1m/ratings.dat')
            self.mdb.load_votes('ml-1m/ratings.dat')
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)

        return json.dumps(output)


    def PUT_RESET_MOVIE(self, movie_id):
        output = {'result' : 'success'}
        mid = int(movie_id)
        try:
            mdb_tmp = _movie_database()
            mdb_tmp.load_movies('ml-1m/movies.dat')
            movie = mdb_tmp.get_movie(mid)
            self.mdb.set_movie(mid, movie) # also get genre
        except Exception as ex:
            output['result'] = 'error'
            output['message'] = str(ex)

        return json.dumps(output)
