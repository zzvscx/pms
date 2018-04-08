
from django import template

register = template.Library()

@register.simple_tag
def get(dict, key, attr=None):
	if dict.get(key):
		return getattr(dict.get(key),attr) if attr else dict.get(key)
	else:
		return ''

@register.simple_tag
def getnum(cla, attr, l, r):
	if attr == 'total_score':
		return cla.filter(total_score__gte=l,total_score__lte=r).count()




