import datetime
import unittest
from mock import patch, DEFAULT
import marchanddesable

@patch.multiple('marchanddesable', online=DEFAULT, shutdown=DEFAULT)
class MarchandTestCase(unittest.TestCase):
    def setUp(self):
        # Yay ! Emulate files with a closure !
        patcher = patch('marchanddesable.save_awake')
        self.addCleanup(patcher.stop)
        save_awake = patcher.start()
        patcher = patch('marchanddesable.last_awake')
        self.addCleanup(patcher.stop)
        last_awake = patcher.start()

        value = 123456789
        self.time = value

        def fake_save():
            nonlocal value
            value = self.time
        save_awake.side_effect = fake_save

        def fake_last():
            return datetime.datetime.fromtimestamp(value)
        last_awake.side_effect = fake_last

        class fakedatetime(datetime.datetime):
            @classmethod
            def now(cls):
                return cls.fromtimestamp(self.time)
        patcher = patch('datetime.datetime', fakedatetime)
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_do_nothing_while_up(self, online, shutdown):
        online.return_value = True

        marchanddesable.tick(['192.168.0.1'])

        online.assert_called_with('192.168.0.1')
        self.assertFalse(shutdown.called)

    def test_shutdown_after_exactly_5_minutes_when_alone(self, online, shutdown):
        online.return_value = True
        for i in range(20):
            self.time += 60
            marchanddesable.tick(['192.168.0.1'])

        online.return_value = False
        marchanddesable.tick(['192.168.0.1'])
        self.time += 300
        marchanddesable.tick(['192.168.0.1'])
        self.assertFalse(shutdown.called)

        self.time += 1
        marchanddesable.tick(['192.168.0.1'])
        self.assertTrue(shutdown.called)
