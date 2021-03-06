from pymessenger.bot import Bot
from app import user_query

ACCESS_TOKEN = 'EAALU1QUBIuYBAGgTmLKgqdgFVw7iVu1t0DU1Tt5GT3xFVcx8TtjqX0SGcPfIu42lU3x1xTFhWcFgvyEpQuvjnLDZB3utNM5KIZBZBqVBMSCwcr7bdY5ZAY2npmwPfycPDfFqjbAZBqBP19nvuT2ZCF50d4juzA5jGY15Yloio2cVqwYAc6jOt1'
VERIFY_TOKEN = 'eurekafille'
bot = Bot(ACCESS_TOKEN)

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

def quick_reply_template(text, choices):
    return {
        "text": text,
        "quick_replies":choices
    }

def departure_menu(recipient_id):
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
                "payload":"DepartureIngress_Prev"+str(slicing-1)
            }
        )
    for choice in sliced_stations:
        choices.append(
            {
                "content_type":"text",
                "title":choice,
                "payload":"DepartureIngress_"+choice
            }
        )
    if chunk_size*(slicing+1) < len(stations):
        choices.append(
            {
                "content_type":"text",
                "title":"More...",
                "payload":"DepartureIngress_Next"+str(slicing+1)
            }
        )
    
    out = quick_reply_template('Which station are you coming from?', choices)
    bot.send_message(recipient_id, out)

def parse_egress(recipient_id, ingress, slicing):
    choices = []
    chunk_size = 6
    sliced_stations = [stations[i:i + chunk_size] for i in range(0, len(stations), chunk_size)][slicing]

    if slicing > 0:
        choices.append(
            {
                "content_type":"text",
                "title":"Previous",
                "payload":"DepartureEgress_"+ingress+'_Prev'+str(slicing-1)
            }
        )
    for choice in sliced_stations:
        if choice == ingress:
            continue
        choices.append(
            {
                "content_type":"text",
                "title":choice,
                "payload":"DepartureEgress_"+ingress+'_'+choice
            }
        )
    if chunk_size*(slicing+1) < len(stations):
        choices.append(
            {
                "content_type":"text",
                "title":"More...",
                "payload":"DepartureEgress_"+ingress+'_Next'+str(slicing+1)
            }
        )
    
    out = quick_reply_template("What's your destination?", choices)
    bot.send_message(recipient_id, out)

def parse_final(recipient_id, ingress, egress, time_epoch=None):
    #plug in Titus' part
    #bot.send_text_message(recipient_id, 'In: {}\n Out: {}\nTime: {}'.format(ingress, egress, time_epoch))
    texts = user_query.query(time_epoch, ingress, egress)
    for text in texts:
        bot.send_text_message(recipient_id, text)

# def get_location(recipient_id, coordinates):
#     lat = coordinates['lat']
#     lon = coordinates['long']
#     # find nearest station
#     ingress = 'Roosevelt'
#     parse_egress(recipient_id, ingress, 0) 
#     return
