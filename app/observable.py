from astropy.coordinates import EarthLocation, AltAz, get_sun, get_body, SkyCoord
from astropy.time import Time
import astropy.units as u
from astroquery.vizier import Vizier

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