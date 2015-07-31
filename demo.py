from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from RPi import GPIO


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

    Application([('/$', Handler)]).listen(50000)
    IOLoop.instance().start()

except KeyboardInterrupt:
    exit()

finally:
    GPIO.cleanup()
