import json, uuid
from json     import JSONDecodeError
from enum     import Enum
from decimal  import Decimal
from datetime import datetime, timedelta

from django.http      import JsonResponse
from django.db.models import Q
from django.views     import View

from users.utils     import login_decorator
from bookings.models import Booking
from planets.models  import Accomodation

class BookingStatusEnum(Enum):
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

            SURCHARGE_RATE     = 0.1
            start_date         = datetime.strptime(data['start_date'], '%Y-%m-%d')
            end_date           = datetime.strptime(data['end_date'], '%Y-%m-%d')
            accomodation       = Accomodation.objects.get(id=data['accomodation_id'])
            number_of_adults   = int(data['number-of-adults'])
            number_of_children = int(data['number-of-children'])
            total_price        = Decimal(data['total_price'])
            num_of_people      = number_of_adults+number_of_children
            additional_price   = accomodation.price*Decimal(SURCHARGE_RATE)

            if num_of_people > accomodation.max_of_people:
                return JsonResponse({'message':'TOO_MANY_PEOPLE'}, status=400)

            if num_of_people > accomodation.min_of_people:
                total_price += (num_of_people-accomodation.min_of_people)*additional_price

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
                booking_status_id  = BookingStatusEnum.PENDING.value,
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

    @login_decorator
    def get(self, request):
        my_stay = request.GET.get('my-stay')
        limit   = int(request.GET.get('limit', 3))
        offset  = int(request.GET.get('offset', 0))
        today   = datetime.today().strftime("%Y-%m-%d")
        user    = request.user

        q = Q(user=user)

        if my_stay == 'booking-info':
            q &= Q(start_date__gte=today)

        if my_stay == 'history':
            q &= Q(start_date__lt=today)

        bookings = Booking.objects.filter(q)[offset:offset+limit]

        booking_list = [{
            'booking_id'         : booking.id,
            'booking_number'     : booking.booking_number,
            'start_date'         : booking.start_date,
            'end_date'           : booking.end_date,
            'number_of_adults'   : booking.number_of_adults,
            'number_of_children' : booking.number_of_children,
            'user_request'       : booking.user_request,
            'price'              : booking.price,
            'booking_status'     : booking.booking_status.status,
            'planet_name'        : booking.planet.name,
            'accomodation_name'  : booking.accomodation.name
        } for booking in bookings]

        return JsonResponse({'booking_list':booking_list}, status=200)

    @login_decorator
    def patch(self, request, booking_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            status  = data['status']
            booking = Booking.objects.get(user=user, id=booking_id)

            booking_status = {
                'pending'   : BookingStatusEnum.PENDING.value,
                'paid'      : BookingStatusEnum.PAID.value,
                'reserved'  : BookingStatusEnum.RESERVED.value,
                'cancelled' : BookingStatusEnum.CANCELLED.value
            }

            booking.booking_status_id = booking_status[status]
            booking.save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except Booking.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=404)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request):
        user        = request.user
        booking_ids = request.GET.getlist('booking-ids')
        bookings    = Booking.objects.filter(user=user, id__in=booking_ids)
            
        if not bookings:
            return JsonResponse({'message':'NOT_FOUND'}, status=404)

        bookings.delete()

        return JsonResponse({'message':'SUCCESS'}, status=200)
        
