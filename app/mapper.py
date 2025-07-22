import folium
from folium.plugins import MousePosition
import os
import webbrowser
import platform

def create_map(file_path='map.html'):
    if os.path.exists(file_path):
        print(f"{file_path} already exists. Opening in default browser.")
        try:
            # Attempt to open the map in the default browser
            webbrowser.open(file_path)
        except webbrowser.Error:
            print("No default browser found, opening in Firefox...")
            # Check for Linux platform
            if platform.system() == "Linux":
                firefox_path = "/usr/bin/firefox"
                if os.path.exists(firefox_path):
                    os.system(f"{firefox_path} {file_path}")
                else:
                    print("Firefox is not installed or not found at expected location.")
            else:
                print("Default browser could not be detected on this platform. Please ensure it's properly configured.")
    else:
        # Create a map centered at a specific location
        m = folium.Map(location=[0, 0], zoom_start=2)

        # Add a MousePosition plugin to display coordinates on the map
        formatter = "function(num) {return L.Util.formatNum(num, 5);};"
        MousePosition(
            position='topright',
            separator=' Long: ',
            empty_string='NaN',
            lng_first=False,
            num_digits=20,
            prefix='Lat:',
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(m)

        # Save the map to an HTML file
        m.save(file_path)
        print(f"Map has been created and saved to {file_path}")
        
        try:
            # Attempt to open the map in the default browser
            webbrowser.open(file_path)
        except webbrowser.Error:
            print("No default browser found, opening in Firefox...")
            # Check for Linux platform
            if platform.system() == "Linux":
                firefox_path = "/usr/bin/firefox"
                if os.path.exists(firefox_path):
                    os.system(f"{firefox_path} {file_path}")
                else:
                    print("Firefox is not installed or not found at expected location.")
            else:
                print("Default browser could not be detected on this platform. Please ensure it's properly configured.")
