import json, uuid
from json     import JSONDecodeError
from enum     import Enum
from datetime import datetime, timedelta

from django.http      import JsonResponse
from django.db.models import Q
from django.views     import View

from users.utils     import login_decorator
from bookings.models import Booking
from planets.models  import Accomodation

class BookingStatus(Enum):
    PENDING   = 1
    PAID      = 2
    RESERVED  = 3
    CANCELLED = 4

class BookingView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            start_date         = datetime.strptime(data['start_date'], '%Y-%m-%d')
            end_date           = datetime.strptime(data['end_date'], '%Y-%m-%d')
            accomodation       = Accomodation.objects.get(id=data['accomodation_id'])
            number_of_adults   = int(data['number_of_adults'])
            number_of_children = int(data['number_of_children'])
            num_of_people      = number_of_adults + number_of_children
            price              = int(data['price'])

            if num_of_people > accomodation.max_of_people:
                return JsonResponse({'message':'TOO_MANY_PEOPLE'}, status=400)

            if num_of_people > accomodation.min_of_people:
                total_price = price + (num_of_people-accomodation.min_of_people)*100000

            q = Q()

            q &= Q(user_id=user.id)
            q &= Q(start_date__range=(start_date, end_date-timedelta(days=1)))\
                 | Q(end_date__range=(start_date+timedelta(days=1), end_date))

            if Booking.objects.filter(q):
                return JsonResponse({'message':'ALREADY_EXISTS'}, status=400)

            booking = Booking.objects.create(
                booking_number     = uuid.uuid4(),
                start_date         = start_date,
                end_date           = end_date,
                number_of_adults   = number_of_adults,
                number_of_children = number_of_children,
                user_request       = data['user_request'],
                price              = total_price,
                user               = user,
                booking_status_id  = BookingStatus.PENDING.value,
                planet_id          = data['planet_id'],
                accomodation_id    = accomodation.id
            )

            result = {
                'booking_id'     : booking.id,
                'booking_number' : booking.booking_number
            }
            
            return JsonResponse({'result':result}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)

