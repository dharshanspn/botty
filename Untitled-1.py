import requests
import time
def telegram_bot_sendtext(bot_message):
    bot_token = '6283203048:AAGgOl-o6Itm3D1mw4_Omcf-g4t260vixN8'
    bot_chatID = '1155462778'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + \
                '&parse_mode=MarkdownV2&text=' + str(bot_message).replace('.', '\\.')  # Escape the dot character
    response = requests.get(send_text)
    return response.json()
print("Good till now : sending medsage")
time.sleep(5)
telegram_bot_sendtext("Connection successful")
time.sleep(5)
i=6369877.269
telegram_bot_sendtext(i)
start_time=time.time()
while True:
        bot_seconds = 27
        if 25<bot_seconds<28:
            elapsed_time = time.time() - start_time
            if elapsed_time<60:
              status = f"UP Running...  {elapsed_time:.2f}s"
              telegram_bot_sendtext(status)
            elif 60 < elapsed_time < 3600:
              min = elapsed_time // 60
              status = f"UP Running...  {min:.2f} min"
              telegram_bot_sendtext(status)
            elif 3600 < elapsed_time < 86400 :
              hours = elapsed_time // 3600
              mins = (elapsed_time-hours*3600)//60
              status = f"UP Running...  {hours:.2f} hr {mins:.2f} min"
              telegram_bot_sendtext(status)
    time.sleep(2)