def save_data_to_db(vehicle_list, cursor):
    for vehicle in vehicle_list:
        if vehicle['routeShortName'] in ['199', '168']:
            number = vehicle['routeShortName']
            delay = vehicle['delay']
            lat = vehicle['lat']
            lon = vehicle['lon']
            veh_id = vehicle.get('vehicleCode', 'Unknown')

            print(f"Saving: Lane {number} ({veh_id}), delay: {delay}")

            cursor.execute(
                """INSERT INTO bus_positions 
                   (line_number, delay_seconds, latitude, longitude, vehicle_id) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (number, delay, lat, lon, veh_id)
            )