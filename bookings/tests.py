import jwt, json

from django.test import TestCase, Client
from my_settings     import SECRET_KEY, ALGORITHM

from planets.models  import Planet, Accomodation, Galaxy, PlanetTheme
from bookings.models import BookingStatus, Booking
from users.models    import User

class BookingTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = '가람',
            email    = 'kimkrh@naver.com',
            kakao_id = 1234
        )

        Galaxy.objects.create(
            id   = 1,
            name = '가람우주'
        )

        PlanetTheme.objects.create(
            id   = 1,
            name = '무한테스트'
        )

        Planet.objects.create(
            id        = 1,
            name      = '가람별',
            thumbnail = 'http://urls',
            theme_id  = 1,
            galaxy_id = 1
        )

        Accomodation.objects.create(
            id            = 1,
            name          = '가람의호텔',
            price         = 1000,
            min_of_people = 2,
            max_of_people = 4,
            num_of_bed    = 2,
            description   = "편안합니다.",
            planet_id     = 1
        )

        BookingStatus.objects.create(
            id     = 1,
            status = 'PENDING'
        )        

        Booking.objects.create(
            id                 = 1,
            booking_number     = 5678,
            star_date          = '2022-03-20',
            end_date           = '2022-03-22',
            number_of_adults   = 1,
            number_of_children = 1,
            user_request       = '살려주세요.',
            price              = 2000,
            user_id            = 1,
            booking_status_id  = 1,
            planet_id          = 1,
            accomodation_id    = 1
        )

        def tearDown(self):
            User.objects.all().delete()
            Galaxy.objects.all().delete()
            PlanetTheme.objects.all().delete()
            Planet.objects.all().delete()
            Accomodation.objects.all().delete()
            BookingStatus.objects.all().delete()
            Booking.objects.all().delete()

        def test_bookingview_post_success(self):
            token   = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
            client  = Client()
            headers = {'HTTP_Authorization':token}
            booking = {
                'start_date'         : '2022-03-20',
                'end_date'           : '2022-03-21',
                'number_of_adults'   : 1,
                'number_of_children' : 1,
                'user_request'       : '테스트',
                'price'              : 10000,
                'booking_status_id'  : 1,
                'planet_id'          : 1,
                'accomodation_id'    : 1
            }
            response = client.post(
                '/bookings', 
                json.dump(booking), 
                content_type='application/json', 
                **headers
            )
            self.assertEqual(response.status_code, 201)

        def test_bookingview_post_error(self):
            token   = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
            client  = Client()
            headers = {'HTTP_Authorization':token}
            booking = {
                'start_date'         : '2022-03-20',
                'end_date'           : '2022-03-21',
                'number_of_adults'   : 1,
                'number_of_children' : 1,
                'user_request'       : '테스트',
                'pric'               : 10000,
                'booking_status_id'  : 1,
                'planet_id'          : 1,
                'accomodation_id'    : 1
            }
            response = client.post(
                '/bookings', 
                json.dump(booking), 
                content_type='application/json', 
                **headers
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {'message':'KEY_ERROR'})

