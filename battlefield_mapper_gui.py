from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont
from PIL import ImageTk, Image
from transmitters import Transmitter
import tkintermapview, os, types, math, sympy
from maps import set_nice_marker, CanvasPositionMarkerNice

class Window(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight() - 54
        self.devices = ["usb1", "usb2", "usb3"]
        self.clasifications = ["Section", "Platoon", "Company HQ", "Battalion HQ", "Regiment HQ"]
        self.selected_transmitter = ""
        self.friendly_transmitters = []
        self.enemy_transmitters = []
        self.blocked = False
        self.nato_toggle = True

        self.title_font = tkFont.Font(family = "Raleway", size = -(int(self.width * 0.044)), weight = "bold")
        self.heading_font = tkFont.Font(family = "Raleway", size = -(int(self.width * 0.02)), weight = "normal")
        self.text_font = tkFont.Font(family = "Raleway", size = -(int(self.width * 0.01)), weight = "normal")
        self.selection_font = tkFont.Font(family = "Raleway", size = -(int(self.width * 0.0075)), weight = "normal")
        self.button_font = tkFont.Font(family = "Raleway", size = -(int(self.width * 0.0075)), weight = "bold")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TEntry", foreground = "white", background = "#26242f", fieldbackground="#26242f", relief = "flat", highlightbackground = "white", highlightcolor = "white", insertcolor = "white")
        self.style.configure("TCombobox", foreground = "white", background = "#26242f", fieldbackground = "#26242f", arrowcolor = "white", focusfill = "#26242f", selectedbackground = "#26242f", selectedforground = "white")
        self.style.configure("TButton", foreground = "#26242f", background = "white", font = self.button_font, bordercolor = "#26242f")
        self.style.map('TCombobox', background=[('hover', 'white')], arrowcolor = [('hover', '#26242f')])
        self.style.map('TButton', background=[('hover', '#26242f')], foreground = [('hover', 'white')])

        self.option_add("*TCombobox*Listbox*Background", 'white')
        self.option_add("*TCombobox*Listbox*Foreground", '#26242f')
        self.option_add("*TCombobox*Listbox*Font", self.selection_font)

        self.frame = Frame(self)

        self.left_frame = Frame(self.frame, width = (self.width * 0.7) - 8, height = self.height)
        self.divider_3_frame = Frame(self.frame, width = 8, height = self.height)
        self.right_frame = Frame(self.frame, width = self.width * 0.3, height = self.height)

        self.header_frame = Frame(self.left_frame, width = (self.width * 0.7) - 8, height = self.height * 0.1)
        self.main_frame = Frame(self.left_frame, width = (self.width * 0.7) - 8, height = self.height * 0.8)
        self.footer_frame = Frame(self.left_frame, width = (self.width * 0.7) - 8, height = self.height * 0.1)

        self.logo_frame = Frame(self.header_frame, width = self.height * 0.1, height = self.height * 0.1)
        self.title_frame = Frame(self.header_frame, width = self.width - (self.height * 0.1), height = self.height * 0.1)

        self.divider_3_top_padding = Frame(self.divider_3_frame, width = 3, height = self.height * 0.01)
        self.divider_3 = Frame(self.divider_3_frame, width = 3, height = self.height * 0.98)
        self.divider_3_bottom_padding = Frame(self.divider_3_frame, width = 3, height = self.height * 0.01)

        self.device_frame = Frame(self.right_frame, width = self.width * 0.3, height = self.height * 0.22)
        self.divider_1_frame = Frame(self.right_frame, width = self.width * 0.3, height = 3)
        self.settings_frame = Frame(self.right_frame, width = self.width * 0.3, height = self.height * 0.2)
        self.divider_2_frame = Frame(self.right_frame, width = self.width * 0.3, height = 3)
        self.info_frame = Frame(self.right_frame, width = self.width * 0.3, height = (self.height * 0.58) - 6)

        self.divider_1_left_padding = Frame(self.divider_1_frame, width = self.width * 0.01, height = 3)
        self.divider_1 = Frame(self.divider_1_frame, width = self.width * 0.28, height = 3)
        self.divider_1_right_padding = Frame(self.divider_1_frame, width = self.width * 0.01, height = 3)

        self.divider_2_left_padding = Frame(self.divider_2_frame, width = self.width * 0.01, height = 3)
        self.divider_2 = Frame(self.divider_2_frame, width = self.width * 0.28, height = 3)
        self.divider_2_right_padding = Frame(self.divider_2_frame, width = self.width * 0.01, height = 3)

        self.map_left_padding_frame = Frame(self.main_frame, width = (self.width * 0.035), height = self.height * 0.8)
        self.map_frame = Frame(self.main_frame, width = (self.width * 0.63) - 8, height = self.height * 0.8)
        self.map_right_padding_frame = Frame(self.main_frame, width = (self.width * 0.035), height = self.height * 0.8)

        self.frame.pack(expand=True)

        self.left_frame.grid(row = 0, column = 0, sticky = N + W)
        self.left_frame.grid_propagate(False)
        self.divider_3_frame.grid(row = 0, column = 1, sticky = N + W)
        self.divider_3_frame.grid_propagate(False)
        self.right_frame.grid(row = 0, column = 2, sticky = N + W)
        self.right_frame.grid_propagate(False)

        self.header_frame.grid(row = 0, column = 0, sticky = N + W)
        self.header_frame.grid_propagate(False)
        self.main_frame.grid(row = 1, column = 0, sticky = N + W)
        self.main_frame.grid_propagate(False)
        self.footer_frame.grid(row = 2, column = 0, sticky = N + W)
        self.footer_frame.grid_propagate(False)

        self.logo_frame.grid(row = 0, column = 0, sticky = N + W)
        self.logo_frame.grid_propagate(False)
        self.title_frame.grid(row = 0, column = 1, sticky = N + W)
        self.title_frame.grid_propagate(False)

        self.divider_3_top_padding.grid(row = 0, column = 0, sticky = N + W)
        self.logo_frame.grid_propagate(False)
        self.divider_3.grid(row = 1, column = 0, sticky = N + W)
        self.logo_frame.grid_propagate(False)
        self.divider_3_bottom_padding.grid(row = 2, column = 0, sticky = N + W)
        self.logo_frame.grid_propagate(False)

        self.device_frame.grid(row = 0, column = 0, sticky = N + W)
        self.device_frame.grid_propagate(False)
        self.divider_1_frame.grid(row = 1, column = 0, sticky = N + W)
        self.divider_1_frame.grid_propagate(False)
        self.settings_frame.grid(row = 2, column = 0, sticky = N + W)
        self.settings_frame.grid_propagate(False)
        self.divider_2_frame.grid(row = 3, column = 0, sticky = N + W)
        self.divider_2_frame.grid_propagate(False)
        self.info_frame.grid(row = 4, column = 0, sticky = N + W)
        self.info_frame.grid_propagate(False)

        self.divider_1_left_padding.grid(row = 0, column = 0, sticky = N + W)
        self.divider_1_left_padding.grid_propagate(False)
        self.divider_1.grid(row = 0, column = 1, sticky = N + W)
        self.divider_1.grid_propagate(False)
        self.divider_1_right_padding.grid(row = 0, column = 2, sticky = N + W)
        self.divider_1_right_padding.grid_propagate(False)

        self.divider_2_left_padding.grid(row = 0, column = 0, sticky = N + W)
        self.divider_2_left_padding.grid_propagate(False)
        self.divider_2.grid(row = 0, column = 1, sticky = N + W)
        self.divider_2.grid_propagate(False)
        self.divider_2_right_padding.grid(row = 0, column = 2, sticky = N + W)
        self.divider_2_right_padding.grid_propagate(False)

        self.map_left_padding_frame.grid(row = 0, column = 0, sticky = N + W)
        self.map_left_padding_frame.grid_propagate(False)
        self.map_frame.grid(row = 0, column = 1, sticky = N + W)
        self.map_frame.grid_propagate(False)
        self.map_right_padding_frame.grid(row = 0, column = 2, sticky = N + W)
        self.map_right_padding_frame.grid_propagate(False)

        self.logo_frame.configure(background = "#26242f")
        self.title_frame.configure(background = "#26242f")
        self.device_frame.configure(background = "#26242f")
        self.divider_1_left_padding.configure(background = "#26242f")
        self.divider_1.configure(background = "white")
        self.divider_1_right_padding.configure(background = "#26242f")
        self.settings_frame.configure(background = "#26242f")
        self.divider_2_left_padding.configure(background = "#26242f")
        self.divider_2.configure(background = "white")
        self.divider_2_right_padding.configure(background = "#26242f")
        self.divider_3_frame.configure(background = "#26242f")
        self.divider_3_top_padding.configure(background = "#26242f")
        self.divider_3.configure(background = "white")
        self.divider_3_bottom_padding.configure(background = "#26242f")
        self.info_frame.configure(background = "#26242f")
        self.main_frame.configure(background = "#26242f")
        self.footer_frame.configure(background = "#26242f")
        self.map_left_padding_frame.configure(background = "#26242f")
        self.map_frame.configure(background = "#26242f")
        self.map_right_padding_frame.configure(background = "#26242f")

        self.logo_canvas = Canvas(self.logo_frame, width = self.height * 0.1, height = self.height * 0.1, bd = 0, highlightthickness = 0, relief='ridge', bg = "#26242f")
        self.logo_canvas.grid(sticky = E)
        self.sized_logo = Image.open(("images/mod_logo.png"))
        self.resized_logo = self.sized_logo.resize((int(self.height * 0.1), int(self.height * 0.1)), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.resized_logo)
        self.logo_canvas.create_image(0, 0, anchor = N+W, image = self.logo)

        self.title = Label(self.title_frame, text = "RADIO BATTLEFIELD MAPPER", fg = "white", bg = "#26242f")
        self.title.config(font = self.title_font)
        self.title.grid(row = 0, column = 0, sticky = N + S + W)

        self.device_title = Label(self.device_frame, text = "DETECTORS:", fg = "white", bg = "#26242f")
        self.device_title.config(font = self.heading_font)
        self.device_title.grid(row = 0, column = 0, sticky = N + S + W, columnspan = 4, padx = 10)

        self.detector_1_canvas = Canvas(self.device_frame, width = self.height * 0.05, height = self.height * 0.05, bd = 0, highlightthickness = 0, relief='ridge', bg = "#26242f")
        self.detector_1_canvas.grid(row = 1, column = 0, sticky = W, padx = 5)
        self.sized_detector_1 = Image.open(("images/detector_1.png"))
        self.resized_detector_1 = self.sized_detector_1.resize((int(self.height * 0.05), int(self.height * 0.05)), Image.ANTIALIAS)
        self.detector_1 = ImageTk.PhotoImage(self.resized_detector_1)
        self.detector_1_canvas.create_image(0, 0, anchor = N+W, image = self.detector_1)

        self.detector_1_device = ttk.Combobox(self.device_frame, width = 10, font = self.selection_font)
        self.detector_1_device["values"] = self.devices
        self.detector_1_device.grid(row = 1, column = 1, padx = 5, ipady = 2)

        self.detector_1_lat_label = Label(self.device_frame, text = "Lat:", fg = "white", bg = "#26242f")
        self.detector_1_lat_label.config(font = self.text_font)
        self.detector_1_lat_label.grid(row = 1, column = 2, sticky = N + S + W)

        self.detector_1_lat = StringVar(self, "52.34902873378519")
        self.detector_1_lat_entry = ttk.Entry(self.device_frame, textvariable = self.detector_1_lat, font = self.selection_font, width = 12)
        self.detector_1_lat_entry.grid(row = 1, column = 3, padx = 5, ipady=2)

        self.detector_1_long_label = Label(self.device_frame, text = "Long:", fg = "white", bg = "#26242f")
        self.detector_1_long_label.config(font = self.text_font)
        self.detector_1_long_label.grid(row = 1, column = 4)
        
        self.detector_1_long = StringVar(self, "-1.583893926455627")
        self.detector_1_long_entry = ttk.Entry(self.device_frame, textvariable = self.detector_1_long, font = self.selection_font, width = 12)
        self.detector_1_long_entry.grid(row = 1, column = 5, padx = 5, ipady=2)

        self.detector_2_canvas = Canvas(self.device_frame, width = self.height * 0.05, height = self.height * 0.05, bd = 0, highlightthickness = 0, relief='ridge', bg = "#26242f")
        self.detector_2_canvas.grid(row = 2, column = 0, sticky = W, padx = 5)
        self.sized_detector_2 = Image.open(("images/detector_2.png"))
        self.resized_detector_2 = self.sized_detector_2.resize((int(self.height * 0.05), int(self.height * 0.05)), Image.ANTIALIAS)
        self.detector_2 = ImageTk.PhotoImage(self.resized_detector_2)
        self.detector_2_canvas.create_image(0, 0, anchor = N+W, image = self.detector_2)

        self.detector_2_device = ttk.Combobox(self.device_frame, width = 10, font = self.selection_font)
        self.detector_2_device["values"] = self.devices
        self.detector_2_device.grid(row = 2, column = 1, padx = 5, ipady = 2)

        self.detector_2_lat_label = Label(self.device_frame, text = "Lat:", fg = "white", bg = "#26242f")
        self.detector_2_lat_label.config(font = self.text_font)
        self.detector_2_lat_label.grid(row = 2, column = 2, sticky = N + S + W)

        self.detector_2_lat = StringVar(self, "52.34618433354199")
        self.detector_2_lat_entry = ttk.Entry(self.device_frame, textvariable = self.detector_2_lat, font = self.selection_font, width = 12)
        self.detector_2_lat_entry.grid(row = 2, column = 3, padx = 5, ipady=2)

        self.detector_2_long_label = Label(self.device_frame, text = "Long:", fg = "white", bg = "#26242f")
        self.detector_2_long_label.config(font = self.text_font)
        self.detector_2_long_label.grid(row = 2, column = 4)

        self.detector_2_long = StringVar(self, "-1.5790015774080997")
        self.detector_2_long_entry = ttk.Entry(self.device_frame, textvariable = self.detector_2_long, font = self.selection_font, width = 12)
        self.detector_2_long_entry.grid(row = 2, column = 5, padx = 5, ipady=2)
        
        self.detector_3_canvas = Canvas(self.device_frame, width = self.height * 0.05, height = self.height * 0.05, bd = 0, highlightthickness = 0, relief='ridge', bg = "#26242f")
        self.detector_3_canvas.grid(row = 3, column = 0, sticky = W, padx = 5)
        self.sized_detector_3 = Image.open(("images/detector_3.png"))
        self.resized_detector_3 = self.sized_detector_3.resize((int(self.height * 0.05), int(self.height * 0.05)), Image.ANTIALIAS)
        self.detector_3 = ImageTk.PhotoImage(self.resized_detector_3)
        self.detector_3_canvas.create_image(0, 0, anchor = N+W, image = self.detector_3)

        self.detector_3_device = ttk.Combobox(self.device_frame, width = 10, font = self.selection_font)
        self.detector_3_device["values"] = self.devices
        self.detector_3_device.grid(row = 3, column = 1, padx = 5, ipady = 2)

        self.detector_3_lat_label = Label(self.device_frame, text = "Lat:", fg = "white", bg = "#26242f")
        self.detector_3_lat_label.config(font = self.text_font)
        self.detector_3_lat_label.grid(row = 3, column = 2, sticky = N + S + W)

        self.detector_3_lat = StringVar(self, "52.34612155627798")
        self.detector_3_lat_entry = ttk.Entry(self.device_frame, textvariable = self.detector_3_lat, font = self.selection_font, width = 12)
        self.detector_3_lat_entry.grid(row = 3, column = 3, padx = 5, ipady=2)

        self.detector_3_long_label = Label(self.device_frame, text = "Long:", fg = "white", bg = "#26242f")
        self.detector_3_long_label.config(font = self.text_font)
        self.detector_3_long_label.grid(row = 3, column = 4)
        
        self.detector_3_long = StringVar(self, "-1.586258129005962")
        self.detector_3_long_entry = ttk.Entry(self.device_frame, textvariable = self.detector_3_long, font = self.selection_font, width = 12)
        self.detector_3_long_entry.grid(row = 3, column = 5, padx = 5, ipady=2)

        self.settings_title = Label(self.settings_frame, text = "SETTINGS:", fg = "white", bg = "#26242f")
        self.settings_title.config(font = self.heading_font)
        self.settings_title.grid(row = 0, column = 0, sticky = N + S + W, columnspan = 4, padx = 10)

        self.friendly_frequency_label = Label(self.settings_frame, text = "Friendly Frequency:", fg = "white", bg = "#26242f")
        self.friendly_frequency_label.config(font = self.text_font)
        self.friendly_frequency_label.grid(row = 1, column = 0, sticky = W, padx = 10)

        self.friendly_frequency_entry = ttk.Entry(self.settings_frame, font = self.selection_font, width = 12)
        self.friendly_frequency_entry.grid(row = 1, column = 1, padx = 5, ipady=2)

        self.friendly_frequency_label_end = Label(self.settings_frame, text = "Mhz", fg = "white", bg = "#26242f")
        self.friendly_frequency_label_end.config(font = self.text_font)
        self.friendly_frequency_label_end.grid(row = 1, column = 2, sticky = W)

        self.enemy_frequency_label = Label(self.settings_frame, text = "Enemy Frequency:", fg = "white", bg = "#26242f")
        self.enemy_frequency_label.config(font = self.text_font)
        self.enemy_frequency_label.grid(row = 2, column = 0, sticky = W, pady = 20, padx = 10)

        self.enemy_frequency_entry = ttk.Entry(self.settings_frame, font = self.selection_font, width = 12)
        self.enemy_frequency_entry.grid(row = 2, column = 1, padx = 5, ipady=2)

        self.enemy_frequency_label_end = Label(self.settings_frame, text = "Mhz", fg = "white", bg = "#26242f")
        self.enemy_frequency_label_end.config(font = self.text_font)
        self.enemy_frequency_label_end.grid(row = 2, column = 2, sticky = W)

        self.nato_symbols_label = Label(self.settings_frame, text = "Predict Classification:", fg = "white", bg = "#26242f")
        self.nato_symbols_label.config(font = self.text_font)
        self.nato_symbols_label.grid(row = 3, column = 0, sticky = W, columnspan = 2, padx = 10)

        self.predict_classification = IntVar()
        self.predict_classification_box = Checkbutton(self.settings_frame, fg = "white", bg = "#26242f", variable = self.predict_classification)
        self.predict_classification_box.grid(row = 3, column = 1, sticky = W, padx = 10)

        self.run_button = ttk.Button(self.settings_frame, text = "Run Mapper", command = self.runButtonPressed)
        self.run_button.grid(row = 3, column = 2, sticky = W, columnspan = 2, padx = 20)

        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.database_path = os.path.join(self.script_directory, "offline_map.db")

        self.funcType = types.MethodType
        self.map = tkintermapview.TkinterMapView(self.map_frame, width = (self.width * 0.63) - 8, height = self.height * 0.8, corner_radius=10, use_database_only=True, max_zoom=19, database_path=self.database_path)
        self.map.set_marker = self.funcType(set_nice_marker, self.map)
        self.map.grid(row = 0, column = 0, sticky = E)
        self.map.set_position(52.38357295014132, -1.560884717814845)
        self.map.set_zoom(7)
        self.map.add_left_click_map_command(self.deselectTransmitter)
        self.map.add_right_click_menu_command(label="Deselect Transmitter", command=self.deselectTransmitter)
        self.map.add_right_click_menu_command(label="Toggle NATO Symbols", command=self.toggleNATOSymbols)

        self.pack()
    
    def runButtonPressed(self):
        if self.detector_1_device.get() in self.devices and self.detector_2_device.get() in self.devices and self.detector_3_device.get() in self.devices:
            try:
                float(self.detector_1_lat.get())
                float(self.detector_1_long.get())

                float(self.detector_2_lat.get())
                float(self.detector_2_lat.get())

                float(self.detector_3_lat.get())
                float(self.detector_3_lat.get())
            except:
                print("Error")
                return
            
            self.detector_1_device.configure(state = "disabled")
            self.detector_2_device.configure(state = "disabled")
            self.detector_3_device.configure(state = "disabled")

            self.detector_1_lat_entry.configure(state = "disabled")
            self.detector_1_long_entry.configure(state = "disabled")

            self.detector_2_lat_entry.configure(state = "disabled")
            self.detector_2_long_entry.configure(state = "disabled")

            self.detector_3_lat_entry.configure(state = "disabled")
            self.detector_3_long_entry.configure(state = "disabled")
        
        else:
            print("Error")
            return


        try:
            if (int(self.friendly_frequency_entry.get()) >= 24 and int(self.friendly_frequency_entry.get()) <= 1766) and (int(self.enemy_frequency_entry.get()) >= 24 and int(self.enemy_frequency_entry.get()) <= 1766):
                pass

            else:
                print("Error")
                return
        except:
            print("Error")
            return

        self.friendly_frequency = self.friendly_frequency_entry.get()
        self.enemy_frequency = self.enemy_frequency_entry.get()
        self.predict = self.predict_classification.get()

        self.detector_1_marker = self.map.set_marker(float(self.detector_1_lat.get()), float(self.detector_1_long.get()), marker_color_circle = "white", marker_color_outside = "#f1c631", data = "detector")
        self.detector_2_marker = self.map.set_marker(float(self.detector_2_lat.get()), float(self.detector_2_long.get()), marker_color_circle = "white", marker_color_outside = "#f1c631", data = "detector")
        self.detector_3_marker = self.map.set_marker(float(self.detector_3_lat.get()), float(self.detector_3_long.get()), marker_color_circle = "white", marker_color_outside = "#f1c631", data = "detector")


        self.friendly_frequency_entry.configure(state = "disabled")
        self.enemy_frequency_entry.configure(state = "disabled")
        self.predict_classification_box.configure(state = "disabled")

        transmitter = self.processBearing(157.9234969398929, 283.587192488583, 71.11198705571883)
        self.addTransmitter(transmitter[1], transmitter[0], 60)

        transmitter = self.processBearing(33.66678688841918, 25.852763273405095, 34.11773634251195)
        self.addTransmitter(transmitter[1], transmitter[0], 60)

        transmitter = self.processBearing(181.0847129803221, 185.33051942482112, 179.09372065420987)
        self.addTransmitter(transmitter[1], transmitter[0], 24)

    def toggleNATOSymbols(self, event=None):
        self.nato_toggle = not self.nato_toggle
        for friendly_transmitter in self.friendly_transmitters:
            self.updateMarker(friendly_transmitter)

        for enemy_transmitter in self.enemy_transmitters:
            self.updateMarker(enemy_transmitter)
    
    def addTransmitter(self, lat, long, frequency):
        transmitter = Transmitter(lat, long, frequency, self.predict)
        if str(frequency) == self.friendly_frequency:
            self.friendly_transmitters.append(transmitter)
            designation = "Friendly"
            colour = "#000574"
            transmitter.uid = len(self.friendly_transmitters)
            
        elif str(frequency) == self.enemy_frequency:
            self.enemy_transmitters.append(transmitter)
            designation = "Enemy"
            colour = "#af0001"
            transmitter.uid = len(self.enemy_transmitters)

        else:
            return
        
        if self.nato_toggle == True and transmitter.classification:
            sized_nato_symbol = Image.open(("images/" + designation + "_" + transmitter.classification.replace(" ", "_" ).lower() + "_map.png"))
            resized_nato_symbol = sized_nato_symbol.resize((int(self.height * 0.06), int(self.height * 0.06)), Image.ANTIALIAS)
            nato_symbol = ImageTk.PhotoImage(resized_nato_symbol)
            marker = self.map.set_marker(lat, long, command = lambda x: self.displayTransmitterInformation(transmitter) , marker_color_circle = "white", marker_color_outside = colour, image = nato_symbol, image_zoom_visibility = (8, float('inf')), text = transmitter.uid, text_color = colour)
            transmitter.addMarker(marker)
            
        else:
            marker = self.map.set_marker(lat, long, command = lambda x: self.displayTransmitterInformation(transmitter), marker_color_circle = "white", marker_color_outside = colour, text = transmitter.uid, text_color = colour)
            transmitter.addMarker(marker)
    
    def updateMarker(self, transmitter):
        self.map.delete(transmitter.marker)

        if str(transmitter.frequency) == self.friendly_frequency:
            designation = "Friendly"
            colour = "#000574"
            
        elif str(transmitter.frequency) == self.enemy_frequency:
            designation = "Enemy"
            colour = "#af0001"
        else:
            return

        if self.nato_toggle == 1:
            sized_nato_symbol = Image.open(("images/" + designation + "_" + transmitter.classification.replace(" ", "_" ).lower() + "_map.png"))
            resized_nato_symbol = sized_nato_symbol.resize((int(self.height * 0.06), int(self.height * 0.06)), Image.ANTIALIAS)
            nato_symbol = ImageTk.PhotoImage(resized_nato_symbol)
            marker = self.map.set_marker(transmitter.lat, transmitter.long, command = lambda x: self.displayTransmitterInformation(transmitter) , marker_color_circle = "white", marker_color_outside = colour, image = nato_symbol, image_zoom_visibility = (8, float('inf')), text = transmitter.uid, text_color = colour)
            transmitter.addMarker(marker)
            
        else:
            marker = self.map.set_marker(transmitter.lat, transmitter.long, command = lambda x: self.displayTransmitterInformation(transmitter), marker_color_circle = "white", marker_color_outside = colour, text = transmitter.uid, text_color = colour)
            transmitter.addMarker(marker)

    def deselectTransmitter(self, event=None):
        if self.blocked != True:
            for widget in self.info_frame.winfo_children():
                widget.destroy()
        else:
            self.blocked = False

    def displayTransmitterInformation(self, transmitter, event=None):
        self.blocked = True
        self.selected_transmitter = transmitter

        self.info_title = Label(self.info_frame, text = "Transmitter Information:", fg = "white", bg = "#26242f")
        self.info_title.config(font = self.heading_font)
        self.info_title.grid(row = 0, column = 0, sticky = N + S + W, columnspan = 4, padx = 10)

        self.transmitter_name_label = Label(self.info_frame, text = "Name:", fg = "white", bg = "#26242f")
        self.transmitter_name_label.config(font = self.text_font)
        self.transmitter_name_label.grid(row = 1, column = 0, sticky = W, pady = 20, padx = 10)

        self.transmitter_name = StringVar(self, self.selected_transmitter.name)
        self.transmitter_name_entry = ttk.Entry(self.info_frame, textvariable = self.transmitter_name, font = self.selection_font, width = 12)
        self.transmitter_name_entry.grid(row = 1, column = 1, ipady = 2, pady = 20, sticky = "")

        self.transmitter_classification_label = Label(self.info_frame, text = "Classification:", fg = "white", bg = "#26242f")
        self.transmitter_classification_label.config(font = self.text_font)
        self.transmitter_classification_label.grid(row = 1, column = 2, sticky = W, padx = 10)

        self.transmitter_classification = ttk.Combobox(self.info_frame, width = 12, font = self.selection_font)
        self.transmitter_classification["values"] = self.clasifications

        if self.predict == 1:
            self.transmitter_classification.current(self.clasifications.index(self.selected_transmitter.classification))

        self.transmitter_classification.bind("<<ComboboxSelected>>", self.displayNatoSymbol)
        self.transmitter_classification.grid(row = 1, column = 3, padx = 5, ipady = 2, sticky = "") 

        self.transmitter_lat_label = Label(self.info_frame, text = "Lat:", fg = "white", bg = "#26242f")
        self.transmitter_lat_label.config(font = self.text_font)
        self.transmitter_lat_label.grid(row = 4, column = 0, sticky = W, padx = 10)

        self.transmitter_lat = Label(self.info_frame, text = self.selected_transmitter.lat, fg = "white", bg = "#26242f")
        self.transmitter_lat.config(font = self.text_font)
        self.transmitter_lat.grid(row = 4, column = 1, sticky = W)

        self.transmitter_long_label = Label(self.info_frame, text = "Long:", fg = "white", bg = "#26242f")
        self.transmitter_long_label.config(font = self.text_font)
        self.transmitter_long_label.grid(row = 4, column = 2, sticky = W, padx = 10)

        self.transmitter_long = Label(self.info_frame, text = self.selected_transmitter.long, fg = "white", bg = "#26242f")
        self.transmitter_long.config(font = self.text_font)
        self.transmitter_long.grid(row = 4, column = 3, sticky = W)

        self.transmitter_grid_label = Label(self.info_frame, text = "Grid Ref:", fg = "white", bg = "#26242f")
        self.transmitter_grid_label.config(font = self.text_font)
        self.transmitter_grid_label.grid(row = 5, column = 0, sticky = W, pady = 20, padx = 10)

        self.transmitter_grid = Label(self.info_frame, text = self.selected_transmitter.grid_ref, fg = "white", bg = "#26242f")
        self.transmitter_grid.config(font = self.text_font)
        self.transmitter_grid.grid(row = 5, column = 1, sticky = W, pady = 20)

        self.transmitter_frequency_label = Label(self.info_frame, text = "Frequency:", fg = "white", bg = "#26242f")
        self.transmitter_frequency_label.config(font = self.text_font)
        self.transmitter_frequency_label.grid(row = 5, column = 2, sticky = W, pady = 20, padx = 10)

        self.transmitter_frequency = Label(self.info_frame, text = str(self.selected_transmitter.frequency) + " Mhz", fg = "white", bg = "#26242f")
        self.transmitter_frequency.config(font = self.text_font)
        self.transmitter_frequency.grid(row = 5, column = 3, sticky = W, pady = 20)

        self.transmitter_number_label = Label(self.info_frame, text = "No. Transmissions:", fg = "white", bg = "#26242f")
        self.transmitter_number_label.config(font = self.text_font)
        self.transmitter_number_label.grid(row = 6, column = 0, sticky = W, columnspan = 2, padx = 10)

        self.transmitter_number = Label(self.info_frame, text = (f"{self.selected_transmitter.transmission_number:04d}"), fg = "white", bg = "#26242f")
        self.transmitter_number.config(font = self.text_font)
        self.transmitter_number.grid(row = 6, column = 1, sticky = E, padx = 10)

        self.save_button = ttk.Button(self.info_frame, text = "Save", command = self.savedButtonPressed)
        self.save_button.grid(row = 6, column = 2, sticky = "", columnspan = 2)

        self.nato_symbol_frame = Frame(self.info_frame, width = self.width * 0.29, height = self.height * 0.25)
        self.nato_symbol_frame.grid(row = 7, column = 0, sticky = W, columnspan = 5, pady = 20)
        
        self.nato_symbol_padding_left = Frame(self.nato_symbol_frame, width = ((self.width * 0.29) - (self.height * 0.25)) / 2, height = self.height * 0.25)
        self.nato_symbol_padding_left.grid(row = 7, column = 0, sticky = W)
        self.nato_symbol_padding_left.configure(background = "#26242f")

        self.nato_symbol_centre = Frame(self.nato_symbol_frame, width = self.height * 0.25, height = self.height * 0.25)
        self.nato_symbol_centre.grid(row = 7, column = 1, sticky = W)

        self.nato_symbol_padding_right = Frame(self.nato_symbol_frame, width = ((self.width * 0.29) - (self.height * 0.25)) / 2, height = self.height * 0.25)
        self.nato_symbol_padding_right.grid(row = 7, column = 2, sticky = W)
        self.nato_symbol_padding_right.configure(background = "#26242f")

        self.nato_symbol_canvas = Canvas(self.nato_symbol_centre, width = self.height * 0.25, height = self.height * 0.25, bd = 0, highlightthickness = 0, relief='ridge', bg = "#26242f")
        self.nato_symbol_canvas.grid(sticky = "")

        if self.transmitter_classification.get() != "":
            self.displayNatoSymbol()

    def displayNatoSymbol(self, event=None):
        self.nato_symbol_canvas.delete("all")

        if str(self.selected_transmitter.frequency) == self.friendly_frequency:
            designation = "Friendly"
        elif str(self.selected_transmitter.frequency) == self.enemy_frequency:
            designation = "Enemy"
        else:
            return

        self.sized_nato_symbol = Image.open(("images/" + designation + "_" + self.transmitter_classification.get().replace(" ", "_" ).lower() + ".png"))
        self.resized_nato_symbol = self.sized_nato_symbol.resize((int(self.height * 0.25), int(self.height * 0.25)), Image.ANTIALIAS)
        self.nato_symbol = ImageTk.PhotoImage(self.resized_nato_symbol)
        self.nato_symbol_canvas.create_image(0, 0, anchor = N+W, image = self.nato_symbol)
    
    def savedButtonPressed(self):
        if self.transmitter_name.get():
            self.selected_transmitter.name = self.transmitter_name.get()

        if self.transmitter_classification.get() in self.clasifications:
            self.selected_transmitter.classification = self.transmitter_classification.get()
            self.selected_transmitter.estimate = 0

            self.updateMarker(self.selected_transmitter)
        else:
            self.transmitter_classification.current(self.clasifications.index(self.selected_transmitter.classification))
            print("Error")
    
    def processBearing(self, a1, a2, a3):
        x,y = sympy.symbols('x,y')
        radian = math.pi / 180
        
        eq1 = sympy.Eq(y - (1 / math.tan(a1 * radian)) * x, float(self.detector_1_lat.get()) - ((1 / math.tan(a1 * radian)) * float(self.detector_1_long.get())))
        eq2 = sympy.Eq(y - (1 / math.tan(a2 * radian)) * x, float(self.detector_2_lat.get()) - ((1 / math.tan(a2 * radian)) * float(self.detector_2_long.get())))
        eq3 = sympy.Eq(y - (1 / math.tan(a3 * radian)) * x, float(self.detector_3_lat.get()) - ((1 / math.tan(a3 * radian)) * float(self.detector_3_long.get())))

        rst1 = sympy.solve([eq1, eq2], (x, y))
        rst2 = sympy.solve([eq2, eq3], (x, y))
        rst3 = sympy.solve([eq1, eq3], (x, y))
        
        x_array = [float(rst1[x]), float(rst2[x]), float(rst3[x])]
        y_array = [float(rst1[y]), float(rst2[y]), float(rst3[y])]
        center = sum(x_array)/len(x_array), sum(y_array)/len(y_array)
        return center

root = Tk()
window_frame = Window(root)
root.title("RADIO BATTLEFIELD MAPPER")
root.geometry(str(window_frame.width) + "x" + str(window_frame.height) + "+0+0")
root.resizable(False, False)
root.mainloop()
