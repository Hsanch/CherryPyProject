
class _movie_database:

  def __init__(self):
    self.movies = dict()
    self.users = dict()
    self.ratings = dict()
    self.votes = dict()

  def load_movies(self, movie_file):
    f = open(movie_file)
    for line in f:
      # line => MovieID::Title::Genres
      line = line.rstrip()
      components = line.split("::")
      m_id = int(components[0])
      m_name = components[1]
      m_genres = components[2]

      self.movies[m_id] = [m_name,  m_genres]
    f.close()

  def get_movie(self, m_id):
    if m_id in self.movies:
      return self.movies[m_id]
    else:
      return None
  
  def get_movies(self):
    return self.movies.keys()

  def set_movie(self, m_id, m_props):
    self.movies[m_id] = m_props

  def delete_movie(self, m_id):
    if int(m_id) in self.movies.keys():
      del self.movies[int(m_id)]
    else:
      raise KeyError

  def load_users(self, user_file):
    #  Should this clear the dictionary?
    f = open(user_file)
    for line in f:
      # line => UserID::Gender::Age::Occupation::Zip-code
      line = line.rstrip()
      components = line.split("::")
      u_id = int(components[0])
      u_gender = components[1]
      u_age = int(components[2])
      u_occupation = int(components[3])
      u_zipcode = components[4]

      self.users[u_id] = [u_gender, u_age, u_occupation, u_zipcode]
    f.close()

  def get_user(self, u_id):
    if u_id in self.users:
      return self.users[u_id]
    else: None
  
  def get_users(self):
    return self.users.keys()

  def set_user(self, u_id, u_props):
    self.users[u_id] = u_props

  def delete_user(self, u_id):
    if u_id in self.users:
      del self.users[u_id]
    else:
      print("There is no user with that id")

  def load_ratings(self, rating_file):
    f = open(rating_file)
    for line in f:
      # line => UserID::MovieID::Rating::Timestamp
      line = line.rstrip()
      components = line.split("::")
      u_id = int(components[0])
      m_id = int(components[1])
      rating = int(components[2])

      # movie_rating_object = { u_id: rating, u_id: rating, u_id: rating}
      if m_id in self.ratings:
        current_ratings = self.ratings[m_id]
        current_ratings[u_id] = rating
        self.ratings[m_id] = current_ratings
      else:
        self.ratings[m_id] = { u_id: rating }

    f.close()

  def get_rating(self, m_id):
    if m_id in self.ratings:
      rating_sum = 0
      num_of_ratings = len(self.ratings[m_id])
      for rating in self.ratings[m_id].values():
        rating_sum = rating_sum + rating
      return float(rating_sum/num_of_ratings)
    else:
      return 0

  def get_highest_rated_movie(self):
    if len(self.ratings.keys()) != 0:
      # 5000 is an arbitrary number that is larger than any other movie id
      movie_and_rating = (5000,0) # (m_id, rating) tuple
      for m_id in self.ratings.keys():

        m_rating = self.get_rating(m_id)
        if m_rating > movie_and_rating[1]:
          movie_and_rating = (m_id, m_rating)
        elif m_rating == movie_and_rating[1]:
          movie_and_rating = (m_id, m_rating) if m_id < movie_and_rating[0] else movie_and_rating
      return movie_and_rating[0]
    else:
      return None 
        
  def set_user_movie_rating(self, u_id, m_id, rating):
    if m_id in self.ratings.keys():
      movie_ratings = self.ratings[m_id]
      movie_ratings[u_id] = rating
      self.ratings[m_id] = movie_ratings
    else:
      self.ratings[m_id] = {u_id: rating}

  def get_user_movie_rating(self, u_id, m_id):
    m_ratings = self.ratings.get(m_id, None)
    return m_ratings if m_ratings is None else m_ratings.get(u_id, None)
    
  def delete_all_ratings(self):
    self.ratings.clear()

  def print_sorted_movies(self):
    self.movies = sorted(self.movies)
    for movie in self.movies:
      print(movie)

  def load_votes(self, rating_file):
    f = open(rating_file)
    for line in f:
      # line => UserID::MovieID::Rating::Timestamp
      line = line.rstrip()
      components = line.split("::")
      u_id = int(components[0])
      m_id = int(components[1])
      rating = int(components[2])

      # user_rating_object = { m_id: rating, m_id: rating, m_id: rating}
      if u_id in self.votes:
        current_user_votes = self.votes[u_id]
        current_user_votes[m_id] = rating
        self.votes[m_id] = current_user_votes
      else:
        self.votes[u_id] = { u_id: rating }

    f.close()

  def set_vote(self, u_id, movie_data):
    self.votes[u_id] = movie_data
    m_id = movie_data["movie_id"]
    rating = movie_data["rating"]

    self.set_user_movie_rating(u_id, m_id, rating)

  def get_user_recommendation(self, u_id):
    movie_id = 500000 # number that is higher than any other m_id
    highest_rating = 0
    for m_id in self.ratings.keys():
      if self.get_user_movie_rating(u_id, m_id) is None: # User has not rated that movie
        current_rating = self.get_rating(m_id)
        if current_rating > highest_rating:
          movie_id = m_id
          highest_rating = current_rating
        elif current_rating == highest_rating and m_id < movie_id:
          movie_id = m_id
          highest_rating = current_rating
    return movie_id

  def delete_all_votes(self):
    self.votes.clear()

if __name__ == "__main__":
  mdb = _movie_database()

  mdb.load_movies('ml-1m/movies.dat')
  mdb.load_users('ml-1m/users.dat')
  mdb.load_ratings('ml-1m/ratings.dat')
  mdb.load_votes('ml-1m/ratings.dat')