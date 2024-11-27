import folium
from folium.plugins import MousePosition
from astropy.coordinates import EarthLocation, AltAz, get_sun, get_body, SkyCoord
from astropy.time import Time
import astropy.units as u
from datetime import datetime
import os
import webbrowser
from astroquery.vizier import Vizier
from astroquery.simbad import Simbad

def get_observable_objects(latitude, longitude, time, magnitude_limit=5):
    # Define observer location
    location = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg)

    # Define time
    now = Time(time)

    # Define AltAz frame
    altaz_frame = AltAz(obstime=now, location=location)

    # Get Sun and Moon positions
    sun = get_sun(now).transform_to(altaz_frame)
    moon = get_body("moon", now, location).transform_to(altaz_frame)

    # Define observable objects
    objects = {
        "Sun": sun,
        "Moon": moon
    }

    # Define planets
    planets = ["mercury", "venus", "mars", "jupiter", "saturn"]

    # Compute positions of planets
    for planet in planets:
        body = get_body(planet, now, location).transform_to(altaz_frame)
        objects[planet.capitalize()] = body

    # Query the Hipparcos catalog for stars with Vmag < magnitude_limit
    v = Vizier(columns=['HIP', 'RAICRS', 'DEICRS', 'Vmag'], column_filters={"Vmag": f"<{magnitude_limit}"})
    result = v.query_constraints(catalog='I/239/hip_main')

    # Extract the data
    stars = result[0]
    star_coords = SkyCoord(ra=stars['RAICRS'].data*u.deg, dec=stars['DEICRS'].data*u.deg, frame='icrs')

    # Transform to AltAz frame
    star_altaz = star_coords.transform_to(altaz_frame)

    # Filter stars above the horizon and add to observable objects
    for star, altaz in zip(stars, star_altaz):
        if altaz.alt > 0*u.deg:
            objects[f"Star HIP {star['HIP']}"] = altaz

    # Filter objects above the horizon
    observable = {name: obj for name, obj in objects.items() if obj.alt > 0*u.deg}

    # Display results
    print(f"Observable objects from {location} at {now.iso} UTC:")
    for name, obj in observable.items():
        print(f"  {name}: Altitude {obj.alt:.2f}, Azimuth {obj.az:.2f}")

    return observable

def locate_nearby_stars(latitude, longitude, time, input_altitude, input_azimuth, magnitude_limit=5):
    # Define observer location
    location = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg)

    # Define time
    now = Time(time)

    # Define AltAz frame
    altaz_frame = AltAz(obstime=now, location=location)

    # Query the Hipparcos catalog for stars with Vmag < magnitude_limit
    v = Vizier(columns=['HIP', 'RAICRS', 'DEICRS', 'Vmag'], column_filters={"Vmag": f"<{magnitude_limit}"})
    result = v.query_constraints(catalog='I/239/hip_main')

    # Extract the data
    stars = result[0]
    star_coords = SkyCoord(ra=stars['RAICRS'].data*u.deg, dec=stars['DEICRS'].data*u.deg, frame='icrs')

    # Transform to AltAz frame
    star_altaz = star_coords.transform_to(altaz_frame)

    # Find the nearest stars to the input altitude and azimuth
    input_coord = SkyCoord(alt=input_altitude*u.deg, az=input_azimuth*u.deg, frame=altaz_frame)
    
    nearest_stars = []
    
    for star, altaz in zip(stars, star_altaz):
        separation = input_coord.separation(altaz)
        nearest_stars.append((star['HIP'], altaz.alt.deg, altaz.az.deg, star['Vmag'], separation))
    
    nearest_stars.sort(key=lambda x: x[4])  # Sort by separation

    # Display the nearest stars (limit to 5 for brevity)
    print(f"Nearest stars to Altitude {input_altitude}°, Azimuth {input_azimuth}°:")
    
    for hip_id, alt, az, vmag, sep in nearest_stars[:5]:
        print(f"  Star HIP {hip_id}: Altitude={alt:.2f}°, Azimuth={az:.2f}°, Vmag={vmag}, Separation={sep:.2f}")

def create_map(file_path='map.html'):
    if os.path.exists(file_path):
        print(f"{file_path} already exists. Opening in default browser.")
        webbrowser.open(file_path)
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
        webbrowser.open(file_path)

def research_star(hip_id):
    # Query Simbad for detailed information about the star
    custom_simbad = Simbad()
    custom_simbad.add_votable_fields('sptype', 'distance', 'flux(V)', 'flux(B)', 'flux(R)', 'flux(I)', 'flux(J)', 'flux(H)', 'flux(K)', 'pmra', 'pmdec', 'plx', 'rv_value', 'rot', 'biblio', 'ids', 'otypes')

    result = custom_simbad.query_object(f"HIP {hip_id}")

    if result is None:
        print(f"No information found for HIP {hip_id}")
        return

    star_info = result[0]
    
    print(f"Information for HIP {hip_id}:")
    
    try:
        print(f"  Spectral Type: {star_info['SP_TYPE']}")
    except KeyError:
        print("  Spectral Type: Not available")
    
    try:
        print(f"  Distance: {star_info['Distance_distance']} pc")
    except KeyError:
        print("  Distance: Not available")
    
    try:
        print(f"  Visual Magnitude (V): {star_info['FLUX_V']}")
    except KeyError:
        print("  Visual Magnitude (V): Not available")
    
    try:
        print(f"  Color Index (B-V): {star_info['FLUX_B'] - star_info['FLUX_V']}")
    except KeyError:
        print("  Color Index (B-V): Not available")
    
    try:
        print(f"  Proper Motion (RA): {star_info['PMRA']} mas/yr")
    except KeyError:
        print("  Proper Motion (RA): Not available")
    
    try:
        print(f"  Proper Motion (Dec): {star_info['PMDEC']} mas/yr")
    except KeyError:
        print("  Proper Motion (Dec): Not available")
    
    try:
        print(f"  Parallax: {star_info['PLX_VALUE']} mas")
    except KeyError:
        print("  Parallax: Not available")
    
    try:
        print(f"  Radial Velocity: {star_info['RV_VALUE']} km/s")
    except KeyError:
        print("  Radial Velocity: Not available")
    
    try:
        print(f"  Rotation: {star_info['ROT']} km/s")
    except KeyError:
        print("  Rotation: Not available")
    
    try:
        print(f"  Object Types: {star_info['OTYPES']}")
    except KeyError:
        print("  Object Types: Not available")
    
    try:
        print(f"  Other IDs: {star_info['IDS']}")
    except KeyError:
        print("  Other IDs: Not available")

intro = """

 .    '                   .  "   '
            .  .  .                 '      '
    "`       .   .
                                     '     '
  .    '      _______________
          ==c(___(o(______(_()
                  \=\\
                   )=\\
                   //|\\
                  //|| \\
                 // ||  \\
                //  ||   \\
               //         \\
 _____ _               _        _                ____                      
|_   _| |__   ___     / \   ___| |_ _ __ ___    / ___|___  _ __ ___  _ __  
  | | | '_ \ / _ \   / _ \ / __| __| '__/ _ \  | |   / _ \| '_ ` _ \| '_ \ 
  | | | | | |  __/  / ___ \\__ \ |_| | | (_) | | |__| (_) | | | | | | |_) |
  |_| |_| |_|\___| /_/   \_\___/\__|_|  \___/   \____\___/|_| |_| |_| .__/ 
                                                                    |_|    
"""

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
        latitude = float(input("Enter latitude: "))
        longitude = float(input("Enter longitude: "))
        time_str = input("Enter time (YYYY-MM-DD HH:MM:SS): ")
        time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        
        input_altitude = float(input("Enter altitude (degrees): "))
        input_azimuth = float(input("Enter azimuth (degrees): "))
        
        locate_nearby_stars(latitude, longitude, time, input_altitude, input_azimuth)
    
    elif command == "research":
        hip_id = input("Enter HIP ID: ")
        research_star(hip_id)
    
    else:
        print("Bye")
        break