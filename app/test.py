import db

db.reset()
db.add_past_search("kevin", "ur mom's house")
print(db.past_searches_for_user("kevin"))
print(db.past_searches_for_user("faiyaz"))
print(db.user_exists("kevin"))
print(db.user_exists("just a random"))