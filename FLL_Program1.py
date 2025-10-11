from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.tools import StopWatch, wait
# Am eliminat import math, deoarece nu este acceptat pe MicroPython
# import math # -> Eliminat

# CONSTANTE GLOBALE
PI = 3.141592653589793 # Constanta PI folosită de tine

class PrecisionRobot:
    """
    O clasă pentru a gestiona mișcarea precisă a robotului bazată pe roți și IMU.
    Utilizează controlere P sau PID simplificate pentru a îmbunătăți precizia.
    """
    def __init__(self, hub, left_motor_port, right_motor_port, wheel_diameter_mm, axle_track_mm):
        # Inițializare hardware
        self.hub = hub
        self.motor_stanga = Motor(left_motor_port, positive_direction=Direction.COUNTERCLOCKWISE)
        self.motor_dreapta = Motor(right_motor_port)
        
        # Resetare unghiuri la pornire
        self.motor_stanga.reset_angle(0)
        self.motor_dreapta.reset_angle(0)

        # Configurație fizică
        self.wheel_diameter_mm = wheel_diameter_mm
        self.axle_track_mm = axle_track_mm
        self.timer = StopWatch() # Timer pentru calcularea delta time (dt)

        # Setări P pentru Mers Drept bazat pe IMU (Corecția de deviație)
        # Kp_imu_straight: Cât de agresiv corectează deviația de la unghiul global
        self.Kp_imu_straight = 0.8 # Valoare de start: Mărește dacă robotul șerpuiește
        
        # Câștig P pentru Distanță (Controlul Vitezei/Decelerației)
        # Kp_distance: Controlează viteza în funcție de distanța rămasă.
        self.Kp_distance = 6.0
        
        # Setări PID pentru Rotație (Controlul Unghiului) - Păstrat pentru 'turn' IMU
        self.Kp_turn = 1.5
        self.Kd_turn = 1.0
        
        self.global_angle = self.hub.imu.heading() # Unghiul absolut țintă (mereu actualizat)
        self.tolerance_drive = 10 # Toleranță unghiuri (grade) pentru break loop Drive
        self.tolerance_turn = 1  # Toleranță unghiuri (grade) pentru break loop Turn
        self.steady_time = 150 # Timp în ms cât trebuie să stea robotul în toleranță


    # ======================================
    # Funcții utilitare
    # ======================================

    def cm_to_degrees(self, cm):
        """Convertește distanța în cm în grade de rotație ale motorului."""
        circumferinta_mm = PI * self.wheel_diameter_mm
        rotatii = (cm * 10) / circumferinta_mm
        grade = rotatii * 360
        return grade

    def clamp(self, val, low, high):
        """Limitează o valoare între o limită minimă și una maximă."""
        return max(low, min(val, high))

    def get_avg_angle(self):
        """Returnează media unghiurilor motorului (pentru distanța parcursă)."""
        return (self.motor_stanga.angle() + self.motor_dreapta.angle()) / 2

    # ======================================
    # Mers drept cu P-Control Distanță și P-Control Corecție IMU
    # ======================================
    def drive_distance_precise(self, distance_cm, max_speed):
        """
        Mers drept folosind P-Controller pentru distanță (decelerație)
        și P-Controller bazat pe IMU pentru a menține unghiul global.
        """
        target_deg = self.cm_to_degrees(distance_cm)
        self.motor_stanga.reset_angle(0)
        self.motor_dreapta.reset_angle(0)
        self.timer.reset()
        
        print(f"Începe mersul pe {distance_cm:.1f} cm (Target Rot: {target_deg:.0f} deg). Țintă IMU: {self.global_angle:.0f}")

        while True:
            # Calculează dt (delta time)
            dt = self.timer.time() / 1000
            self.timer.reset()
            if dt == 0:
                dt = 0.001 # Previne împărțirea la zero

            # 1. Măsurători Rot/Distanță
            rot_l = self.motor_stanga.angle()
            rot_r = self.motor_dreapta.angle()
            avg_rot = (rot_l + rot_r) / 2
            
            # 2. P-Controller pentru Distanță (Decelerație)
            remaining_error = target_deg - avg_rot

            if remaining_error <= self.tolerance_drive:
                break # Oprește bucla când se ajunge la țintă

            # Viteza de bază (se reduce pe măsură ce eroarea se apropie de 0)
            base_speed = self.Kp_distance * remaining_error
            base_speed = self.clamp(base_speed, 50, max_speed) # Minim 50 pentru a evita blocarea
            
            # 3. P-Controller pentru Corecția Direcției (IMU Straightness)
            current_heading = self.hub.imu.heading()
            
            # Eroare normalizată (-180..180)
            heading_error = (self.global_angle - current_heading + 180) % 360 - 180
            
            # Corecție P bazată pe IMU
            corectie = self.Kp_imu_straight * heading_error
            
            # 4. Aplică Corecția
            # Dacă corecția e pozitivă (trebuie să vireze spre stânga), viteza dreaptă crește, stânga scade.
            v_l = base_speed - corectie
            v_r = base_speed + corectie

            # 5. Limitează vitezele și rulează motoarele
            v_l = self.clamp(v_l, -max_speed, max_speed)
            v_r = self.clamp(v_r, -max_speed, max_speed)

            self.motor_stanga.run(v_l)
            self.motor_dreapta.run(v_r)
            
            wait(10) # Buclează rapid

        self.motor_stanga.stop()
        self.motor_dreapta.stop()
        print(f"Mers drept finalizat. Unghi final IMU: {self.hub.imu.heading():.0f}")
        wait(300)

    # ======================================
    # Rotație stabilă cu PID pe IMU Heading (Metoda Precisă)
    # ======================================
    def turn_to_angle_precise(self, target_angle, max_speed):
        """
        Rotește robotul la un unghi absolut (față de resetarea IMU)
        folosind PID pe datele de la IMU.
        """
        self.global_angle = target_angle # Actualizează unghiul absolut
        
        error_prev = 0
        min_speed = 30
        
        # Timer pentru a verifica dacă robotul este stabil
        stable_timer = StopWatch()
        stable_timer.reset()

        print(f"Începe rotația PID către unghiul absolut: {target_angle:.0f} grade")

        while True:
            # Măsură unghiul curent
            heading_raw = self.hub.imu.heading()
            
            # Eroare normalizată (-180..180)
            error = (target_angle - heading_raw + 180) % 360 - 180

            # Verificare stabilitate
            if abs(error) <= self.tolerance_turn:
                # Dacă eroarea este în toleranță, pornește/continuă numărătoarea
                if stable_timer.time() >= self.steady_time:
                    break # Ieși din buclă dacă timpul de stabilitate a fost atins
            else:
                # Dacă iese din toleranță, resetează timer-ul
                stable_timer.reset()

            # Calcul Derivativ (Kd)
            derivative = error - error_prev
            error_prev = error

            # Calcul Viteză = Kp * Eroare + Kd * Derivativ
            speed = self.Kp_turn * error + self.Kd_turn * derivative
            
            # Limitează viteza (inclusiv viteza minimă)
            speed = self.clamp(speed, -max_speed, max_speed)
            if abs(speed) < min_speed:
                speed = min_speed if speed > 0 else -min_speed

            # Aplică viteza (un motor înainte, unul înapoi)
            self.motor_stanga.run(-speed)
            self.motor_dreapta.run(speed)
            
            wait(10)

        self.motor_stanga.stop()
        self.motor_dreapta.stop()
        print(f"Rotație IMU finalizată la unghiul: {self.hub.imu.heading():.0f}")
        wait(300)

    # ======================================
    # Rotație bazată pe Grade Motor (Pentru Teste RAW)
    # ======================================
    def turn_relative_motor_degrees(self, relative_angle, max_speed):
        """
        Rotește robotul cu un unghi relativ (e.g., 90) bazat DOAR pe calculele motorului.
        IGNORĂ IMU și PID. Folosit pentru calibrarea fizică.
        """
        # Formula pentru a calcula rotația motoarelor necesară pentru un viraj în loc
        # Formula: (unghi_relativ * axle_track_mm) / wheel_diameter_mm
        motor_degrees = (relative_angle * self.axle_track_mm) / self.wheel_diameter_mm
        
        print(f"Raw Turn: Rotesc cu {relative_angle:.0f} grade, Motoare: {motor_degrees:.0f} grade")

        # Rotește motoarele
        self.motor_stanga.run_angle(max_speed, -motor_degrees, wait=False)
        self.motor_dreapta.run_angle(max_speed, motor_degrees, wait=True)
        
        print(f"Raw Turn: Rotație motor finalizată. Unghi IMU curent: {self.hub.imu.heading():.1f} grade")
        wait(300)

    # ======================================
    # Execuție traseu (combinat drive + turn)
    # ======================================
    def executa_traseu(self, traseu):
        """
        Execută o secvență de comenzi de mișcare.
        Acum, 'turn_raw' actualizează unghiul țintă global (global_angle)
        pentru ca mersul drept (drive) să corecteze deviația.
        """
        print("--- Începe Traseul ---")
        for com in traseu:
            tip = com[0]
            if tip == 'drive':
                dist, viteza = com[1], com[2]
                print(f"Comandă: Mers {dist:.1f} cm (Viteza Max: {viteza})")
                self.drive_distance_precise(dist, viteza)
            
            elif tip == 'turn_raw':
                unghi_rel, viteza = com[1], com[2]
                
                # NOU: Actualizează unghiul global țintă înainte de a executa turn_raw
                self.global_angle += unghi_rel
                self.global_angle = self.global_angle % 360
                if self.global_angle > 180:
                    self.global_angle -= 360
                
                # Execută rotația simplă (care va fi imprecisă)
                self.turn_relative_motor_degrees(unghi_rel, viteza)
                
            elif tip == 'turn':
                unghi_rel, viteza = com[1], com[2]
                
                # Calculează noul unghi absolut
                self.global_angle += unghi_rel
                
                # Normalizare unghi (opțional, dar bun)
                self.global_angle = self.global_angle % 360
                if self.global_angle > 180:
                    self.global_angle -= 360

                print(f"Comandă: Rotire relativă cu {unghi_rel:.0f} grade (Target Absolut: {self.global_angle:.0f})")
                self.turn_to_angle_precise(self.global_angle, viteza)
            
            wait(100) # Pauză scurtă între comenzi
        print("--- Traseu Finalizat ---")


# ======================================
# Configurarea Robotului și a Traseelor
# ======================================

# 1. Definirea configurației fizice a robotului
ROBOT_WHEEL_DIAMETER_MM = 62.4 # Diametrul roților în mm
ROBOT_AXLE_TRACK_MM = 80    # Distanța dintre centrele roților în mm

# 2. Inițializarea și calibrarea Hub-ului
main_hub = PrimeHub()
main_hub.imu.reset_heading(0) # Resetează unghiul IMU la 0 la pornire

# 3. Crearea instanței robotului
robot = PrecisionRobot(
    hub=main_hub,
    left_motor_port=Port.C,
    right_motor_port=Port.F,
    wheel_diameter_mm=ROBOT_WHEEL_DIAMETER_MM,
    axle_track_mm=ROBOT_AXLE_TRACK_MM
)

# 4. Trasee de test

# Traseu pentru CALIBRAREA RAW (Testează cât de mult se rotește robotul)
traseu_test_raw_turn = [
    ('turn_raw', 90, 300), # Rotește 90 de grade, dar fără corecție IMU/PID
]

# Traseu Patrat, acum folosește turn_raw, dar drive corectează unghiul pierdut!
traseu_patrat = [
    ('drive', 50, 600), # Merge drept la 0 grade
    ('turn_raw', 90, 300), # Rotește, probabil la 93 grade, dar ținta globală devine 90
    ('drive', 50, 600), # Merge drept, corectând deviația de la 93 grade înapoi la 90
    ('turn_raw', 90, 300), # Rotește, ținta globală devine 180
    ('drive', 50, 600), # Merge drept, corectând deviația spre 180
    ('turn_raw', 90, 300), # Rotește, ținta globală devine -90
    ('drive', 50, 600), # Merge drept, corectând deviația spre -90
    ('turn_raw', 90, 300) # Rotește, ținta globală devine 0
]

traseu_test_drept = [
    ('drive', 100, 800), # Merge 1 metru
]

# ======================================
# Rulează traseul dorit
# ======================================
# Acum se va executa traseul patrat care folosește corecția IMU pe mersul drept
robot.executa_traseu(traseu_patrat)
# robot.executa_traseu(traseu_test_raw_turn)
# robot.executa_traseu(traseu_test_drept)
