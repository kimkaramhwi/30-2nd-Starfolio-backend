from django.test     import TestCase, Client

from users.models    import User
from planets.models  import Accomodation, Planet, PlanetImage, PlanetTheme, Galaxy

class PlanetListTest(TestCase):
    @classmethod
    def setUpTestData(cls):	
        User.objects.create(
            id       = 1,
            name     = '박건규',
            password = '',
            email    = '박건규@박건규.com',
            kakao_id = 123456789111
        )

        Galaxy.objects.bulk_create([
            Galaxy(
                id   = 1,
                name = '우리은하'
            ),
            Galaxy(
                id   = 2,
                name = '가람우주'
            )
        ])

        PlanetTheme.objects.bulk_create([
            PlanetTheme(
                id   = 1,
                name = '제일 이쁘다'
            ),
            PlanetTheme(
                id   = 2,
                name = '가람테마'
            )
        ])

        Planet.objects.bulk_create([
            Planet(
                id        = 1,
                name      = '이쁜행성',
                thumbnail = 'testurl/testurl/test',
                theme_id  = 1,
                galaxy_id = 1
            ),
            Planet(
                id        = 2,
                name      = '가람별2',
                thumbnail = 'http://urls2',
                theme_id  = 2,
                galaxy_id = 2
            )
        ])

        PlanetImage.objects.bulk_create([
            PlanetImage(
                id        = 1,
                image_url = 'testurl/testurl/test',
                planet_id = 1
            ),
            PlanetImage(
                id        = 2,
                image_url = 'urls2',
                planet_id = 2
            )
        ])

        Accomodation.objects.bulk_create([
            Accomodation(
                id            = 1,
                name          = '이쁜숙소',
                price         = 2500000.00,
                min_of_people = 2,
                max_of_people = 4,
                num_of_bed    = 2,
                description   = '엄청 이쁜 숙소입니다.',
                planet_id     = 1
            ),
            Accomodation(
                id            = 2,
                name          = '가람의호텔2',
                price         = 200000.00,
                min_of_people = 4,
                max_of_people = 8,
                num_of_bed    = 4,
                description   = '큽니다.',
                planet_id     = 2
            )
        ])

    def tearDown(self):
        User.objects.all().delete()
        Galaxy.objects.all().delete()
        PlanetTheme.objects.all().delete()
        Planet.objects.all().delete()
        PlanetImage.objects.all().delete()
        Accomodation.objects.all().delete()

    def test_success_planetlistview_get(self):
        client   = Client()
        response = client.get(
            '/planets'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'planets_list':[{
                'id'        : 1,
                'name'      : '이쁜행성',
                'thumbnail' : 'testurl/testurl/test',
                'galaxy'    : '우리은하',
                'theme'     : '제일 이쁘다',
                'image'     : ['testurl/testurl/test'],
                'accomodation_info' :[{
                    'min_of_people' : 2,
                    'max_of_people' : 4,
                    'price'         : '2500000.00'
                }]
            },
            {
                'id'        : 2,
                'name'      : '가람별2',
                'thumbnail' : 'http://urls2',
                'galaxy'    : '가람우주',
                'theme'     : '가람테마',
                'image'     : ['urls2'],
                'accomodation_info' :[{
                    'min_of_people' : 4,
                    'max_of_people' : 8,
                    'price'         : '200000.00'
                }]
            }]
        })

    def test_success_planetlistview_get_filter(self):
        client   = Client()
        response = client.get(
            '/planets?galaxy=2&theme=2&people=5'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'planets_list':[{
                'id'        : 2,
                'name'      : '가람별2',
                'thumbnail' : 'http://urls2',
                'galaxy'    : '가람우주',
                'theme'     : '가람테마',
                'image'     : ['urls2'],
                'accomodation_info' :[{
                    'min_of_people' : 4,
                    'max_of_people' : 8,
                    'price'         : '200000.00'
                }]
            }]
        })

    def test_success_planetlistview_get_price_filter(self):
        client   = Client()
        response = client.get(
            '/planets?min-price=210000&max-price=2500000'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'planets_list':[{
                'id'        : 1,
                'name'      : '이쁜행성',
                'thumbnail' : 'testurl/testurl/test',
                'galaxy'    : '우리은하',
                'theme'     : '제일 이쁘다',
                'image'     : ['testurl/testurl/test'],
                'accomodation_info' :[{
                    'min_of_people' : 2,
                    'max_of_people' : 4,
                    'price'         : '2500000.00'
                }]
            }]
        })

    def test_success_planetlistview_get_searching_filter(self):
        client   = Client()
        response = client.get(
            '/planets?searching=가람별'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'planets_list':[{
                'id'        : 2,
                'name'      : '가람별2',
                'thumbnail' : 'http://urls2',
                'galaxy'    : '가람우주',
                'theme'     : '가람테마',
                'image'     : ['urls2'],
                'accomodation_info' :[{
                    'min_of_people' : 4,
                    'max_of_people' : 8,
                    'price'         : '200000.00'
                }]
            }]
        })

    def test_success_planetlistview_get_sort(self):
        client   = Client()
        response = client.get(
            '/planets?sort=asc'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'planets_list':[{
                'id'        : 2,
                'name'      : '가람별2',
                'thumbnail' : 'http://urls2',
                'galaxy'    : '가람우주',
                'theme'     : '가람테마',
                'image'     : ['urls2'],
                'accomodation_info' :[{
                    'min_of_people' : 4,
                    'max_of_people' : 8,
                    'price'         : '200000.00'
                }]
            },
            {
                'id'        : 1,
                'name'      : '이쁜행성',
                'thumbnail' : 'testurl/testurl/test',
                'galaxy'    : '우리은하',
                'theme'     : '제일 이쁘다',
                'image'     : ['testurl/testurl/test'],
                'accomodation_info' :[{
                    'min_of_people' : 2,
                    'max_of_people' : 4,
                    'price'         : '2500000.00'
                }]
            }]
        })

    def test_fail_planetlistview_get_invalid_date(self):
        client   = Client()
        response = client.get(
            '/planets?check-in=2022-03-19&check-out=2022-03-18'
        )
        self.assertEqual(response.status_code, 400)