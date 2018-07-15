from pymessenger.bot import Bot
import random

ACCESS_TOKEN = 'EAALU1QUBIuYBAGgTmLKgqdgFVw7iVu1t0DU1Tt5GT3xFVcx8TtjqX0SGcPfIu42lU3x1xTFhWcFgvyEpQuvjnLDZB3utNM5KIZBZBqVBMSCwcr7bdY5ZAY2npmwPfycPDfFqjbAZBqBP19nvuT2ZCF50d4juzA5jGY15Yloio2cVqwYAc6jOt1'
VERIFY_TOKEN = 'eurekafille'
bot = Bot(ACCESS_TOKEN)

questions = ['Which coffeeshop brand recently declared war against plastic straws? #singleuse #notostraws# sustainability']
answers = [['Star Frappes','Starbucks Coffee']]

def quick_reply_template(text, choices):
    return {
        "text": text,
        "quick_replies":choices
    }

def start_game(recipient_id):
    rand = random.randint(0, len(questions)-1)

    choices = []

    for choice in answers:
        choices.append(
            {
                "content_type":"text",
                "title":choice,
                "payload":"QuizAnswer_"+choice
            }
        )
    
    out = quick_reply_template(questions[rand], choices)
    bot.send_message(recipient_id, out)

def answer_question(recipient_id, answer):
    if answer != answers[1]:
        bot.send_text_message(recipient_id, 'LRT1: Wrong! Please try again later')
    else:
        bot.send_text_message(recipient_id, 'Correct!')
        bot.send_text_message(recipient_id, 'Present this message to any Starbucks Coffee branch and receive a Free Grande upgrade on your next drink! CODE: ITSTHELASTSTRAW PER DTI-FTRB SPD PERMIT No. 13756. Series of 2018.')