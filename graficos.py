from flask import Flask, send_from_directory
import matplotlib.pyplot as plt
import uuid
import os

app = Flask(__name__)
IMAGES_DIR = "temp_graficos"
os.makedirs(IMAGES_DIR, exist_ok=True)


@app.route("/generar-grafico")
def generar_grafico():
    """Genera un gráfico de ejemplo y devuelve la URL"""
    # 1. Crear gráfico simple
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.title("Gráfico de ejemplo")

    # 2. Guardar en archivo único
    nombre_archivo = f"{uuid.uuid4()}.png"
    ruta_archivo = os.path.join(IMAGES_DIR, nombre_archivo)
    plt.savefig(ruta_archivo)
    plt.close()

    return {"url": f"http://localhost:5000/graficos/{nombre_archivo}", "instruccion": "Abre esta URL en tu navegador"}


@app.route("/graficos/<filename>")
def servir_grafico(filename):
    """Sirve los gráficos guardados"""
    return send_from_directory(IMAGES_DIR, filename)


if __name__ == "__main__":
    print("\nServidor de gráficos listo!")
    print("Accede a http://localhost:5000/generar-grafico")
    print("Presiona Ctrl+C para detener\n")
    app.run(host="0.0.0.0", port=5000)
