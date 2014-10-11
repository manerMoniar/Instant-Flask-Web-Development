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
        self.app.post('/login/', data=dict(
            username='admin@mail.com',
            password='pass'), follow_redirects=True)

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



class ModelsTest(unittest.TestCase):

    def test_get_password(self):
        user = mod.User(name='Administrator',
                        email='admin@mail.com',
                        password='pass')
        assert "sha1" in user._get_password()
        assert "md5" not in user._get_password()

    def test_set_password(self):
        user = mod.User(name='Administrator',
                        email='admin@mail.com',
                        password='pass')
        user._set_password("pass")
        self.assertEqual(True, user.check_password("pass"))
        self.assertEqual(False, user.check_password("password"))

    def test_check_password(self):
        user = mod.User(name='Administrator',
                        email='admin@mail.com')
        self.assertEqual(False, user.check_password(""))
        user._set_password("pass")
        self.assertEqual(False, user.check_password(""))
        self.assertEqual(True, user.check_password("pass"))

    def test_authenticate(self):
        user, authenticate = mod.User.authenticate(
            ap.db.session.query, "admin@mail.com", "pass")
        self.assertEqual(True, authenticate)
        self.assertEqual(user.name, u"Administrator")

        user2, authenticate2 = mod.User.authenticate(
            ap.db.session.query, "a", "pass")
        self.assertEqual(False, authenticate2)
        self.assertEqual(None, user2)

        user3, authenticate3 = mod.User.authenticate(
            ap.db.session.query, "maner@mail.com", "password")
        self.assertEqual(u'Maner', user3.name)
        self.assertEqual(False, authenticate3)

    def test_get_id(self):
        user = mod.User(id=45, name='Administrator',
                        email='admin@mail.com')
        self.assertEqual('45', user.get_id())
        self.assertNotEqual('5', user.get_id())

    def test_is_active(self):
        user = mod.User(name='Administrator',
                        email='admin@mail.com')
        self.assertEqual(True, user.is_active())
        self.assertNotEqual(False, user.is_active())
        
    def test_is_anonymous(self):
        user = mod.User(name='Administrator',
                email='admin@mail.com')
        self.assertEqual(False, user.is_anonymous())
        self.assertNotEqual(True, user.is_anonymous())

    def test_is_authenticated(self):
        user = mod.User(name='Administrator',
                email='admin@mail.com')
        self.assertEqual(True, user.is_authenticated())
        self.assertNotEqual(False, user.is_authenticated())

    def test__repr__(self):
        user = mod.User(id=25, name='Administrator',
                email='admin@mail.com')
        self.assertEqual('<User: 25>', user.__repr__())
        self.assertNotEqual('<User: 22>', user.__repr__())

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

"""
class test_filter(unittest.TestCase):

    def test_datetime_without_hour(self):
        now = date(2010, 11, 11)
        fecha = filters.do_datetime(now)
        self.assertNotEqual(fecha, "2010-11-11 - Thursday")

    def test_datetime_with_hour(self):
        now = datetime(2010, 11, 11, 13, 00, 00)
        fecha = filters.do_datetime(now)
        self.assertEqual(fecha, '2010-11-11 - Thursday at 1:00pm')

    def test_datetime_None(self):
        fecha = filters.do_datetime(None)
        self.assertNotEqual(fecha, "Today")
        self.assertEqual(fecha, '')

    def test_datetime_format_None(self):
        now = datetime(2010, 11, 11, 14, 00, 00)
        fecha = filters.do_datetime(now, None)
        self.assertEqual(fecha, '2010-11-11 - Thursday at 2:00pm')

    def test_datetime_with_format(self):
        a = '%Y-%m-%d - %A'
        now = datetime(2010, 11, 11, 14, 00, 00)
        fecha = filters.do_datetime(now, a)
        self.assertNotEqual(fecha, '2010-11-11 - Thursday at 2:00pm')

    def test_date_none(self):
        fechadate = filters.do_date(None)
        self.assertEqual(fechadate, '')

    def test_date_not_none(self):
        now = datetime(2010, 11, 11, 13, 00, 00)
        fechadate = filters.do_date(now)
        self.assertNotEqual(fechadate, '2010-11-11 - Thursday at 1:00pm')
        self.assertEqual(fechadate, '2010-11-11 - Thursday')

    def test_duration_hour(self):
        time = filters.do_duration(3600)
        self.assertNotEqual(time, "1 day")
        self.assertEqual(time, "0 day, 1 hour, 0 minute, 0 second")

    def test_duration_days(self):
        time = filters.do_duration(258732)
        self.assertEqual(time, "2 days, 23 hours, 52 minutes, 12 seconds")

    def test_do_nl2br_without_Markup(self):
        template_env = Environment(
            autoescape=False,
         extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'])
        text = "Texto con '\n' para saltos '\n' pero junto"
        changes = filters.do_nl2br(template_env, text)
        self.assertNotEqual(changes, "")
        self.assertEqual(
            changes, "Texto con &#39;<br />&#39; para saltos &#39;<br />&#39; pero junto")

    def test_do_nl2br_with_Markup(self):
        template_env = Environment(
            autoescape=True,
         extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'])
        text = "Texto con '\n' para saltos '\n' pero <script>junto</script>"
        changes = filters.do_nl2br(template_env, text)
        self.assertNotEqual(
            changes, "Texto con &#39;<br />&#39; para saltos &#39;<br />&#39; pero junto")
        self.assertEqual(
            changes, "Texto con &#39;<br />&#39; para saltos &#39;<br />&#39; pero &lt;script&gt;junto&lt;/script&gt;")
"""

if __name__ == '__main__':
    unittest.main()
