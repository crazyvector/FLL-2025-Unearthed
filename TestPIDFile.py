from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.tools import wait, StopWatch
from pybricks.parameters import Port, Direction

# Inițializare hub
hub = PrimeHub()

# Motoare
motor_stanga = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
motor_dreapta = Motor(Port.F)

# Senzori de culoare
sensor_stanga = ColorSensor(Port.D)
sensor_dreapta = ColorSensor(Port.B)

# PID Settings
Kp = 1.2
Ki = 0.0
Kd = 0.4

# Viteză variabilă
viteza_min = 80
viteza_max = 300

# Prag reflexie pentru a detecta linia (ajustează după mediu)
prag_linie = 40

# PID state
eroare_anterioara = 0
suma_eroare = 0

# Timer pentru dt
timer = StopWatch()
timer.reset()

# Stare căutare linie
searching = False
search_direction = 1  # 1 = dreapta, -1 = stânga
search_time = 0
max_search_time = 1000  # ms pentru fiecare direcție de căutare

while True:
    val_stanga = sensor_stanga.reflection()
    val_dreapta = sensor_dreapta.reflection()

    # Detectare linie pierdută (ambele senzori văd alb)
    linie_pierduta = (val_stanga > prag_linie) and (val_dreapta > prag_linie)

    if linie_pierduta:
        if not searching:
            searching = True
            search_direction = 1
            search_time = 0

        # Rotește pe loc pentru a căuta linia
        motor_stanga.run(100 * search_direction)
        motor_dreapta.run(-100 * search_direction)

        wait(10)
        search_time += 10

        if search_time >= max_search_time:
            # Schimbă direcția de căutare dacă nu găsește linia
            search_direction *= -1
            search_time = 0

        # Reset PID când cauți
        suma_eroare = 0
        eroare_anterioara = 0
        timer.reset()
        continue

    # Linia găsită, oprește căutarea
    if searching:
        searching = False
        # Resetează timer pentru PID
        timer.reset()

    # Calculează eroarea: diferența reflexiilor (linia între senzori)
    eroare = val_stanga - val_dreapta

    dt = timer.time() / 1000  # în secunde
    timer.reset()

    if dt == 0:
        dt = 0.001  # evită împărțirea la zero

    suma_eroare += eroare * dt
    derivata = (eroare - eroare_anterioara) / dt

    corectie = Kp * eroare + Ki * suma_eroare + Kd * derivata
    eroare_anterioara = eroare

    # Viteză adaptivă: scade când corecția e mare, crește când e mică
    factor = max(0, min(1, 1 - abs(corectie) / 100))  # ajustează 100 după nevoie
    viteza_curenta = viteza_min + (viteza_max - viteza_min) * factor

    viteza_stanga = viteza_curenta - corectie
    viteza_dreapta = viteza_curenta + corectie

    motor_stanga.run(viteza_stanga)
    motor_dreapta.run(viteza_dreapta)

    wait(10)
