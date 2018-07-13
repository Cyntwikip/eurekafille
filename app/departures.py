from pymessenger.bot import Bot

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
    choices = []
    for choice in stations[:5]:
        choices.append(
            {
                "content_type":"text",
                "title":choice,
                "payload":"DepartureIngress_"+choice
            }
        )
    out = quick_reply_template('Departure Times: Entry Station', choices)
    bot.send_message(recipient_id, out)

def departure_ingress(recipient_id, ingress):
    choices = []
    for choice in stations[:5]:
        if choice == ingress:
            continue
        choices.append(
            {
                "content_type":"text",
                "title":choice,
                "payload":"DepartureEgress_"+ingress+'_'+choice
            }
        )
    out = quick_reply_template('Departure Times: Exit Station', choices)
    bot.send_message(recipient_id, out)

def departure_egress(recipient_id, ingress, egress):
    bot.send_message(recipient_id, 'In: {}, Out: {}'.format(ingress, egress))
    
    #bot.send_button_message(recipient_id, 'Hi! How may I help you?', choices)
