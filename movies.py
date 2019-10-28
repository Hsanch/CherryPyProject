import cherrypy
import json
from _movie_database import _movie_database #()

class MovieController(object):

        def __init__(self, mdb=None):
                if mdb is None:
                        self.mdb = _movie_database()
                else:
                        self.mdb = mdb

                self.mdb.load_movies('ml-1m/movies.dat')
             #   self.mdb.load_posters('m1-1m/images.dat') #create this method
                #TODO load other resource files


        def GET(self):
                output = {'result' : 'success'}
                try:
                        if self.mdb is None:
                                output['result'] = 'success'
                                output['message'] = 'None type value associated with requested key'
                        else:
                                my_list = []
                                #TODO this where I left off
                                #should this just use get_movie?
                                for mid in self.mdb.get_movies():
                                        movie = self.mdb.get_movie(mid)
                                        my_list.append({'genres' : movie[1], 'title' : movie[0], 'result' : 'success', 'id' : mid, 'img' : self.get_poster_by_mid(mid)})
                                output['movies'] = my_list
                                

                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(output)


        def GET_MID(self, movie_id):
                output = {'result' : 'success'}
                movie_id = int(movie_id)

                try:
                        movie = self.mdb.get_movie(movie_id)
                        if movie is not None:
                                output['id'] = movie_id
                                output['title'] = movie[0]
                                output['genres'] = movie[1]
                                output['img'] = self.get_poster_by_mid(movie_id)
                        else:
                                output['result'] = 'error'
                                output['message'] = 'movie not found'
                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(output)


        def POST(self):
                output = {'result' : 'success'}
                #TODO update the output so that it has the
                #movie_id as well

                #extract msg from body
                data = cherrypy.request.body.read()
                data = json.loads(data)

                try:
                        # genres = data['genres']
                        # title = data['title']
                        lastMovieId = max(self.mdb.get_movies())
                        new_mid = lastMovieId + 1
                        output["id"] = new_mid
                        self.mdb.set_movie(new_mid, data)

                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(output)


        def PUT_MID(self, movie_id):
                output = {'result' : 'success'}
                movie_id = int(movie_id)
                #extract msg from body
                data = cherrypy.request.body.read()
                print(data)
                data = json.loads(data)

                try:
                      #  genre = data['genres']
                      #  title = data['title']
                        self.mdb.set_movie(self, movie_id, data)
                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(output)


        def DELETE(self):
                output = {'result' : 'success'}

                try:
                        self.mdb.movies.clear()
                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(output)


        def DELETE_MID(self, movid_id):
                output = {'result', 'success'}

                try:
                        self.mdb.delete_movie(movie_id)
                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(output)




        def get_poster_by_mid(self, mid):
                if mid in self.posters.keys():
                        return self.posters[mid]
                return '/default.jpg'

        def load_posters(self, posters_file):
                self.posters = {}
                f = open(posters_file)
                for line in f:
                        #TODO string parsing to get m_img
                        mov = line.split('::')
                        self.posters[mov[0]] = mov[2]
                        #self.posters[mid] = m_img