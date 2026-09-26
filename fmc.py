import tkinter as tk
from tkinter import messagebox
import math
#buse ceren kara 

class FMC:

    def __init__(self, root):

        self.root = root

        self.root.title("Flight Management Computer")
        self.root.geometry("1050x750")
        self.root.configure(background="white")


        # UÇUŞ BİLGİLERİ


        self.origin = ""
        self.destination = ""

        self.route = []

        self.route_active = False

        self.total_distance = 0
        self.remaining_distance = 0

        self.fuel = 18500
        self.initial_fuel = 18500

        self.altitude = 0
        self.target_altitude = 35000

        self.speed = 0
        self.target_speed = 450

        self.simulation_running = False

        self.current_page = "RTE"


        # DEMO HAVALİMANI KOORDİNATLARI


        self.airports = {

            "LTFM": (41.2753, 28.7519),
            "LTBA": (40.9769, 28.8146),

            "EGLL": (51.4700, -0.4543),

            "LFPG": (49.0097, 2.5479),

            "EDDF": (50.0379, 8.5622),

            "EHAM": (52.3105, 4.7683)
        }

        self.create_interface()


    # ARAYÜZ ınterface


    def create_interface(self):

        title = tk.Label(
            self.root,
            text="FLIGHT MANAGEMENT COMPUTER",
            font=("Arial", 24, "bold"),
            background="white",
            foreground="black"
        )

        title.pack(pady=15)

        main_frame = tk.Frame(
            self.root,
            background="white"
        )

        main_frame.pack()


        # SOL TUŞLAR R1 R2 R3 AKTİF  R4 R5 R6 PASİF


        left_frame = tk.Frame(
            main_frame,
            background="white"
        )

        left_frame.grid(
            row=0,
            column=0,
            padx=15
        )

        for i in range(6):

            button = tk.Button(
                left_frame,
                text=f"L{i + 1}",
                width=8,
                height=2,
                font=("Arial", 11, "bold"),
                command=lambda i=i: self.left_key(i + 1)
            )

            button.pack(pady=7)


        # FMC EKRANI

        screen_frame = tk.Frame(
            main_frame,
            background="black",
            padx=8,
            pady=8
        )

        screen_frame.grid(
            row=0,
            column=1
        )

        self.screen = tk.Text(
            screen_frame,
            width=62,
            height=27,
            background="#101010",
            foreground="#00FF66",
            insertbackground="#00FF66",
            font=("Courier New", 13),
            relief="flat",
            padx=15,
            pady=15
        )

        self.screen.pack()


        # SAĞ TUŞLAR L1 L2 L3 L4 L5 L6


        right_frame = tk.Frame(
            main_frame,
            background="white"
        )

        right_frame.grid(
            row=0,
            column=2,
            padx=15
        )

        for i in range(6):

            button = tk.Button(
                right_frame,
                text=f"R{i + 1}",
                width=8,
                height=2,
                font=("Arial", 11, "bold"),
                command=lambda i=i: self.right_key(i + 1)
            )

            button.pack(pady=7)


        # FMC BUTONLARI


        keyboard = tk.Frame(
            self.root,
            background="white"
        )

        keyboard.pack(pady=15)

        buttons = [

            ("INIT", self.init_page),
            ("RTE", self.rte_page),
            ("LEGS", self.legs_page),
            ("DEP/ARR", self.dep_arr_page),

            ("VNAV", self.vnav_page),
            ("PROG", self.prog_page),
            ("MENU", self.menu_page),
            ("CLR", self.clear_screen),

            ("EXEC", self.execute_route),
            ("SIM START", self.start_simulation),
            ("PAUSE", self.pause_simulation),
            ("FUEL", self.fuel_page)
        ]

        for index, (text, command) in enumerate(buttons):

            button = tk.Button(
                keyboard,
                text=text,
                width=11,
                height=2,
                font=("Arial", 10, "bold"),
                command=command
            )

            button.grid(
                row=index // 4,
                column=index % 4,
                padx=5,
                pady=5
            )

        self.show_welcome()


    # EKRAN YAZMA


    def write_screen(self, text):

        self.screen.delete(
            "1.0",
            tk.END
        )

        self.screen.insert(
            tk.END,
            text
        )


    # BAŞLANGIÇ


    def show_welcome(self):

        self.write_screen(

            """
              FLIGHT MANAGEMENT COMPUTER

----------------------------------------------

                SYSTEM READY

              TRAINING MODE

----------------------------------------------

     INIT       RTE        LEGS

     DEP/ARR    VNAV       PROG

----------------------------------------------

       ENTER ROUTE TO BEGIN

"""
        )


    # INIT


    def init_page(self):

        self.current_page = "INIT"

        self.write_screen(

            """
                 INIT / IDENT

----------------------------------------------

 MODEL          TRAINING FMC

 DATABASE       SIMULATION

 AIRAC          DEMO DATABASE

 STATUS         READY

----------------------------------------------

 PURPOSE

 EDUCATIONAL FLIGHT MANAGEMENT
 COMPUTER SIMULATION

----------------------------------------------
"""
        )


    # RTE


    def rte_page(self):

        self.current_page = "RTE"

        text = """

                    RTE

----------------------------------------------

 ORIGIN       {}

 DEST         {}

----------------------------------------------

 ROUTE

""".format(

            self.origin or "----",
            self.destination or "----"
        )

        if self.route:

            for index, waypoint in enumerate(
                    self.route,
                    start=1
            ):

                text += f" {index:02d}   {waypoint}\n"

        else:

            text += "          NO WAYPOINTS\n"

        text += """

----------------------------------------------

 L1  ORIGIN

 L2  DESTINATION

 L3  ADD WAYPOINT

----------------------------------------------
"""

        self.write_screen(text)

    # =================================================
    # LEGS
    # =================================================

    def legs_page(self):

        self.current_page = "LEGS"

        text = """

                  LEGS

----------------------------------------------

"""

        if not self.route:

            text += "           NO ACTIVE LEGS\n"

        else:

            for index, waypoint in enumerate(
                    self.route,
                    start=1
            ):

                text += (
                    f" {index:02d}   "
                    f"{waypoint:<10} "
                    f"DIRECT\n"
                )

        text += """

----------------------------------------------

 ROUTE STATUS:
 {}
""".format(
            "ACTIVE" if self.route_active else "MODIFIED"
        )

        self.write_screen(text)


    # DEP / ARR


    def dep_arr_page(self):

        self.current_page = "DEPARR"

        self.write_screen(

            f"""
                 DEP / ARR

----------------------------------------------

 DEPARTURE

 {self.origin or "----"}

----------------------------------------------

 ARRIVAL

 {self.destination or "----"}

----------------------------------------------

 SID             NONE

 STAR            NONE

----------------------------------------------

 TRAINING DATABASE

"""
        )

    # =================================================
    # VNAV
    # =================================================

    def vnav_page(self):

        self.current_page = "VNAV"

        self.write_screen(

            f"""
                   VNAV

----------------------------------------------

 ALTITUDE

 CURRENT       {self.altitude:05d} FT

 TARGET        {self.target_altitude:05d} FT

----------------------------------------------

 SPEED

 CURRENT       {self.speed:03d} KT

 TARGET        {self.target_speed:03d} KT

----------------------------------------------

 VERTICAL PROFILE

 CLIMB / CRUISE / DESCENT

----------------------------------------------
"""
        )


    # PROGRESS


    def prog_page(self):

        self.current_page = "PROG"

        if self.speed > 0:

            hours = self.remaining_distance / self.speed

            minutes = int(hours * 60)

            eta = f"{minutes // 60:02d}:{minutes % 60:02d}"

        else:

            eta = "--:--"

        self.write_screen(

            f"""
                 PROGRESS

----------------------------------------------

 FROM

 {self.origin or "----"}

 TO

 {self.destination or "----"}

----------------------------------------------

 TOTAL DISTANCE

 {self.total_distance:.1f} NM

 REMAINING

 {self.remaining_distance:.1f} NM

----------------------------------------------

 ETA

 {eta}

 SPEED

 {self.speed} KT

----------------------------------------------
"""
        )


    # FUEL


    def fuel_page(self):

        self.current_page = "FUEL"

        used = self.initial_fuel - self.fuel

        self.write_screen(

            f"""
                   FUEL

----------------------------------------------

 INITIAL FUEL

 {self.initial_fuel:.0f} KG

----------------------------------------------

 USED

 {used:.1f} KG

----------------------------------------------

 REMAINING

 {self.fuel:.1f} KG

----------------------------------------------

 STATUS

 {"LOW FUEL" if self.fuel < 3000 else "NORMAL"}

----------------------------------------------
"""
        )


    # MENU


    def menu_page(self):

        self.current_page = "MENU"

        self.write_screen(

            """
                    MENU

----------------------------------------------

 < FMC

 < NAVIGATION

 < PERFORMANCE

 < AIRCRAFT

 < SYSTEM

----------------------------------------------

 SIMULATION SOFTWARE

 VERSION 1.0

"""
        )


    # SOL LSK


    def left_key(self, number):

        if number == 1:

            value = self.ask_input(
                "ORIGIN",
                "ICAO kalkış kodu:"
            )

            if value:

                value = value.upper()

                if value not in self.airports:

                    messagebox.showwarning(
                        "FMC",
                        "Bu demo veritabanında havalimanı yok."
                    )

                    return

                self.origin = value

            self.rte_page()

        elif number == 2:

            value = self.ask_input(
                "DESTINATION",
                "ICAO varış kodu:"
            )

            if value:

                value = value.upper()

                if value not in self.airports:

                    messagebox.showwarning(
                        "FMC",
                        "Bu demo veritabanında havalimanı yok."
                    )

                    return

                self.destination = value

            self.rte_page()

        elif number == 3:

            value = self.ask_input(
                "WAYPOINT",
                "Waypoint kodu:"
            )

            if value:

                self.route.append(
                    value.upper()
                )

            self.rte_page()

        elif number == 4:

            self.prog_page()

        elif number == 5:

            self.fuel_page()

        elif number == 6:

            self.vnav_page()


    # SAĞ LSK


    def right_key(self, number):

        if number == 1:

            self.execute_route()

        elif number == 2:

            self.clear_route()

        elif number == 3:

            self.fuel_page()

        else:

            messagebox.showinfo(
                "FMC",
                f"R{number} fonksiyonu."
            )


    # ROTA AKTİFLEŞTİRME KISMI


    def execute_route(self):

        if not self.origin or not self.destination:

            messagebox.showwarning(
                "FMC",
                "Önce ORIGIN ve DESTINATION giriniz."
            )

            return

        self.calculate_route()

        self.route_active = True

        self.rte_page()

        messagebox.showinfo(
            "FMC EXEC",
            "ROUTE ACTIVATED"
        )


    # MESAFE HESABI


    def calculate_route(self):

        if (
            self.origin not in self.airports
            or
            self.destination not in self.airports
        ):

            return

        lat1, lon1 = self.airports[self.origin]

        lat2, lon2 = self.airports[self.destination]

        self.total_distance = self.haversine(
            lat1,
            lon1,
            lat2,
            lon2
        )

        self.remaining_distance = self.total_distance


    # HAVERSINE denizmili olarak hesaplanmıstır


    def haversine(
        self,
        lat1,
        lon1,
        lat2,
        lon2
    ):

        R = 3440.065

        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        dlat = math.radians(lat2 - lat1)

        dlon = math.radians(
            lon2 - lon1
        )

        a = (
            math.sin(dlat / 2) ** 2
            +
            math.cos(lat1)
            *
            math.cos(lat2)
            *
            math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return R * c


    # SİMÜLASYON BAŞLAT


    def start_simulation(self):

        if not self.route_active:

            messagebox.showwarning(
                "FMC",
                "Önce EXEC ile rotayı aktive edin."
            )

            return

        if self.simulation_running:

            return

        self.simulation_running = True

        self.speed = 450

        self.simulation_loop()


    # SİMÜLASYON


    def simulation_loop(self):

        if not self.simulation_running:

            return

        if self.remaining_distance <= 0:

            self.remaining_distance = 0

            self.speed = 0

            self.simulation_running = False

            messagebox.showinfo(
                "FMC",
                "DESTINATION REACHED"
            )

            self.prog_page()

            return

        # Her döngüde yaklaşık 15 NM ilerle

        distance_step = 15

        self.remaining_distance -= distance_step

        if self.remaining_distance < 0:

            self.remaining_distance = 0

        # Yakıt tüketimi

        fuel_consumption = 90

        self.fuel -= fuel_consumption

        if self.fuel < 0:

            self.fuel = 0

        # İrtifa simülasyonu

        if self.altitude < self.target_altitude:

            self.altitude += 1500

            if self.altitude > self.target_altitude:

                self.altitude = self.target_altitude

        # Ekranı güncelle

        if self.current_page == "PROG":

            self.prog_page()

        elif self.current_page == "FUEL":

            self.fuel_page()

        elif self.current_page == "VNAV":

            self.vnav_page()

        # 1 saniye sonra tekrar

        self.root.after(
            1000,
            self.simulation_loop
        )


    # PAUSE


    def pause_simulation(self):

        self.simulation_running = False

        messagebox.showinfo(
            "FMC",
            "SIMULATION PAUSED"
        )


    # ROTA TEMİZLE


    def clear_route(self):

        self.route = []

        self.route_active = False

        self.remaining_distance = 0

        self.total_distance = 0

        self.rte_page()


    # EKRANI TEMİZLE


    def clear_screen(self):

        self.screen.delete(
            "1.0",
            tk.END
        )


    # VERİ GİRİŞİ


    def ask_input(
        self,
        title,
        message
    ):

        window = tk.Toplevel(
            self.root
        )

        window.title(title)

        window.geometry(
            "400x180"
        )

        window.transient(
            self.root
        )

        window.grab_set()

        label = tk.Label(
            window,
            text=message,
            font=("Arial", 11),
            background="white"
        )

        label.pack(
            pady=15
        )

        entry = tk.Entry(
            window,
            font=("Arial", 15),
            justify="center"
        )

        entry.pack()

        result = {
            "value": None
        }

        def confirm():

            value = entry.get().strip()

            if value:

                result["value"] = value

                window.destroy()

            else:

                messagebox.showwarning(
                    "FMC",
                    "Değer giriniz."
                )

        button = tk.Button(
            window,
            text="ENTER",
            width=12,
            height=2,
            command=confirm
        )

        button.pack(
            pady=15
        )

        entry.focus()

        self.root.wait_window(
            window
        )

        return result["value"]



# PROGRAM BAŞLAT


if __name__ == "__main__":

    root = tk.Tk()

    app = FMC(root)

    root.mainloop()
