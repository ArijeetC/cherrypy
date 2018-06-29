# This file is part of CherryPy <http://www.cherrypy.org/>
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab:fileencoding=utf-8


import cherrypy
from cherrypy.test import helper


class SignAuthTest(helper.CPWebCase):

    @staticmethod
    def setup_server():
        class Root:

            @cherrypy.expose
            def index(self):
                return 'This is public.'

        class BasicProtected:

            @cherrypy.expose
            def index(self):
                return "Hello, you've been authorized."

        class BasicProtected2:

            @cherrypy.expose
            def index(self):
                return "Hello, you've been authorized."

        class BasicProtected2_u:

            @cherrypy.expose
            def index(self):
                return "Hello, you've been authorized."

        conf = {
            '/basic': {
                'tools.auth_sign.on': True,
                'tools.auth_sign.realm': 'wonderland',
                'tools.auth_sign.key_file': 'cherrypy/test/test_public.pem',
            },
            '/basic2': {
                'tools.auth_sign.on': True,
                'tools.auth_sign.realm': 'wonderland',
                'tools.auth_sign.key_file': 'cherrypy/test/test_public.pem',
            },
            '/basic2_u': {
                'tools.auth_sign.on': True,
                'tools.auth_sign.realm': 'wonderland',
                'tools.auth_sign.key_file': 'cherrypy/test/test_public.pem',
            },
        }

        root = Root()
        root.basic = BasicProtected()
        root.basic2 = BasicProtected2()
        root.basic2_u = BasicProtected2_u()
        cherrypy.tree.mount(root, config=conf)

    def testPublic(self):
        self.getPage('/')
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'text/html;charset=utf-8')
        self.assertBody('This is public.')

    def testSign(self):
        self.getPage('/basic/')
        self.assertStatus(401)
        self.assertHeader(
            'WWW-Authenticate',
            'Basic realm="wonderland"'
        )

        self.getPage('/basic/',
                     [('Signature', 'MjD0h1/Yj/J6KCaJ89j/BBGL3jeHpUOtKxOI4/W73ydoREXsFKMWbBHAIGV4cZ0fkWLZjG88V9KA8BOiM7TMXik3BKjCxIQU3moBGNbZaG39M7d7SMr+neXj7mNCk80VJQXG7HBT1CyEswwqTtA7kUl+4238QgbGIOUi5LnICUuXx0dloRjnp+x6CLfzGly0Od4z2TqWK5vv2JowJGyRqixQbgnhkGPDicqA6sblQ7r85ZLka6Sc3Pml12ifU6WH7ycS7h5fX0WAncaTArAQMNaCukkxJLbMMSSXik0q1Xtbwe9eaUBrmoyrRV5yjt9nEppfaRBHQcHvq5NJRpKh+Q=='), ('Message', '152593727144')])  # noqa: E501
        self.assertStatus(401)

        self.getPage('/basic/',
                     [('Signature', 'EBOw4I9HnwMNZL3TdLfRzA9uqi8qSuOqsD7WiUtoM4zJzKk9wvXmbojBUwxdLS/poNPmgzIh2bEOTJ9dlZvVrxHG4DId9K+2gVEaQykAwFQ3/tZpAuYXTdY6vvF+ZTuYSV3+67LkvJfrWIYrewDMSzYeMr0BFY+rQQeB728g0VqYhvlrj35g/zquUTGLHy6ebJnaEKFdx04KuzWnSGoXy5vt98f7wLFcOEE5/Y/No0WZVjULF5sK75pQCLEAGuTOOE1EgVxCJCM3JUV3akybWoP6YGOJt7tUA/6de9v6eMtlBNEoaA7mQszH9JYch+ClOxPVTK1SoxLrPQmrSJshLA=='), ('Message', '1530191775584')])  # noqa: E501
        self.assertStatus('200 OK')
        self.assertBody("Hello, you've been authorized.")

    # def testBasic2(self):
    #     self.getPage('/basic2/')
    #     self.assertStatus(401)
    #     self.assertHeader('WWW-Authenticate', 'Basic realm="wonderland"')

    #     self.getPage('/basic2/',
    #                  [('Authorization', 'Basic eHVzZXI6eHBhc3N3b3JX')])
    #     self.assertStatus(401)

    #     self.getPage('/basic2/',
    #                  [('Authorization', 'Basic eHVzZXI6eHBhc3N3b3Jk')])
    #     self.assertStatus('200 OK')
    #     self.assertBody("Hello xuser, you've been authorized.")

    # def testBasic2_u(self):
    #     self.getPage('/basic2_u/')
    #     self.assertStatus(401)
    #     self.assertHeader(
    #         'WWW-Authenticate',
    #         'Basic realm="wonderland", charset="UTF-8"'
    #     )

    #     self.getPage('/basic2_u/',
    #                  [('Authorization', 'Basic eNGO0LfQtdGAOtGX0LbRgw==')])
    #     self.assertStatus(401)

    #     self.getPage('/basic2_u/',
    #                  [('Authorization', 'Basic eNGO0LfQtdGAOtGX0LbQsA==')])
    #     self.assertStatus('200 OK')
    #     self.assertBody("Hello xюзер, you've been authorized.")
