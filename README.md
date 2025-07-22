# The Astro Comp

**The Astro Comp** is an interactive astronomy tool built in Python that allows users to:

- Create a dynamic map with coordinates.
- Identify observable celestial objects (Sun, Moon, planets, and stars) visible from a given location and time.
- Locate stars near specified celestial coordinates (altitude and azimuth).
- Research detailed information about stars from the Hipparcos catalog.

## Features

- **Map Creation**: Generate and view a map centered on a specific location with coordinate tracking.
- **Sky Observation**: Query and display observable celestial objects (e.g., Sun, Moon, planets, stars) based on geographical location and time.
- **Locate Nearby Stars**: Find stars near a specified altitude and azimuth for a given time and location.
- **Star Research**: Retrieve detailed information about stars (e.g., spectral type, distance, radial velocity) from the Simbad and Hipparcos catalogs.

## Prerequisites

Ensure that the following Python libraries are installed:

- `astropy` for astronomical calculations.
- `folium` for map creation and interactive viewing.
- `astroquery` for querying astronomical catalogs (Simbad and Vizier).
- `webbrowser` for opening maps in your default browser.

You can install the required libraries using `pip`:

```bash
pip install astropy folium astroquery
```

## Usage

```bash
python main.py
```

## Example Use Cases

- Check what planets or stars are visible right now from your location.
- Find stars near the position of a telescope or fixed camera.
- Explore star data for research or educational projects.

## License

This project is licensed under the MIT License

## Contribuiting

Contributions are welcome! Feel free to:
- Fork the repository.
- Submit issues for bugs or ideas.
- Open pull requests to improve features or code.

## Acknowledgements

- Built using Astroquery, Astropy, and Folium.
- Stellar data provided by the Simbad and Hipparcos catalogs.
  




