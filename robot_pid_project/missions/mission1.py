# ============================================================
# missions/mission1.py
# Misiune demonstrativă: urmărire de linie 5 secunde + viraj
# ============================================================

from pybricks.tools import wait


def run(hub, motors, sensor, pid, config):
    """
    Execută traseul specific misiunii 1.
    motors = (motor_stanga, motor_dreapta)
    """

    motor_stanga, motor_dreapta = motors
    base_speed = config["base_speed"]
    target = config["target_reflection"]

    # 1️⃣ Urmărire linie 5 secunde
    t = 0
    step = 10
    while t < 5000:
        reflection = sensor.reflection()
        correction = pid.compute(target, reflection)

        # limităm
        if correction > base_speed:
            correction = base_speed
        elif correction < -base_speed:
            correction = -base_speed

        left_speed = base_speed - correction
        right_speed = base_speed + correction
        motor_stanga.run(left_speed)
        motor_dreapta.run(right_speed)

        wait(step)
        t += step

    # 2️⃣ Mic viraj spre dreapta
    motor_stanga.run_time(200, 800)
    motor_dreapta.run_time(-200, 800)

    # Oprire
    motor_stanga.stop()
    motor_dreapta.stop()
