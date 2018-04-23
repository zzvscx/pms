
from django import template

register = template.Library()

@register.simple_tag
def get(dict, key, attr=None):
	if dict.get(key):
		return getattr(dict.get(key),attr) if attr else dict.get(key)
	else:
		return ''




