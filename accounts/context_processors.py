def liked_properties(request):
    liked_ids = []
    if request.user.is_authenticated:
        liked_ids = request.user.favorites.values_list('property_id', flat=True)
    return {'liked_ids': liked_ids}