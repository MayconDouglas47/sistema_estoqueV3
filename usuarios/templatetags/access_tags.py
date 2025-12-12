from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def has_access(context, allowed_levels):
    """Usage: {% has_access "admin,estoquista" as can_view %} then {% if can_view %}
    Returns True if request.user.nivel_acesso is in allowed_levels (comma-separated).
    """
    request = context.get('request')
    if not request or not hasattr(request, 'user') or not request.user.is_authenticated:
        return False
    nivel = getattr(request.user, 'nivel_acesso', None)
    if not nivel:
        return False
    allowed = [x.strip() for x in allowed_levels.split(',') if x.strip()]
    return nivel in allowed
