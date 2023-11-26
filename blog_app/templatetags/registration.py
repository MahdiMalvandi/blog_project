from django.template.defaulttags import register

@register.filter(name='show_error')
def show_error(dictionary):
    try:
        return dictionary.values()[0][0]
    except (TypeError,IndexError,AttributeError):
        return 'tip: try again'