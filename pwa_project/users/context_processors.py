def username(request):
    if request.user.is_authenticated:
        return {'username': request.user.username}
    return {'username': None}