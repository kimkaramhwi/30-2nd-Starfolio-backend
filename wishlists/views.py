from django.http  import JsonResponse
from django.views import View

from users.utils      import login_decorator
from planets.models   import Planet
from wishlists.models import WishList

class WishListView(View):
    @login_decorator
    def post(self, request, planet_id):
        try:
            user      = request.user
            planet    = Planet.objects.get(id=planet_id)

            wishlist, is_created = WishList.objects.get_or_create(
                user   = user,
                planet = planet
            )

            if not is_created:
                wishlist.delete()
                return JsonResponse({'message':'DELETED'}, status=204)

            return JsonResponse({'message':'CREATED'}, status=201)

        except Planet.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=404)
    
    @login_decorator
    def get(self, request):
        limit  = int(request.GET.get('limit', 3))
        offset = int(request.GET.get('offset', 0))
        user   = request.user

        wishlists = WishList.objects.filter(user=user)\
                    .select_related('planet')[offset:offset+limit]

        wishlist_lists = [{
            'wishlist_id'       : wishlist.id,
            'planet_id'         : wishlist.planet.id,
            'planet_name'       : wishlist.planet.name,
            'planet_thumbnail'  : wishlist.planet.thumbnail,
            'galaxy_name'       : wishlist.planet.galaxy.name,
            'theme_name'        : wishlist.planet.theme.name,
            'accomodation_info' : [{
                'min_of_people' : accomodation.min_of_people,
                'max_of_people' : accomodation.max_of_people,
                'price'         : accomodation.price,
            } for accomodation in wishlist.planet.accomodation_set.all()]
        } for wishlist in wishlists]

        return JsonResponse({'wishlist_lists':wishlist_lists}, status=200)
