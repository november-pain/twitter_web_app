import urllib.request, urllib.parse, urllib.error, twurl, json, ssl
import folium
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim


geolocator = Nominatim(timeout=100, user_agent="Macs")
geocode = RateLimiter(geolocator.geocode, error_wait_seconds=0.5,
                      max_retries=0, swallow_exceptions=False, return_value_on_exception=True)



def get_file_json(name_acc, num_of_friends):
    """
    (str) -> json
    :param name_acc:
    :param num_of_friends:
    :return: json file with information about user
    """
    url = 'https://api.twitter.com/1.1/friends/list.json'
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    url = twurl.augment(url, {'name': name_acc, 'num': num_of_friends})
    data = urllib.request.urlopen(url, context=context).read().decode()
    # sonjey = json.loads(data, encoding='utf-8')
    return data


def get_location(path):
    f_js = json.loads(path)
    users_locations_dct = {}
    for user in f_js['users']:
        users_locations_dct[user['screen_name']] = user['location']
    return users_locations_dct


def friend_mark(friend_dict, map, acc):

    friends_layer = folium.FeatureGroup(name="friends of {}".format(acc))
    for friend in friend_dict:
        location = geolocator.geocode(friend_dict[friend])
        if location is None:
            pass
        else:
            friends_layer.add_child(folium.Marker(location=[location.latitude, location.longitude],
                                                popup=friend))
    map.add_child(friends_layer)


def main(acc, num):
    son_jey = get_file_json(acc, num)
    map = folium.Map()
    friend_mark(get_location(son_jey), map, acc)
    return map._repr_html_()



if __name__ == '__main__':
    pass
