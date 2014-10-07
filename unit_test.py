import unittest
import sched.app as ap
import sched.models as mod
from datetime import datetime
from datetime import timedelta


class TestApp(unittest.TestCase):

    def test_delete(self):
        self.assertRaises(NotImplementedError, ap.appointment_delete, 8)


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
        self.assertNotEqual(1050, app.duration)

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
