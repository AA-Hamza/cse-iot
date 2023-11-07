from classes.Command import Command
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd


class LCD16x2Command(Command):
    name = "lcd16x2"
    state = None
    lcd: characterlcd.Character_LCD_Mono

    def __init__(self, rs=22, en=17, d4=25, d5=24, d6=23, d7=18):
        self.lcd = characterlcd.Character_LCD_Mono(
            # rs=digitalio.DigitalInOut(board.pin(rs)),
            # en=digitalio.DigitalInOut(board.pin(en)),
            # db4=digitalio.DigitalInOut(board.pin(d4)),
            # db5=digitalio.DigitalInOut(board.pin(d5)),
            # db6=digitalio.DigitalInOut(board.pin(d6)),
            # db7=digitalio.DigitalInOut(board.pin(d7)),
            rs=digitalio.DigitalInOut(board.D22),
            en=digitalio.DigitalInOut(board.D17),
            db4=digitalio.DigitalInOut(board.D25),
            db5=digitalio.DigitalInOut(board.D24),
            db6=digitalio.DigitalInOut(board.D23),
            db7=digitalio.DigitalInOut(board.D18),
            columns=16,
            lines=2)
        self.lcd.clear()
        self.state = ""

    def execute(self, payload) -> dict:
        if (isinstance(payload, str)):
            self.lcd.clear()
            self.lcd.message = payload
            self.state = payload
            result = {
                "feedback": {
                    "message":
                    "successfully written {message} on lcd".format(
                        message=payload)
                }
            }
            return result
        else:
            result = {
                "feedback": {
                    "error": "payload supported types are [str]"
                }
            }
            return result
