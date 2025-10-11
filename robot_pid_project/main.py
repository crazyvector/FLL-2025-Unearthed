# ============================================================
# main.py
# Sistem complet LEGO FLL cu PID modular și misiuni separate
# ============================================================

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Stop
from pybricks.tools import wait

from pid_controller import PIDController
from utils import read_config, write_config, calibrate_sensor

# ------------------------------------------------------------
# Inițializări
# ------------------------------------------------------------
hub = PrimeHub()
motor_stanga = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
motor_dreapta = Motor(Port.F, positive_direction=Direction.CLOCKWISE)
sensor_culoare = ColorSensor(Port.B)

motors = (motor_stanga, motor_dreapta)

# ------------------------------------------------------------
# Citim config-ul
# ------------------------------------------------------------
config = read_config()
pid = PIDController(config["Kp"], config["Ki"], config["Kd"])

# ------------------------------------------------------------
# Meniu de selecție misiune cu butoanele hub-ului
# ------------------------------------------------------------
missions = ["mission1", "mission2", "mission3"]
selected = 0

hub.display.text(missions[selected])

while True:
    if hub.buttons.pressed():
        btn = hub.buttons.pressed()[0]

        # Navigare între misiuni
        if btn == "left":
            selected = (selected - 1) % len(missions)
            hub.display.text(missions[selected])
            wait(300)
        elif btn == "right":
            selected = (selected + 1) % len(missions)
            hub.display.text(missions[selected])
            wait(300)
        elif btn == "center":
            break

wait(500)
hub.display.text("RUN")

# ------------------------------------------------------------
# Încărcăm dinamically misiunea aleasă
# ------------------------------------------------------------
mission_name = missions[selected]
mission_module = __import__(f"missions.{mission_name}", fromlist=["run"])

# ------------------------------------------------------------
# Rulare misiune selectată
# ------------------------------------------------------------
mission_module.run(hub, motors, sensor_culoare, pid, config)

# ------------------------------------------------------------
# Auto-tuning simplu (ajustare fină a Kp)
# ------------------------------------------------------------
avg_error = abs(pid.last_error)
if avg_error > 10:  # dacă eroarea a fost mare, creștem Kp
    config["Kp"] += 0.05
elif avg_error < 3:  # dacă robotul a mers prea stabil, scădem Kp
    config["Kp"] -= 0.02

write_config(config)

hub.display.text("DONE")
