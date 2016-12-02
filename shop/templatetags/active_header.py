from django.template.defaulttags import register


@register.simple_tag
def active_header(request, view_name):
    if not request:
        return ""
    return "active" if request.path_info.endswith(view_name) else ""
