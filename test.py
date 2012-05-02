import unittest
import mock

import marchanddesable


class MarchandTestCase(unittest.TestCase):
    def setUp(self):
        self.p1 = mock.patch('marchanddesable.online')
        self.p2 = mock.patch('marchanddesable.shutdown')

        self.online = self.p1.start()
        self.shutdown = self.p2.start()

        self.marchand = marchanddesable.MarchandDeSable(['192.168.0.1'])

    def tearDown(self):
        self.p1.stop()
        self.p2.stop()

    def test_do_nothing_while_up(self):
        self.online.return_value = True

        for i in range(20):
            self.marchand.tick()

        self.online.assert_called_with('192.168.0.1')
        self.assertFalse(self.shutdown.called)

    def test_shutdown_after_exactly_5_ticks_when_down(self):
        self.online.return_value = True
        for i in range(20):
            self.marchand.tick()

        self.online.return_value = False
        for i in range(4):
            self.marchand.tick()
        self.assertFalse(self.shutdown.called)

        self.marchand.tick()
        self.assertTrue(self.shutdown.called)
