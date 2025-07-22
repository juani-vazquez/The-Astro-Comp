from astropy.coordinates import EarthLocation, AltAz, get_sun, get_body, SkyCoord
from astropy.time import Time
import astropy.units as u
from astroquery.vizier import Vizier
import matplotlib.pyplot as plt

def on_key(event):
    if event.key == 'escape':
        plt.close()

def locate_nearby_stars(latitude, longitude, time, input_altitude, input_azimuth, magnitude_limit=5, plot=False):
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

    if plot:
        plt.figure(figsize=(10,6))
        
        top_5_stars = nearest_stars[:5]

        top_5_az = [star[2] for star in top_5_stars]
        top_5_alt = [star[1] for star in top_5_stars]
        top_5_labels = [star[0] for star in top_5_stars]

        plt.scatter(top_5_az,top_5_alt,c="red", label="Nearest Stars", s=100, marker="*", edgecolor="black")

        for az, alt, label in zip(top_5_az,top_5_alt,top_5_labels):
            plt.text(az, alt, f"HIP {label}", fontsize=9, ha="left", color="black")

        plt.title("Nearby Stars in Alt-Az coordinates")
        plt.xlabel("Azimuth degrees")
        plt.ylabel("Altitude degrees")
        plt.legend()
        plt.grid(True)
        plt.gcf().canvas.mpl_connect('key_press_event', on_key)

        plt.show()

    return nearest_stars