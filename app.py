from flask import Flask, render_template, request, send_from_directory
import os
import numpy as np
import matplotlib.pyplot as plt

# Configuração da aplicação Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/graphs'

# Certifique-se de que o diretório para salvar gráficos existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Constantes
k = 1.38e-23
q = 1.602e-19
n = 1.4
Isr = 1.2799e-8
Vg = 1.79e-19
Tc = 298.15
G_ref = 1000
T_var = [298.15, 308.15, 318.15, 328.15, 338.15]
G_var = [400, 600, 800, 1000, 1200]
G = 800

def corrente_fotovoltaica(V, Icc, Kt, G, G_ref, T, Tc):
    Iph = ((Icc / G_ref) * G) * (1 + Kt * (T - Tc))
    Is = Isr * (T / Tc) ** (3 / n) * np.exp((-(q * Vg) / (n * k)) * ((1 / T) - (1 / Tc)))
    I = Iph - Is * np.exp(((q * V) / (n * k * T)) - 1)
    return I

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_graphs', methods=['POST'])
def generate_graphs():
    Icc = float(request.form['icc'])
    Kt = float(request.form['kt'])
    V_values = np.linspace(0, 1.2, 100)

    # Lista para armazenar os caminhos dos gráficos gerados
    graph_paths = []

    # I-V variando a temperatura
    plt.figure()
    for Temp in T_var:
        I_values = [corrente_fotovoltaica(V, Icc, Kt, G, G_ref, Temp, Tc) for V in V_values]
        plt.plot(V_values, I_values, label=f'T = {Temp-273.15:.0f} °C')
    plt.title("Curvas I-V variando a temperatura")
    plt.xlabel("Tensão (V)")
    plt.ylabel("Corrente (A)")
    plt.legend()
    plt.grid(True)
    plt.xlim([0, 1.2])
    iv_temp_path = os.path.join(app.config['UPLOAD_FOLDER'], "iv_temp_graph.png")
    plt.savefig(iv_temp_path)
    graph_paths.append(iv_temp_path)
    plt.close()

    # P-V variando a temperatura
    plt.figure()
    for Temp in T_var:
        I_values = [corrente_fotovoltaica(V, Icc, Kt, G, G_ref, Temp, Tc) for V in V_values]
        P_values = V_values * I_values
        plt.plot(V_values, P_values, label=f'T = {Temp-273.15:.0f} °C')
    plt.title("Curvas P-V variando a temperatura")
    plt.xlabel("Tensão (V)")
    plt.ylabel("Potência (W)")
    plt.legend()
    plt.grid(True)
    plt.xlim([0, 1.2])
    pv_temp_path = os.path.join(app.config['UPLOAD_FOLDER'], "pv_temp_graph.png")
    plt.savefig(pv_temp_path)
    graph_paths.append(pv_temp_path)
    plt.close()

    # I-V variando a irradiação
    plt.figure()
    for Irra in G_var:
        I_values = [corrente_fotovoltaica(V, Icc, Kt, Irra, G_ref, Tc, Tc) for V in V_values]
        plt.plot(V_values, I_values, label=f'G = {Irra:.0f} W/m²')
    plt.title("Curvas I-V variando a irradiação")
    plt.xlabel("Tensão (V)")
    plt.ylabel("Corrente (A)")
    plt.legend()
    plt.grid(True)
    plt.xlim([0, 1.2])
    iv_irra_path = os.path.join(app.config['UPLOAD_FOLDER'], "iv_irra_graph.png")
    plt.savefig(iv_irra_path)
    graph_paths.append(iv_irra_path)
    plt.close()

    # P-V variando a irradiação
    plt.figure()
    for Irra in G_var:
        I_values = [corrente_fotovoltaica(V, Icc, Kt, Irra, G_ref, Tc, Tc) for V in V_values]
        P_values = V_values * I_values
        plt.plot(V_values, P_values, label=f'G = {Irra:.0f} W/m²')
    plt.title("Curvas P-V variando a irradiação")
    plt.xlabel("Tensão (V)")
    plt.ylabel("Potência (W)")
    plt.legend()
    plt.grid(True)
    plt.xlim([0, 1.2])
    pv_irra_path = os.path.join(app.config['UPLOAD_FOLDER'], "pv_irra_graph.png")
    plt.savefig(pv_irra_path)
    graph_paths.append(pv_irra_path)
    plt.close()

    return render_template('index.html', graph_paths=graph_paths)

@app.route('/static/graphs/<filename>')
def send_graph(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
