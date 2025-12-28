def save_data_to_db(vehicle_list, cursor):
    batch_data = []

    for vehicle in vehicle_list:
        number = vehicle['routeShortName']
        delay = vehicle['delay']
        lat = vehicle['lat']
        lon = vehicle['lon']
        veh_id = vehicle.get('vehicleCode', 'Unknown')

        if number and lat and lon:
            batch_data.append( (number, delay, lat, lon, veh_id) )
    if batch_data:
        query = """
            INSERT INTO bus_positions 
            (line_number, delay_seconds, latitude, longitude, vehicle_id) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(query, batch_data)