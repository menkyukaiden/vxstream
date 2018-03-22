from django import template

from app.utils.generic import GenericUtils

register = template.Library()


@register.simple_tag
def display_sat_conf_detail(sat, *args, **kwargs):
    gen = GenericUtils()
    print(gen.read_sat_config(str(sat)))
    print(sat)
    return gen.read_sat_config(str(sat))

