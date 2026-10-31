from django.utils import translation


def get_localized_value(field_value, lang_code=None, default_lang='en'):
    """
    Extracts the localized string from a field_value (dict or str).
    If field_value is a dict e.g. {'en': 'Hello', 'es': 'Hola', 'bn': 'হ্যালো'},
    returns value corresponding to lang_code or fallback to default_lang.
    """
    if isinstance(field_value, dict):
        if not lang_code:
            lang_code = translation.get_language() or default_lang

        lang_code = lang_code.lower()

        # 1. Exact match
        if lang_code in field_value and field_value[lang_code]:
            return field_value[lang_code]

        # 2. Base language code match (e.g. 'zh-hans' -> 'zh')
        base_lang = lang_code.split('-')[0]
        if base_lang in field_value and field_value[base_lang]:
            return field_value[base_lang]

        # 3. Default language fallback
        if default_lang in field_value and field_value[default_lang]:
            return field_value[default_lang]

        # 4. Return any first available translation
        for val in field_value.values():
            if val:
                return val

        return ""

    return field_value


class MultilingualSerializerMixin:
    """
    Mixin for DRF Serializers to automatically localize JSONField or multilingual dict fields.
    Define `multilingual_fields = ['title', 'description', 'content']` on Serializer Meta.
    """
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        lang_code = getattr(request, 'LANGUAGE_CODE', None) if request else translation.get_language()

        multilingual_fields = getattr(self.Meta, 'multilingual_fields', [])
        for field in multilingual_fields:
            if field in ret:
                ret[field] = get_localized_value(ret[field], lang_code=lang_code)

        return ret
