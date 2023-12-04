from django.template.defaulttags import register


@register.filter(name='make_range')
def show_error(number):
    return range(number)
