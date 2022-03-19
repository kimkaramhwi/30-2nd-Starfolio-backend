import jwt

from django.test import TestCase, Client

from my_settings      import SECRET_KEY, ALGORITHM
from planets.models   import Galaxy, PlanetTheme, Planet, Accomodation
from wishlists.models import WishList
from users.models     import User

class WishListTest(TestCase):
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

        Planet.objects.bulk_create([
            Planet(
                id        = 1,
                name      = '가람별',
                thumbnail = 'http://urls',
                theme_id  = 1,
                galaxy_id = 1
            ),
            Planet(
                id        = 2,
                name      = '가람별2',
                thumbnail = 'http://urls2',
                theme_id  = 1,
                galaxy_id = 1
            )
        ])

        Accomodation.objects.create(
            id            = 1,
            name          = '가람의호텔',
            price         = 100000.00,
            min_of_people = 2,
            max_of_people = 4,
            num_of_bed    = 2,
            description   = "편안합니다.",
            planet_id     = 1
        )

        WishList.objects.create(
            id        = 1,
            user_id   = 1,
            planet_id = 1
        )

    def tearDown(self):
        User.objects.all().delete()
        Galaxy.objects.all().delete()
        PlanetTheme.objects.all().delete()
        Planet.objects.all().delete()
        Accomodation.objects.all().delete()

    def test_success_wishlistview_post_create(self):
        token    = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client   = Client()
        headers  = {'HTTP_Authorization':token}
        response = client.post(
            '/wishlists/2',
            **headers
        )
        self.assertEqual(response.status_code, 201)

    def test_success_wishlistview_post_delete(self):
        token    = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client   = Client()
        headers  = {'HTTP_Authorization':token}
        response = client.post(
            '/wishlists/1',
            **headers
        )
        self.assertEqual(response.status_code, 204)

    def test_success_wishlistview_get(self):
        token    = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client   = Client()
        headers  = {'HTTP_Authorization':token}
        response = client.get(
            '/wishlists',
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'wishlist_lists':[{
                'wishlist_id'       : 1,
                'planet_id'         : 1,
                'planet_name'       : '가람별',
                'planet_thumbnail'  : 'http://urls',
                'galaxy_name'       : '가람우주',
                'theme_name'        : '무한테스트',
                'accomodation_info' : [{
                    'min_of_people' : 2,
                    'max_of_people' : 4,
                    'price'         : '100000.00'
                }]
            }]
        })

    def test_fail_wishlistview_post_not_found(self):
        token    = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)
        client   = Client()
        headers  = {'HTTP_Authorization':token}
        response = client.post(
            '/wishlists/3',
            **headers
        )
        self.assertEqual(response.status_code, 404)