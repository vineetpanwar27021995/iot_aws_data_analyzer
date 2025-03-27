from pymongo import MongoClient
import time
import matplotlib.pyplot as plt

# --- MongoDB Setup ---
client = MongoClient("mongodb://localhost:27017/")
db = client["sensor_data"]
collection = db["readings"]

# --- Function: Show latest data for a station (Part B) ---
def show_latest(station_id):
    doc = collection.find({"station_id": station_id}).sort("timestamp", -1).limit(1)
    latest = next(doc, None)
    if not latest:
        print(f"No data found for station '{station_id}'")
        return

    print(f"\nLatest sensor values from {station_id}:")
    print(f"Temperature: {latest['temperature']}°C")
    print(f"Humidity: {latest['humidity']}%")
    print(f"CO2: {latest['co2']} ppm")

    # --- Bar Chart ---
    plt.figure(figsize=(6, 4))
    plt.bar(["Temperature", "Humidity", "CO2"],
            [latest["temperature"], latest["humidity"], latest["co2"]])
    plt.title(f"Latest Readings from {station_id}")
    plt.ylabel("Sensor Value")
    plt.savefig("latest_readings.png")
    plt.tight_layout()
    plt.show()

# --- Function: Show 5-hour history of a sensor (Part C) ---
def show_history(sensor):
    now = time.time()
    cursor = collection.find({
        "timestamp": { "$gte": now - 18000 },
        sensor: { "$exists": True }
    }).sort("timestamp", 1)

    times = []
    values = []

    for doc in cursor:
        times.append(time.strftime('%H:%M:%S', time.localtime(doc["timestamp"])))
        values.append(doc[sensor])

    if not values:
        print(f"No {sensor} data found from the last 5 hours.")
        return

    # Plot full data but limit x-axis ticks
    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker='o')
    plt.title(f"{sensor.capitalize()} Readings (Last 5 Hours)")
    plt.xlabel("Time")
    plt.ylabel(sensor.capitalize())

    # Limit number of x-axis ticks for readability
    max_ticks = 10
    step = max(1, len(times) // max_ticks)
    plt.xticks(times[::step], rotation=45)

    plt.tight_layout()
    plt.savefig(f"{sensor}_history.png")
    plt.show()

# --- CLI Menu ---
while True:
    cmd = input("\nType 'latest <station_id>' or 'history <sensor>' or 'exit': ").strip()

    if cmd.startswith("latest"):
        try:
            _, sid = cmd.split()
            show_latest(sid)
        except:
            print("Usage: latest <station_id>")

    elif cmd.startswith("history"):
        try:
            _, sensor = cmd.split()
            show_history(sensor)
        except:
            print("Usage: history <sensor>")

    elif cmd == "exit":
        break

    else:
        print("Invalid command. Try again.")
