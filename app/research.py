from astroquery.simbad import Simbad

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