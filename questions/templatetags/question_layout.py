import json
from json import JSONDecodeError

from django.template import Context
from django.template.defaulttags import register
from django.template.loader import get_template


@register.simple_tag
def question_layout(ticket, question):
    try:
        data = json.loads(question.data)
    except JSONDecodeError:
        data = []
    return get_template('questions/{}.html'.format(question.type))\
        .render(Context({'ticket': ticket, 'question': question, 'data': data}))

