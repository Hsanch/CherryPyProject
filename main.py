import cherrypy
import json

from votes import VotesController
from ratings import RatingsController
from reset import ResetController
from movies import MovieController
from users import UserController

from _movie_database import _movie_database

def start_service():

    mdb = _movie_database()
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    votes = VotesController(mdb=mdb)
    ratings = RatingsController(mdb=mdb)
    reset = ResetController(mdb=mdb)
     #instantiate controllers
    movieController = MovieController(mdb=mdb)
    userController = UserController(mdb=mdb)

    #connecting endpoings

    #connect /movies/:movie_id resource
    dispatcher.connect('movie_get_mid', '/movies/:movie_id', controller=movieController, action='GET_MID', conditions=dict(method=['GET']))
    dispatcher.connect('movie_put_mid', '/movies/:movie_id', controller=movieController, action='PUT_MID', conditions=dict(method=['PUT']))
    dispatcher.connect('movie_delete_mid', '/movies/:movie_id', controller=movieController, action='DELETE_MID', conditions=dict(method=['DELETE']))
    dispatcher.connect('movie_get', '/movies/', controller=movieController, action='GET', conditions=dict(method=['GET']))
    dispatcher.connect('movie_post', '/movies/', controller=movieController, action='POST', conditions=dict(method=['POST']))
    dispatcher.connect('movie_delete', '/movies/', controller=movieController, action='DELETE', conditions=dict(method=['DELETE']))


    dispatcher.connect('user_get_uid', '/users/:user_id', controller=userController, action='GET_UID', conditions=dict(method=['GET']))
    dispatcher.connect('user_put_uid', '/users/:user_id', controller=userController, action='PUT_UID', conditions=dict(method=['PUT']))
    dispatcher.connect('user_delete_uid', '/users/:user_id', controller=userController, action='DELETE_UID', conditions=dict(method=['DELETE']))
    dispatcher.connect('user_get', '/users/', controller=userController, action='GET', conditions=dict(method=['GET']))
    dispatcher.connect('user_post', '/users/', controller=userController, action='POST', conditions=dict(method=['POST']))
    dispatcher.connect('user_delete', '/users/', controller=userController, action='DELETE', conditions=dict(method=['DELETE']))



    # /recommendations/ routes
    dispatcher.connect('delete_rec', '/recommendations/', controller=votes, action='DELETE_RECOMMENDATIONS', conditions=dict(method=['DELETE']))
    # /recommentdations/:user_id routes
    dispatcher.connect('get_user_rec', '/recommendations/:user_id', controller=votes, action='GET_RECOMMENDATIONS', conditions=dict(method=['GET']))
    dispatcher.connect('put_user_rec', '/recommendations/:user_id', controller=votes, action='PUT_RECOMMENDATIONS', conditions=dict(method=['PUT']))
    # /ratings/:movie_id routes
    dispatcher.connect('get_movie_rating', '/ratings/:movie_id', controller=ratings, action='GET_RATING', conditions=dict(method=['GET']))
    # /reset/ routes
    dispatcher.connect('put_reset', '/reset/', controller=reset, action='PUT_RESET', conditions=dict(method=['PUT']))
    # /reset/:movie_id
    dispatcher.connect('put_reset_movie', '/reset/:movie_id', controller=reset, action='PUT_RESET_MOVIE', conditions=dict(method=['PUT']))

    #configuration
    conf = {
        'global' : {
            'server.socket_host' : '127.0.0.1',
            'server.socket_port' : 8000,
            },
        '/' : {'request.dispatch' : dispatcher}
    }

    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

if __name__ == '__main__':
    start_service()
