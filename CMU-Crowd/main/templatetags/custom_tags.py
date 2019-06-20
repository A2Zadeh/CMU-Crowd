from django import template

register = template.Library()

@register.filter(name='addcss')
def addcss(value, arg):
    """ Adds a css class to a form field """
    css_classes = value.field.widget.attrs.get('class', '').split(' ')
    if css_classes and arg not in css_classes:
        css_classes = '%s %s' % (css_classes, arg)
    return value.as_widget(attrs={'class': css_classes})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
