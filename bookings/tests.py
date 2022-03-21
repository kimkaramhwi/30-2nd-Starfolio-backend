import jwt, json

from django.test import TestCase, Client

from my_settings     import SECRET_KEY, ALGORITHM
from planets.models  import Planet, Accomodation, Galaxy, PlanetTheme
from bookings.models import BookingStatus, Booking
from users.models    import User

class BookingTest(TestCase):
    @classmethod
    def setUpTestData(cls):	
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
            start_date         = '2022-03-20',
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

    def test_success_bookingview_post(self):
        token   = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client  = Client()
        headers = {'HTTP_Authorization':token}
        booking = {
            'booking_number'     : 1,
            'start_date'         : '2022-03-22',
            'end_date'           : '2022-03-23',
            'number-of-adults'   : 1,
            'number-of-children' : 1,
            'user_request'       : '테스트',
            'total_price'        : 10000,
            'planet_id'          : 1,
            'accomodation_id'    : 1
        }
        response = client.post(
            '/bookings', 
            json.dumps(booking), 
            content_type='application/json', 
            **headers
        )
        booking_number = Booking.objects.get(id=2).booking_number
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'result':{
                'booking_id'     : 2,
                'booking_number' : str(booking_number)
            }
        })

    def test_fail_bookingview_post_too_many_people(self):
        token   = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client  = Client()
        headers = {'HTTP_Authorization':token}
        booking = {
            'start_date'         : '2022-03-22',
            'end_date'           : '2022-03-23',
            'number-of-adults'   : 10,
            'number-of-children' : 1,
            'user_request'       : '테스트',
            'total_price'        : 10000,
            'planet_id'          : 1,
            'accomodation_id'    : 1
        }
        response = client.post(
            '/bookings', 
            json.dumps(booking), 
            content_type='application/json', 
            **headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'TOO_MANY_PEOPLE'})

    def test_fail_bookingview_post_already_exists(self):
        token   = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client  = Client()
        headers = {'HTTP_Authorization':token}
        booking = {
            'start_date'         : '2022-03-21',
            'end_date'           : '2022-03-22',
            'number-of-adults'   : 1,
            'number-of-children' : 1,
            'user_request'       : '테스트',
            'total_price'        : 10000,
            'planet_id'          : 1,
            'accomodation_id'    : 1
        }
        response = client.post(
            '/bookings', 
            json.dumps(booking), 
            content_type='application/json', 
            **headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'ALREADY_EXISTS'})

    def test_success_bookingview_get(self):
        token   = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client  = Client()
        headers = {'HTTP_Authorization':token}
        response = client.get(
            '/bookings', 
            **headers
        )
        booking_number = Booking.objects.get(id=1).booking_number
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'booking_list': [{
                'booking_id'         : 1,
                'booking_number'     : str(booking_number),
                'start_date'         : '2022-03-20',
                'end_date'           : '2022-03-22',
                'number_of_adults'   : 1,
                'number_of_children' : 1,
                'user_request'       : '살려주세요.',
                'price'              : '2000.00',
                'booking_status'     : 'PENDING',
                'planet_name'        : '가람별',
                'accomodation_name'  : '가람의호텔'
            }]
        })

    def test_success_bookingview_patch(self):
        token   = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client  = Client()
        headers = {'HTTP_Authorization':token}
        booking = {
            'status' : 'pending'
        }
        response = client.patch(
            '/bookings/1', 
            json.dumps(booking), 
            content_type='application/json', 
            **headers
        )
        self.assertEqual(response.status_code, 200)

    def test_fail_bookingview_patch_not_found(self):
        token   = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client  = Client()
        headers = {'HTTP_Authorization':token}
        booking = {
            'status' : 'pending'
        }
        response = client.patch(
            '/bookings/2', 
            json.dumps(booking), 
            content_type='application/json', 
            **headers
        )
        self.assertEqual(response.status_code, 404)

    def test_success_bookingview_delete(self):
        token   = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client  = Client()
        headers = {'HTTP_Authorization':token}
        response = client.delete(
            '/bookings?booking-ids=1',
            **headers
        )
        self.assertEqual(response.status_code, 200)

    def test_fail_bookingview_delete_not_found(self):
        token   = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client  = Client()
        headers = {'HTTP_Authorization':token}
        response = client.delete(
            '/bookings?booking-ids=2',
            **headers
        )
        self.assertEqual(response.status_code, 404)