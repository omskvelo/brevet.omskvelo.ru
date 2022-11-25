import os 
import json
from datetime import datetime
from urllib import request

api_key = os.environ['RUVDS_API_KEY']
username = os.environ['RUVDS_LOGIN']
password = os.environ['RUVDS_PASSWORD']
server_id = os.environ['RUVDS_SERVER_ID']
pay_id = os.environ['RUVDS_PAY_ID']

def ruvds_login():
    url = f"https://ruvds.com/api/logon/?key={api_key}&username={username}&password={password}&endless=0"
    response = json.loads(request.urlopen(url).read().decode('utf-8'))

    session_token = response.get('sessionToken')
    os.environ['RUVDS_SESSION_TOKEN'] = session_token
    
def ruvds_get_balance():
    if not os.environ.get('RUVDS_SESSION_TOKEN'):
        ruvds_login()
    session_token = os.environ.get('RUVDS_SESSION_TOKEN')

    url = f"https://ruvds.com/api/balance/?sessionToken={session_token}&details=0&currency=RUB"
    response = json.loads(request.urlopen(url).read().decode('utf-8'))
    currency = ["", "RUB", "UAH", "USD", "EUR"][response.get("currency")]

    return f"{response.get('amount')} {currency}"

def DT_to_datetime(DT):
    return datetime.strptime(DT, "%d%m%Y%H%M%S")


def rudvs_get_server_info():
    if not os.environ.get('RUVDS_SESSION_TOKEN'):
        ruvds_login()
    session_token = os.environ.get('RUVDS_SESSION_TOKEN')

    url = f"https://ruvds.com/api/servers/?sessionToken={session_token}&id={server_id}"
    response = json.loads(request.urlopen(url).read().decode('utf-8'))

    payment_periods = ['', 'Пробный', '1 месяц', '3 месяца', '6 месяцев', '1 год']
    
    server_data = []
    for server in response.get('items'):
        data = {}
        data['CPU'] = F"{server['cpu']} ядро"
        data['RAM'] = F"{server['ram']} Гб"
        data['IP'] = server['ip']['assigned'][0]
        data['Создан'] = DT_to_datetime(server['addDT'])
        data['Оплачен до'] = DT_to_datetime(server['paidTill'])
        data['Тариф'] = F"{server['priceRub']} RUB"
        data['Период оплаты'] = payment_periods[server['paymentPeriod']]
        server_data.append(data)

    return server_data
        

def ruvds_get_payment_url():
    return f"https://ruvds.com/ru-rub/pay/{pay_id}"