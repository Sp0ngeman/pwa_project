def username(request):
    """
    Context processor to provide username to templates
    """
    if request.user.is_authenticated:
        return {'username': request.user.username}
    return {'username': 'Guest'} 