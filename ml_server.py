import os
import uuid
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

from sklearn.ensemble import IsolationForest
from mcp.server.fastmcp import FastMCP
from utils import load_sensor_data, format_report, correction_commands, execute_command

# Initialize FastMCP server
mcp = FastMCP("anomaly-detection")

# Global variables to store detection results and visualizations
current_results = None
current_visualization = None


@mcp.tool()
async def fetch_sensor_data(sensor_id: str = "S001") -> str:
    """Fetch sensor data from database.

    Args:
        sensor_id: ID of the sensor to fetch data for
    """
    try:
        df = load_sensor_data()
        sensor_data = df[df["sensor_id"] == sensor_id]
        if sensor_data.empty:
            return f"No data found for sensor {sensor_id}"

        return f"Successfully fetched {len(sensor_data)} records for sensor {sensor_id}"
    except Exception as e:
        return f"Error fetching sensor data: {str(e)}"


@mcp.tool()
async def detect_anomalies(sensor_id: str = "S001", parameter: str = "temperature") -> str:
    """Detect anomalies in sensor data using Isolation Forest algorithm.

    Args:
        sensor_id: ID of the sensor to analyze
        parameter: Parameter to analyze (temperature, humidity, pressure)
    """
    global current_results

    try:
        # Load data
        df = load_sensor_data()
        sensor_data = df[df["sensor_id"] == sensor_id].copy()

        if sensor_data.empty:
            return f"No data found for sensor {sensor_id}"

        if parameter not in sensor_data.columns:
            return f"Parameter '{parameter}' not found in sensor data"

        # Extract features for anomaly detection
        X = sensor_data[[parameter]].values

        # Apply Isolation Forest
        model = IsolationForest(contamination=0.05, random_state=42)
        sensor_data["anomaly_score"] = model.fit_predict(X)
        sensor_data["is_anomaly"] = sensor_data["anomaly_score"] == -1

        # Store results for visualization and reporting
        current_results = sensor_data

        # Format report
        report = format_report(sensor_data)
        return report

    except Exception as e:
        return f"Error detecting anomalies: {str(e)}"


@mcp.tool()
async def visualize_anomalies() -> str:
    """Generate a visualization of detected anomalies and return a viewable URL."""
    global current_results

    if current_results is None:
        return "No anomaly detection results available. Run detect_anomalies first."

    try:
        # Create figure
        plt.figure(figsize=(10, 6))

        # Plot normal data points
        normal = current_results[~current_results["is_anomaly"]]
        plt.scatter(pd.to_datetime(normal["timestamp"]), normal["temperature"], color="blue", label="Normal")

        # Plot anomalies
        anomalies = current_results[current_results["is_anomaly"]]
        plt.scatter(
            pd.to_datetime(anomalies["timestamp"]), anomalies["temperature"], color="red", s=100, label="Anomaly"
        )

        plt.title("Temperature Anomaly Detection")
        plt.xlabel("Time")
        plt.ylabel("Temperature (°C)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Guardar en archivo
        filename = f"anomalies_{uuid.uuid4()}.png"
        filepath = os.path.join("temp_graficos", filename)
        plt.savefig(filepath)
        plt.close()

        return f"Gráfico de anomalías generado: [Haz clic para ver](http://localhost:5000/graficos/{filename})"

    except Exception as e:
        return f"Error: {str(e)}. ¿Está ejecutándose el servidor de gráficos?"


@mcp.tool()
async def get_available_commands() -> str:
    """Get the list of available correction commands."""
    return "Available commands:\n" + "\n".join([f"- {cmd}" for cmd in correction_commands])


@mcp.tool()
async def execute_correction(command: str) -> str:
    """Execute a correction command to address detected anomalies.

    Args:
        command: The correction command to execute
    """
    if command not in correction_commands:
        return f"Error: Unknown command '{command}'. Use get_available_commands to see available options."

    result = execute_command(command)
    return f"Command executed: {command}\nResult: {result}"


if __name__ == "__main__":
    import asyncio

    async def test_functions():
        """Función auxiliar async para probar las herramientas."""
        print("\n=== INICIANDO PRUEBAS ===")
        print("1. Fetch sensor data:", await fetch_sensor_data("S001"))
        print("2. Detect anomalies:", await detect_anomalies("S001", "temperature"))
        print("3. Visualization:", await visualize_anomalies())
        print("=== PRUEBAS COMPLETADAS ===")

    # Ejecuta las pruebas antes de iniciar el servidor
    asyncio.run(test_functions())

    # Inicia el servidor MCP
    print("\nServidor MCP iniciado...")
    mcp.run(transport="stdio")
