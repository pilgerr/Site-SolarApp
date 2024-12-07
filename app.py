@app.route('/generate_graphs', methods=['POST'])
def generate_graphs():
    Icc = float(request.form['icc'])
    Kt = float(request.form['kt'])
    V_values = np.linspace(0, 1.2, 100)  # Aumentei o intervalo para 1.2

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
    plt.xlim([0, 1.2])  # Garante que o gráfico vai até 1.2 no eixo X
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
    plt.xlim([0, 1.2])  # Garante que o gráfico vai até 1.2 no eixo X
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
    plt.xlim([0, 1.2])  # Garante que o gráfico vai até 1.2 no eixo X
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
    plt.xlim([0, 1.2])  # Garante que o gráfico vai até 1.2 no eixo X
    pv_irra_path = os.path.join(app.config['UPLOAD_FOLDER'], "pv_irra_graph.png")
    plt.savefig(pv_irra_path)
    graph_paths.append(pv_irra_path)
    plt.close()

    return render_template('index.html', graph_paths=graph_paths)
