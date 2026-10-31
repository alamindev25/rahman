from django.utils import translation


class LanguageMiddleware:
    """
    Middleware to process language code passed by frontend or Postman.
    Priority order:
    1. Query param: ?lang=bn or ?Accept-Language=bn or ?language=bn
    2. Header: Accept-Language: bn or X-Language: bn
    3. Default fallback: 'en'
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Query parameters (supports ?lang=bn, ?Accept-Language=bn, ?language=bn)
        lang = request.GET.get('lang') or request.GET.get('Accept-Language') or request.GET.get('language')

        # 2. HTTP Headers (supports Accept-Language or X-Language)
        if not lang:
            lang = request.headers.get('Accept-Language') or request.headers.get('X-Language')
        
        if not lang and 'HTTP_ACCEPT_LANGUAGE' in request.META:
            accept_lang = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            if accept_lang:
                lang = accept_lang.split(',')[0].split(';')[0].strip().lower()

        # Sanitize language code (e.g., 'zh-CN' -> 'zh-hans', 'en-US' -> 'en')
        if lang:
            lang = lang.lower()
            if lang.startswith('zh'):
                lang = 'zh-hans'
            else:
                lang = lang.split('-')[0]
        else:
            lang = 'en'

        translation.activate(lang)
        request.LANGUAGE_CODE = lang

        response = self.get_response(request)
        response.headers['Content-Language'] = lang
        return response
