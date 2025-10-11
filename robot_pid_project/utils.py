# ============================================================
# utils.py
# Funcții auxiliare pentru gestionarea fișierelor și calibrări
# ============================================================

from pybricks.tools import wait


# ------------------------------------------------------------
# Citește configurația din fișier
# ------------------------------------------------------------
def read_config(filename="config.txt"):
    config = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=")
                    config[key.strip()] = float(value.strip())
    except OSError:
        print("⚠️ Fișierul de configurare nu a fost găsit.")
    return config


# ------------------------------------------------------------
# Scrie configurația în fișier
# ------------------------------------------------------------
def write_config(config, filename="config.txt"):
    try:
        with open(filename, "w") as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")
    except OSError:
        print("⚠️ Eroare la scrierea fișierului de configurare.")


# ------------------------------------------------------------
# Calibrare senzor de culoare
# (măsoară valoarea alb și negru, apoi setează media ca target)
# ------------------------------------------------------------
def calibrate_sensor(sensor, hub, config):
    hub.display.text("WHITE")
    wait(2000)
    white_val = sensor.reflection()
    hub.display.text("BLACK")
    wait(2000)
    black_val = sensor.reflection()

    target = (white_val + black_val) / 2
    config["target_reflection"] = target
    write_config(config)

    hub.display.text("DONE")
    wait(1000)
