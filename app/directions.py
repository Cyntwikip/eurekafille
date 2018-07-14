from pymessenger.bot import Bot
import numpy as np

ACCESS_TOKEN = 'EAALU1QUBIuYBAGgTmLKgqdgFVw7iVu1t0DU1Tt5GT3xFVcx8TtjqX0SGcPfIu42lU3x1xTFhWcFgvyEpQuvjnLDZB3utNM5KIZBZBqVBMSCwcr7bdY5ZAY2npmwPfycPDfFqjbAZBqBP19nvuT2ZCF50d4juzA5jGY15Yloio2cVqwYAc6jOt1'
VERIFY_TOKEN = 'eurekafille'
bot = Bot(ACCESS_TOKEN)

# Jeff's
GMAP_TOKEN = 'AIzaSyCN3dUVDpLmTSBlzQrzs7-dWwv09LbNPCM'

stations = ["Roosevelt", 
             "Balintawak", 
             "Monumento", 
             "5th Avenue", 
             "R Papa", 
             "Abad Santos", 
             "Blumentritt", 
             "Tayuman", 
             "Bambang", 
             "Doroteo Jose", 
             "Carriedo", 
             "Central Terminal", 
             "United Nations", 
             "Pedro Gil", 
             "Quirino", 
             "Vito Cruz", 
             "Gil Puyat", 
             "Libertad", 
             "EDSA", 
             "Baclaran"
            ]
station_latitude = [14.6575456, 14.6574375, 14.654367, 14.6444202, 14.6360498,
                    14.6306034, 14.6227455, 14.6166646, 14.6054402, 14.6054402, 
                    14.5992496, 14.5927759, 14.58255, 14.5763209, 14.5703345, 
                    14.5633793, 14.5541626, 14.5476629, 14.5385754, 14.5342859] 

station_longitude = [121.021191, 121.0038748, 120.983894, 120.9835832, 120.9822971, 
                     120.9814853, 120.9835353, 120.9827277, 120.982061, 120.982061,
                     120.981363, 120.9816613, 120.984621, 120.9881877, 120.991558, 
                     120.9948178, 120.9971671, 120.9986104, 121.0006372, 120.9983415]

def quick_reply_template(text, choices):
    return {
        "text": text,
        "quick_replies":choices
    }

def directions_menu(recipient_id):
    parse_ingress(recipient_id, 0)

def parse_ingress(recipient_id, slicing):
    choices = []
    chunk_size = 6
    sliced_stations = [stations[i:i + chunk_size] for i in range(0, len(stations), chunk_size)][slicing]

    if slicing > 0:
        choices.append(
            {
                "content_type":"text",
                "title":"Previous",
                "payload":"DirectionIngress_Prev"+str(slicing-1)
            }
        )
    else:
        choices.append(
            {
                "content_type":"location"
            }
        )
    for choice in sliced_stations:
        choices.append(
            {
                "content_type":"text",
                "title":choice,
                "payload":"DirectionIngress_"+choice
            }
        )
    if chunk_size*(slicing+1) < len(stations):
        choices.append(
            {
                "content_type":"text",
                "title":"More...",
                "payload":"DirectionIngress_Next"+str(slicing+1)
            }
        )
    
    out = quick_reply_template('To which station?', choices)
    bot.send_message(recipient_id, out)

def parse_station(recipient_id, station):
    print(station)
    station_index = stations.index(station)
    lat = station_latitude[station_index]
    lon = station_longitude[station_index]
    url = "https://maps.googleapis.com/maps/api/staticmap?key=" + GMAP_TOKEN +
                "&markers=color:red|label:B|" + str(lat) + "," + str(lon) + "&size=360x360&zoom=13"
    messageData = {
        "attachment": {
        "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [{
                    "title": station,
                    "subtitle": "LRT Station",
                    "image_url": url,
                    "default_action": {
                    "type": "web_url",
                    "url": url,
                    "messenger_extensions": true,
                    "webview_height_ratio": "tall"
                    }
                }]
            }
        }
    }
    bot.send_message(recipient_id, messageData)
    return

def get_location(recipient_id, coordinates):
    lat = coordinates['lat']
    lon = coordinates['long']
    
    # find nearest station
    min_dist_index=0
    for i, each in enumerate(stations):
        dist = np.linalg.norm(np.array([lat, lon]) - np.array([station_latitude[i],station_longitude[i]]))
        if i == 0: 
            min_dist = dist
        if min_dist > dist:
            min_dist_index = i
            min_dist = dist

    station = stations[min_dist_index]
    parse_station(recipient_id, station)
    return

