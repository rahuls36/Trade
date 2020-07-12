

def create_currency_data(currency_data,currency):
    currency_data['id'] = currency[0][:-3]
    currency_data['fullName'] = str(currency[1])
    currency_data['feeCurrency'] = str(currency[2])
    return currency_data

