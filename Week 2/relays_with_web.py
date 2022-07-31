# ESP32 GPIO 26
intruder = Pin(13, Pin.OUT)
lights = Pin(12, Pin.OUT)
def web_page():
  sensors = {
    'intruder_alarm': {0: '', 1: 'checked'},
    'lights': {0: '', 1: 'checked'}
  }
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
  body{font-family:Arial;text-align: center;margin: 0px auto;padding-top: 30px}
  main{display:flex;flex-direction: column; justify-content: space-between; align-items: center}
  .switch{position: relative;display:inline-block; width: 120px; height: 68px}.switch input{display: none}
  .slider{position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: #ccc; border-radius: 34px; cursor: pointer}
  .slider:before{position: absolute; content: ""; height: 52px; width: 52px; left: 8px; bottom: 8px; background-color: #fff; -webkit-transition: .4s; transition: .4s; border-radius: 68px}
  input:checked+.slider{background-color: #5BB318}input:checked+.slider:before{-webkit-transform: translateX(52px); -ms-transform: translateX(52px); transform: translateX(52px)}
  @media (min-width: 500px){main{width: 70%%; max-width: 470px; margin: 0 auto; flex-direction: row}}</style>
  <script>function toggleCheckbox(element){var xhr=new XMLHttpRequest(); if(element.checked){xhr.open("GET", `/?${element.id}=on`, true)}else{xhr.open("GET", `/?${element.id}=off`, true)}xhr.send()}</script>
  </head><body> <h1>Smart Farm Controls</h1> <main> <section> <h2>Intruder Alarm</h1> <label class="switch">
  <input type="checkbox" onchange="toggleCheckbox(this)" id='intruder' %s> <span class="slider"> </span> </label> </section>
  <section> <h1>Farm Lights</h1> <label class="switch"> <input type="checkbox" onchange="toggleCheckbox(this)" id='lights' %s>
  <span class="slider"> </span> </label> </section> </main></body></html>""" % (sensors['intruder_alarm'][intruder.value()], sensors['lights'][lights.value()])
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