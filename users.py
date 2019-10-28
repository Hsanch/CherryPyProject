import cherrypy
import json
from _movie_database import _movie_database

class UserController(object):

        def __init__(self, mdb=None):
                if mdb is None:
                    self.mdb = _movie_database()
                else:
                    self.mdb = mdb
                self.mdb.load_users('ml-1m/users.dat')

        def GET(self):
                output = {'result' : 'success'}

                try:
                        if self.mdb is None:
                                output['result'] = 'success'
                                output['message'] = 'None type value associated with requested user'
                        else:
                                output['result'] = ['success']
                                myList = []
                                for user_id in self.mdb.get_users():
                                        user = self.mdb.get_user(user_id)
                                        myList.append({'zipcode':user[3], 'age':user[1], 'gender':user[0], 'id':user_id, 'occupation':user[2]})
                                output['users'] = myList
                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(output)

        def GET_USER(self, user_id):
                output = {'result' : 'success'}
                user_id = int(user_id)

                try:
                        user = self.mdb.get_user(user_id)
                        if user is not None:
                                output['gender'] = user[0]
                                output['age'] = user[1]
                                output['zipcode'] = user[3]
                                output['result'] = 'success'
                                output['id'] = user_id
                                output['occupation'] = user[2]
                        else:
                                output['result'] = 'error'
                                output['message'] = 'user not found'
                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(output)

        def POST(self):
                output = {'result' : 'success'}
                #add id to output

                #extract msg from body
                data = cherrypy.request.body.read()
                data = json.loads(data)

                try:
                        # generate id:
                        new_uid = len(self.mdb.get_users()) + 1
                        # gender = data['gender']
                        # age = data['age']
                        # zipcode = data['zipcode']
                        # occupation = data['occupation']
                        # u_properties = [gender, age, occupation, zipcode]
                        self.mdb.set_user(new_uid, data)
                        output['id'] = new_uid
                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)
                return json.dumps(output)

        def PUT_USER(self, user_id):
                output = {'result' : 'success'}
                user_id = int(user_id)

                #extract message from body
                data = cherrypy.request.body.read()
                print(data)
                data = json.loads(data)

                try:
                        self.mdb.set_user(self, user_id, data)
                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(output)

        def DELETE(self):
                output = {'result' : 'success'}

                try:
                        self.mdb.users.clear()
                except Exception as ex:
                        output['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(output)

        def DELETE_USER(self, user_id):
                output = {'result' : 'success'}

                try:
                        self.mdb.delete_user(user_id)
                except Exception as ex:
                        outupt['result'] = 'error'
                        output['message'] = str(ex)

                return json.dumps(outupt)