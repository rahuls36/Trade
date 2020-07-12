from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse,HttpResponseNotAllowed
from django.db import IntegrityError
from django.views import View
from .models import Symbol
import json
from collections import defaultdict
import redis
import requests
from .utils import create_currency_data
from django.shortcuts import reverse

# Redis Connection
redis_conn = redis.Redis(host='redis', decode_responses=True)


class Trade(View):
    def get(self, request, symbol):
        """
        This Endpoint serves the GET Api Call and returns the appropriate response
        :param request: The request Object for this call
        :param symbol: symbol provided by the user
        :return: The Json encoded Response Data
        """
        # Check for the Incoming symbol and fetch data from local Database
        if symbol == "all":
            _all = [(symbols.name, symbols.fullName, symbols.feeCurrency) for symbols in Symbol.objects.all()]
        else:
            _all = [(symbols.name, symbols.fullName, symbols.feeCurrency) for symbols in
                    Symbol.objects.filter(name=symbol)]
        if not _all:
            return HttpResponseBadRequest("Symbol Data Does not Exist")
        response_data = defaultdict(list)

        # Iterate over the symbols and get the required data
        for currency in _all:
            currency_data = redis_conn.hgetall(currency[0])
            currency_data = create_currency_data(currency_data, currency)
            response_data["currencies"].append(currency_data)
        return JsonResponse(response_data, safe=False)

    def post(self, request, symbol):
        """
        This Endpoint serves the POST Api Call to Add a Symbol in the backend
        :param request: request object
        :return:
        """

        if "all" in request.path:
            return HttpResponseBadRequest('Please check the Request Method and Url')

        # Parse the data from the request body
        data = json.loads(request.body.decode()) if request.body else ""
        if not data:
            return HttpResponseBadRequest("Please Enter the Symbol")

        # Get Currency,Currency_id and make the request
        currency, currency_id = str(data.get("symbol")[:-3]), str(data.get("symbol")[-3:])
        url = "https://api.hitbtc.com/api/2/public/currency/" + currency
        symbol_response = requests.get(url)

        # If Request is valid save in the local database
        if symbol_response.status_code == 200:
            symbol_data = json.loads(symbol_response.text)
            try:
                Symbol.objects.create(name=data.get('symbol'), fullName=symbol_data.get('fullName'),
                                      feeCurrency=currency_id)
                response = HttpResponse("Symbol Created")
                response.status_code = 201
                return response
            except IntegrityError:
                return HttpResponseBadRequest("The Symbol Already exists. Please Enter a new Symbol")

        return HttpResponseBadRequest("Please Enter the correct Symbol")
