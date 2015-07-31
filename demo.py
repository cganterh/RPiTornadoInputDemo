from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop, PeriodicCallback
from RPi import GPIO

last_test = 0


def test_night():
    global last_test

    night = GPIO.input(22)

    if night and not last_test:
        GPIO.output(4, 1)

    if not night and last_test:
        GPIO.output(4, 0)

    last_test = night


class Handler(RequestHandler):
    def get(self):
        self.write(
            "<head>"
            "   <meta name='viewport'"
            "         content='width=device-width,"
            "                  height=device-height'>"
            "</head>"
            "<form action='/' method='post'>"
            "    <input type='submit' name='encender'"
            "           value='Encender' />"
            "    <input type='submit' name='apagar'"
            "           value='Apagar' />"
            "</form>"
        )

    def post(self):
        encender = self.get_argument('encender', '')
        apagar = self.get_argument('apagar', '')

        if encender and not apagar:
            GPIO.output(4, 1)

        if not encender and apagar:
            GPIO.output(4, 0)

        self.get()

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(22, GPIO.IN)

    Application([('/$', Handler)]).listen(50000)
    PeriodicCallback(test_night, 100).start()
    IOLoop.instance().start()

except KeyboardInterrupt:
    exit()

finally:
    GPIO.cleanup()
