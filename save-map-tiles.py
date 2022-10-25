import tkintermapview
import os
top_left_position = (59.053445, -12.224156)
bottom_right_position = (50.194274, 2.752987)
zoom_min = 16
zoom_max = 16
script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, "offline_map.db")
loader = tkintermapview.OfflineLoader(path=database_path)
loader.save_offline_tiles(top_left_position, bottom_right_position, zoom_min, zoom_max)
loader.print_loaded_sections()