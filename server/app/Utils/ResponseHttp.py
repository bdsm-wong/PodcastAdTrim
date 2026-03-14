from flask import jsonify

class ResponseHttp:
    @staticmethod
    def error_message(message, status_code):
        response = jsonify({
            'error': True,
            'message': message
        })
        response.status_code = status_code
        return response
    
    def successful_message(message):
        response = jsonify({
            'error': False,
            'message': message
        })
        response.status_code = 200
        return response
    
    @staticmethod
    def error_message_dictionary(message):
        return {
            'error': True,
            'message': message
        }