import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_sample_data(filename="data/sensor_data.csv", num_samples=96):
    """Generate sample sensor data with some anomalies."""
    # Create directory if not exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Generate timestamps (15-minute intervals for 24 hours)
    start_time = datetime(2025, 1, 1)
    timestamps = [start_time + timedelta(minutes=15 * i) for i in range(num_samples)]

    # Generate normal data
    temperature = [22.0 + np.random.normal(0, 0.3) for _ in range(num_samples)]
    humidity = [45.0 + np.random.normal(0, 0.5) for _ in range(num_samples)]
    pressure = [1013.0 + np.random.normal(0, 0.2) for _ in range(num_samples)]

    # Insert anomalies (around noon)
    noon_index = 48  # noon in a 15-minute interval dataset
    for i in range(noon_index - 2, noon_index + 3):
        if i < len(temperature):
            temperature[i] = 35.0 + np.random.normal(0, 1.0)  # Anomalous high temperature

    # Create dataframe
    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "sensor_id": ["S001"] * num_samples,
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
        }
    )

    # Save to CSV
    df.to_csv(filename, index=False)
    return df


def load_sensor_data(filename="data/sensor_data.csv"):
    """Load sensor data from CSV file."""
    return pd.read_csv(filename)


def format_report(results):
    """Format detection results into a readable report."""
    anomaly_count = sum(results["is_anomaly"])

    report = f"""
    Anomaly Detection Report
    ========================
    Total samples analyzed: {len(results)}
    Anomalies detected: {anomaly_count}
    
    Anomaly Details:
    """

    if anomaly_count > 0:
        anomalies = results[results["is_anomaly"]]
        for idx, row in anomalies.iterrows():
            report += f"""
    - Timestamp: {row['timestamp']}
      Sensor: {row['sensor_id']}
      Temperature: {row['temperature']}°C
      Deviation: {row['anomaly_score']:.2f}
            """
    else:
        report += "\n    No anomalies detected in the data."

    return report


# List of available correction commands
correction_commands = [
    "reset_hvac_system",
    "recalibrate_sensor",
    "activate_backup_cooling",
    "notify_maintenance_team",
    "adjust_temperature_threshold",
]


# Command execution simulation
def execute_command(command):
    """Simulate executing a correction command."""
    if command not in correction_commands:
        return f"Error: Unknown command '{command}'"

    results = {
        "reset_hvac_system": "HVAC system has been reset. System restarting...",
        "recalibrate_sensor": "Sensor recalibration initiated. This will take 5 minutes to complete.",
        "activate_backup_cooling": "Backup cooling system activated. Temperature should normalize in 10-15 minutes.",
        "notify_maintenance_team": "Maintenance team has been notified. Ticket #MT-2025-0124 created.",
        "adjust_temperature_threshold": "Temperature threshold adjusted from 30.0°C to 32.0°C.",
    }

    return results[command]


if __name__ == "__main__":
    # Generate sample data when run as script
    generate_sample_data()
    print("Sample data generated successfully!")
