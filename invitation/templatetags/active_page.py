from django.template.defaulttags import register


@register.simple_tag
def active_page(request, view_name):
    if not request:
        return ""
    return "active" if request.path.startswith(view_name) else ""