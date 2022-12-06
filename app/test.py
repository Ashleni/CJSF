import api

api.reset()
api.add_past_search("kevin", "ur mom's house")
print(api.past_searches_for_user("kevin"))