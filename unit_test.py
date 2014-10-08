import unittest
import flask
import json
import sched.app as ap
import sched.models as mod
from datetime import datetime
from datetime import timedelta


class AppTest(unittest.TestCase):

    def setUp(self):
        # Create Flask test client
        self.app = ap.app.test_client()

    def test_list(self):
        response = self.app.get("/appointments/")
        self.assertEquals(response.status_code, 200)
        assert 'Past Meeting' in response.data
        assert 'Prueba agenda' not in response.data

    def test_detail(self):
        response = self.app.get("/appointments/4/")
        self.assertEquals(response.status_code, 200)
        assert 'Day Off' in response.data
        assert 'Past Meeting' not in response.data

        response2 = self.app.get("/appointments/33/")
        self.assertEquals(response2.status_code, 404)

    def test_create(self):
        response = self.app.get("/appointments/create/")
        self.assertEquals(response.status_code, 200)
        assert 'Add Appointment' in response.data
        assert 'Edit Appointment' not in response.data

        response2 = self.app.post("/appointments/create/",
                                  data=dict(
                                      title='Pruebas',
                                      start='2014-10-07 06:00:00',
                                      end='2014-10-08 15:00:00',
                                      location='Home',
                                      description='Proyecto Flask',
                                  ), follow_redirects=True)
        self.assertEquals(response2.status_code, 200)
        assert 'Pruebas' in response2.data

    def test_edit(self):
        response = self.app.get("/appointments/1/edit/")
        self.assertEquals(response.status_code, 200)
        assert 'Add Appointment' not in response.data
        assert 'Edit Appointment' in response.data

        response2 = self.app.post("/appointments/4/edit/",
                                  data=dict(
                                      title='Day Off',
                                      start='2014-10-07 23:00:00',
                                      end='2014-10-08 13:00:00',
                                      location='School',
                                      description='Proyecto Flask',
                                  ), follow_redirects=True)
        self.assertEquals(response2.status_code, 200)
        assert '2014-10-07 23:00:00' in response2.data

        response3 = self.app.get("/appointments/33/edit/")
        self.assertEquals(response3.status_code, 404)

    def test_delete(self):
        response = self.app.get("/appointments/5/delete/")
        self.assertEquals(response.status_code, 405)

        response2 = self.app.delete(
            "/appointments/5/delete/", follow_redirects=True)
        self.assertEquals(response2.status_code, 200)
        self.assertEqual(json.loads(response2.data), {'status': 'OK'})

        response3 = self.app.delete(
            "/appointments/33/delete/", follow_redirects=True)
        self.assertEquals(response3.status_code, 404)
        self.assertEqual(json.loads(response3.data), {'status': 'Not Found'})


class TestModels(unittest.TestCase):

    def test_duration(self):
        now = datetime.now()
        app = mod.Appointment(
            title='Important Meeting',
            start=now,
            end=now + timedelta(days=1, seconds=3600),
            allday=False,
            location='The Office')
        self.assertEqual(90000, app.duration)

        app2 = mod.Appointment(
            title='Important Meeting',
            start=now,
            end=now + timedelta(seconds=3600),
            allday=False,
            location='The Office')
        self.assertNotEqual(1050, app2.duration)

    def test_repr(self):
        now = datetime.now()
        app = mod.Appointment(
            id=23,
            title='Follow Up',
            start=now,
            end=now,
            allday=False,
            location='The Office')
        self.assertEqual('<Appointment: 23>', app.__repr__())
        self.assertNotEqual('<Appointment: 22>', app.__repr__())


if __name__ == '__main__':
    unittest.main()
