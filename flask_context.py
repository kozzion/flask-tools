import datetime
from flask import jsonify

class FlaskContext(object):
    """docstring for FlaskContext."""
    def __init__(self, apiKey):
        super(FlaskContext, self).__init__()
        self.apiKey = apiKey
        self.callCompleteList = []

    def update_call_statistics(self, routeName, startTimestamp, requestValid, routeSucces):
        endTimeStamp = int(datetime.datetime.now().timestamp())
        duration = endTimeStamp - startTimestamp
        # todo use database or persitancy
        self.callCompleteList.append((routeName, startTimestamp, endTimeStamp, duration, requestValid, routeSucces))

    def prepare_call(self, jsonObject, requiredFieldList, validateApiKey=True):
        #Todo use: https://pypi.org/project/jsonschema/
        startTimestamp = int(datetime.datetime.now().timestamp())

        if jsonObject == None:
            responsePayload = {'message':'no json payload'}
            return False, False, responsePayload, 400, startTimestamp

        if validateApiKey:
            if not 'api_key' in jsonObject:
                responsePayload = {'message':'missing field: api_key'}
                return False, False, responsePayload, 400, startTimestamp
            if not(self.apiKey == jsonObject['api_key']):
                responsePayload = {'message':'api_key incorrect'}
                return False, False, responsePayload, 403, startTimestamp

        for requiredField in requiredFieldList:
            if not requiredField in jsonObject:
                responsePayload = {'message':'missing field: ' + requiredField}
                return False, False, responsePayload, 400, startTimestamp

        return True, False, None, 200, startTimestamp


    def complete_call(self, requestValid, routeSucces, routeName, startTimestamp, responsePayload, statusCode):
        self.update_call_statistics(routeName, startTimestamp, requestValid, routeSucces)
        if requestValid:
            if routeSucces:
                statusCode = 200
            else:
                statusCode = 500 #TODO reserve for exeptuon
        return jsonify(responsePayload), statusCode

    def complete_call_status(self):
        responsePayload = {}
        responsePayload['callCount'] = len(self.callCompleteList)
        return jsonify(responsePayload)
