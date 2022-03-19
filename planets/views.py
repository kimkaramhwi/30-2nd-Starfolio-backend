from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from datetime         import datetime, timedelta

from planets.models import Planet

class PlanetListView(View):
    def get(self, request):
        check_in  = request.GET.get('check-in')
        check_out = request.GET.get('check-out')
        sort      = request.GET.get('sort', 'id')
        limit     = int(request.GET.get('limit', 10))
        offset    = int(request.GET.get('offset', 0))

        filter_options = {
            'galaxy'    : 'galaxy_id',
            'theme'     : 'theme_id',
            'searching' : 'name__icontains',
            'people'    : 'accomodation__max_of_people__gte',
            'min-price' : 'accomodation__price__gte',
            'max-price' : 'accomodation__price__lte'
        }

        filter_set = {
            filter_options.get(key): value\
                for (key, value) in request.GET.items()\
                     if filter_options.get(key)
        }

        booking = Q()

        if check_in and check_out:

            if check_in >= check_out:
                return JsonResponse({'message':'INVALID_DATE'}, status=400)

            check_in  = datetime.strptime(check_in, '%Y-%m-%d')
            check_out = datetime.strptime(check_out, '%Y-%m-%d')

            booking |= Q(booking__start_date__range=(check_in, check_out-timedelta(days=1)))
            booking |= Q(booking__end_date__range=(check_in+timedelta(days=1), check_out))

        sort_type = {
            'id'   : 'id',
            'new'  : '-created_at',
            'desc' : '-accomodation__price',
            'asc'  : 'accomodation__price' 
        }

        planets = Planet.objects.prefetch_related('accomodation_set')\
                        .prefetch_related('booking_set')\
                        .filter(**filter_set)\
                        .exclude(booking)\
                        .order_by(sort_type[sort])[offset:offset+limit]

        planets_list = [{
            'id'                : planet.id,
            'name'              : planet.name,
            'thumbnail'         : planet.thumbnail,
            'galaxy'            : planet.galaxy.name,
            'theme'             : planet.theme.name,
            'image'             : [image.image_url for image in planet.planetimage_set.all()],
            'accomodation_info' : [{
                'min_of_people' : accomodation.min_of_people,
                'max_of_people' : accomodation.max_of_people,
                'price'         : accomodation.price
            } for accomodation in planet.accomodation_set.all()]
        } for planet in planets]

        return JsonResponse({'planets_list':planets_list}, status=200)