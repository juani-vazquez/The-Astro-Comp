from datetime import datetime
from app.observable import get_observable_objects
from app.locator import locate_nearby_stars
from app.mapper import create_map
from app.research import research_star

intro = r"""

 .    '                   .  "   '
            .  .  .                 '      '
    "`       .   .
                                     '     '
  .    '      _______________
          ==c(___(o(______(_()
                   |=\\
                   )=\\
                   //|\\
                  //|| \\
                 // ||  \\
                //  ||   \\
               //         \\
 _____ _               _         _                ____                      
|_   _| |__   ___     / \    ___| |_ _ __ ___    / ___|___  _ __ ___  _ __  
  | | | '_ \ / _ \   / _ \  / __| __| '__/ _ \  | |   / _ \| '_ ` _ \| '_ \ 
  | | | | | |  __/  / ___ \ \__ \ |_| | | (_) | | |__| (_) | | | | | | |_) |
  |_| |_| |_|\___| /_/   \_\ \___/\__|_| \___/   \____\___/|_| |_| |_| .__/ 
                                                                     |_|    
    By Juani Vazquez
"""


def start_cli():
    print(intro)
    
    while True:
        command = input("> ")

        if command == "location":
            # Create the interactive map
            create_map('map.html')

        elif command == "sky":
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            time_str = input("Enter time (YYYY-MM-DD HH:MM:SS): ")
            time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

            observable_objects = get_observable_objects(latitude, longitude, time)

        elif command == "locate":
            #latitude = float(input("Enter latitude: "))
            #longitude = float(input("Enter longitude: "))
            #time_str = input("Enter time (YYYY-MM-DD HH:MM:SS): ")
            #time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            
            #input_altitude = float(input("Enter altitude (degrees): "))
            #input_azimuth = float(input("Enter azimuth (degrees): "))
            #plot = input("Plot? (True/False): ")
            
            latitude = -58.5
            longitude = -34.5
            time_str = "2024-11-26 11:00:00"
            time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            input_altitude = 31.50
            input_azimuth = 175.63
            plot = "True"

            if plot == "True":
                locate_nearby_stars(latitude, longitude, time, input_altitude, input_azimuth, plot=True)

            else:
                locate_nearby_stars(latitude,longitude,time, input_altitude, input_azimuth)
        
        elif command == "research":
            hip_id = input("Enter HIP ID: ")
            research_star(hip_id)
    
        elif command == "help":
            print("""
            Available Commands:
            
            "location"          : Generate an interactive map and display geographic coordinates.
            
            "sky"               : Display a list of observable celestial objects (Sun, Moon, planets, and stars) 
                                from a specific location and time. The location is defined by latitude and longitude, 
                                and the time is provided in UTC.

            "locate"            : Locate celestial objects near a specific altitude and azimuth in the sky, based 
                                on a given location (latitude, longitude) and time. The result includes stars 
                                from the Hipparcos catalog, filtered by a visual magnitude limit.

            "research"          : Retrieve detailed astronomical information about a star using its HIP ID. 
                                This command queries the Simbad database for data on the star's spectral type, 
                                distance, magnitude, proper motion, and other key characteristics.

            General Notes:
            - All commands require input in the specified format (e.g., "latitude, longitude" for location-based commands).
            - The "sky" and "locate" commands also require a valid UTC time.
            - The "research" command needs a valid HIP ID from the Hipparcos catalog to function.

            For more detailed usage or additional help, refer to the documentation or contact the developer.
            """)
        else:
            print("Bye")
            break
