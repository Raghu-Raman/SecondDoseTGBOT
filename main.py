import requests, json
import constants as keys
import response as R
from telegram.ext import *
from datetime import datetime

print('Bot is starting')


def start_command(update, context):
    update.message.reply_text('Yo,welcome to this bot')


current = datetime.now()
today = current.strftime("%d-%m-%Y")
session_dict={}

def send_telegram():
    # update.message.reply_text(vaccine_data)
    # update.message.reply_text('Yo,welcome to this bot')
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
    parameters = {
        'Accept-Language': 'hi_IN',
        'district_id': 571,
        'date': today
    }
    telegram_url = "https://api.telegram.org/bot1865472927:AAHhIgK9zLTmlDuOqJSQjF7m8DYt0Bd0zco/sendMessage?chat_id=@__groupid__&text="
    group_id = "U45_covaxin_2ndDose_Chennai"
    browser_header={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    response = requests.get(url=url, params=parameters, headers=browser_header)
    print(response.json())
    data = response.json()
    text = ''
    print(data)
    for session in data['sessions']:
        if (session['available_capacity_dose2'] > 0 and session['min_age_limit'] < 45 ):
            # print(session)
            if(session['name'] not in session_dict):
                session_dict[session['name']]=True
                text = "Name: " + str(session['name']).capitalize() + '\n' + "Address: " + str(
                    session['address']).title()+ '\n' + "Pincode: " + str(session['pincode']) + '\n' + '\n' + "Fee :" + str(
                    session['fee']) + '\n' + "VACCINE:" + str(session['vaccine'])+'\n'+'Dose2: '+str(session['available_capacity_dose2'])+ '\n' +  'Date:'+ str(session['date'])+'\n'
                final_telegram_url = telegram_url.replace('__groupid__', group_id)
                final_telegram_url = final_telegram_url + text
                response2 = requests.get(final_telegram_url)
                # print(response2.json())
send_telegram()
print(session_dict)

def handle_message(update, context):
    text = str(update.message.text).lower()
    user = update.effective_user
    print(f'{user["username"]}:{text}')
    response = R.sample_responses(text)
    print(f'Bot:{response}')


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    # dp.add_handler(CommandHandler("help", help_command))
    # dp.add_handler(CommandHandler("vaccine", vaccine_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


main()

# response = requests.get(url=url, params=parameters)
# print(response.json())
