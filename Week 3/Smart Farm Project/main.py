from machine import Pin
from time import sleep
import dht
class Smart_farm:
    
    def __init__(self, wifi_name, wifi_password):
        self.wifi_name = wifi_name
        self.wifi_password = wifi_password
    def sense_temp_humidity(self):
        sensor = dht.DHT11(Pin(4))
        print('Sensing...')
        sleep(2)
        try:
            sensor.measure()
            t = sensor.temperature()
            h = sensor.humidity()
        except:
            print('There is something wrong, try again later!')
        else:
            return (t, h)
    def create_web_page(self):
        (temperature, humidity) = self.sense_temp_humidity()
        intruder = Pin(13, Pin.OUT)
        lights = Pin(12, Pin.OUT)
        temperature_fah = round((temperature * (9/5)) + 32)
        print(temperature, temperature_fah, humidity)
        def web_page():
          sensors = {
            'intruder_alarm': {0: '', 1: 'checked'},
            'lights': {0: '', 1: 'checked'}
          }
          html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><meta charset="utf-8">
          <style>body{font-family: Arial; text-align: center; margin: 0px auto; padding-top: 30px}h1{padding: .2em;}
          main{display: flex; flex-direction: column; justify-content: space-between; align-items: center}
          .switch{position: relative; display: inline-block; width: 120px; height: 68px}.switch input{display: none}
          .slider{position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: #ccc; border-radius: 34px; cursor: pointer}
          .slider:before{position: absolute; content: ""; height: 52px; width: 52px; left: 8px; bottom: 8px; background-color: #fff; -webkit-transition: .4s; transition: .4s; border-radius: 68px}
          input:checked+.slider{background-color: #5BB318}input:checked+.slider:before{-webkit-transform: translateX(52px); -ms-transform: translateX(52px); transform: translateX(52px)}
          aside{display: flex; flex-direction: column; width: 90%%; margin: 1em auto; border-radius: 5px}aside div, .measurements{display: flex; align-items: center; text-align: center; background-color: #ccc; justify-content: space-around;}
          aside div{background-color: #5BB318; color: white;}.measurements{padding: .2em 0;}.measurements p{width: 50%%;}
          .measurements h4{width: 30%%; text-align: center;}@media (min-width: 500px){main, aside{width: 70%%; max-width: 470px; margin: 0 auto; flex-direction: row}
          aside{margin: 1em auto; flex-direction: column;}}</style>
          <script>function toggleCheckbox(element){var xhr=new XMLHttpRequest(); if (element.checked){xhr.open("GET", `/?${element.id}=on`, true)}else{xhr.open("GET", `/?${element.id}=off`, true)}xhr.send()}</script></head>
          <body> <h1>Smart Farm Controls</h1> <main> <section> <h2>Intruder Alarm</h1> <label class="switch">
          <input type="checkbox" onchange="toggleCheckbox(this)" id='intruder' %s> <span class="slider"> </span> </label> </section> <section>
          <h2>Farm Lights</h2> <label class="switch"> <input type="checkbox" onchange="toggleCheckbox(this)" id='lights' %s> <span class="slider"> </span>
          </label> </section> </main> <aside> <div> <h3>MEASUREMENT</h3> <h3>VALUE</h3> </div><section class="measurements"> <p>Temp. Celcius</p><h4>%s °C</h4></section>
          <section class="measurements"> <p>Temp. Fahrenheit</p><h4>%s °F</h4> </section> <section class="measurements"> <p>Humidity</p><h4>%s%%</h4> </section>
          </aside></body></html>""" % (sensors['intruder_alarm'][intruder.value()], sensors['lights'][lights.value()], temperature, temperature_fah, humidity)
          return html

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.listen(5)

        while True:
          try:
            if gc.mem_free() < 102000:
              gc.collect()
            conn, addr = s.accept()
            conn.settimeout(3.0)
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            conn.settimeout(None)
            request = str(request)
            print('Content = %s' % request)
            intruder_on = request.find('/?intruder=on')
            intruder_off = request.find('/?intruder=off')
            lights_on = request.find('/?lights=on')
            lights_off = request.find('/?lights=off')
            if intruder_on == 6:
              print('Intruder Alarms ON')
              intruder.value(1)
            if intruder_off == 6:
              print('Intruder Alarms OFF')
              intruder.value(0)
            if lights_on == 6:
              print('Farm Lights ON')
              lights.value(1)
            if lights_off == 6:
              print('Farm Lights OFF')
              lights.value(0)
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
          except OSError as e:
            conn.close()
            print('Connection closed')


first_test = Smart_farm('Akran', 'Jango123')
        
