from django import template
from django.forms import CheckboxInput, Select
from django.forms import TextInput, Textarea

register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})

@register.filter(name='addstr')
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter(name='fieldtype')
def fieldtype(obj):
    return obj.__class__.__name__


@register.filter(name='is_checkbox')
def is_checkbox(field):
  return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__

@register.filter(name='is_textfield')
def is_textfield(field):
  return field.field.widget.__class__.__name__ == TextInput().__class__.__name__

@register.filter(name='is_textarea')
def is_textarea(field):
  return field.field.widget.__class__.__name__ == Textarea().__class__.__name__

@register.filter(name='is_select')
def is_select(field):
  return field.field.widget.__class__.__name__ == Select().__class__.__name__


@register.filter(name='selected_choice')
def selected_choice(form, field_name):
    return dict(form.fields[field_name].choices)[form.data[field_name]]

# @register.filter(name='test')
# def test(form, field_name):
#     return dict(form.fields[field_name].choices)[form.data[field_name]]
# @register.filter(name='test')
# def test(self):
#     return 'hi'
