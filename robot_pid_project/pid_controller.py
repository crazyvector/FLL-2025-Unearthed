# ============================================================
# pid_controller.py
# Modul pentru control PID independent, reutilizabil.
# ============================================================

# Implementare PID fără biblioteci externe, compatibil cu MicroPython
# Obiectiv: control precis al liniei (sau al unghiului) pentru un robot LEGO FLL.


class PIDController:
    def __init__(self, kp, ki, kd):
        # Inițializare constante PID
        self.kp = kp
        self.ki = ki
        self.kd = kd

        # Inițializare erori interne
        self.last_error = 0
        self.integral = 0

    def compute(self, target, current):
        """
        Calculează corecția PID.
        target  – valoarea dorită (de ex. reflecția ideală pe linia neagră)
        current – valoarea curentă citită de senzorul de culoare
        """
        error = target - current
        self.integral += error
        derivative = error - self.last_error

        # Calcul PID complet
        correction = (
            self.kp * error + self.ki * self.integral + self.kd * derivative
        )

        # Salvăm eroarea actuală pentru pasul următor
        self.last_error = error

        return correction
