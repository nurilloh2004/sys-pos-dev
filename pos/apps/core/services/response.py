from rest_framework.response import Response


class RequestController:

    def get_language(self):
        """
        Public method
        @return: request headers language
        """
        return self.__check_language()

    def __check_language(self):
        """Private method"""
        # header = self.request.headers
        lang = 'en'
        # if 'Accept-Language' in header:
        #     lang = header['Accept-Language'][:2]
        # else:
        #     lang = 'en'
        return lang


class ResponseController(RequestController):

    code = 0
    success_message: dict = {"uz": "OK", "de": "ОК", "en": "OK", "ru": "ОК"}  # de = cryllic
    error_message: dict = {"uz": "", "de": "", "en": "", "ru": ""}
    error_text: dict = {"uz": "", "de": "", "en": "", "ru": ""}
    exception: tuple = ""

    def success_response(self, *args, **kwargs):
        lang = self.get_language()
        msg_by_language = self.success_message.get(lang)
        response = {'success': True, 'code': self.code, 'message': msg_by_language}
        if kwargs:
            response.update({key: kwargs[key] for key in kwargs})
        return Response(response)

    def update_error_text(self, catch):
        self.error_text.update(dict.fromkeys(['uz', 'de', 'en', 'ru'], catch))

    def error_response(self):
        lang = self.get_language()
        error_by_language = self.error_text.get(lang)
        try:
            message_by_language = self.error_message.get(lang) % error_by_language
        except TypeError:
            message_by_language = self.error_message.get(lang)
        response = {'success': False, 'code': self.code, 'message': message_by_language}
        if self.exception:
            response['debug'] = self.exception
        return Response(response)
