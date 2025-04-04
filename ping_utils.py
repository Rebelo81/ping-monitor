import subprocess
import datetime
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

def criar_pasta_resultados():
    pasta = "resultados_ping"
    os.makedirs(pasta, exist_ok=True)
    return pasta

def testar_ping(destino, pacotes=4):
    try:
        resultado = subprocess.run(
            ["ping", "-c", str(pacotes), destino],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        output = resultado.stdout
        if "min/avg/max" in output:
            rtt = output.strip().split("\n")[-1]
            rtt_info = rtt.split("=")[1].strip().split(" ")[0]
            min_rtt, avg_rtt, max_rtt, _ = map(float, rtt_info.split("/"))

            perda = [l for l in output.split("\n") if "packet loss" in l][0]
            perda_percentual = perda.split(",")[2].strip().replace("% packet loss", "")
            perda_float = float(perda_percentual.replace("%", ""))

            return {
                "destino": destino,
                "min": min_rtt,
                "avg": avg_rtt,
                "max": max_rtt,
                "perda": perda_float
            }
        else:
            return None

    except subprocess.TimeoutExpired:
        return None

def salvar_em_csv_e_excel(dados, pasta, data_hora):
    csv_path = os.path.join(pasta, f"resumo_{data_hora}.csv")
    excel_path = csv_path.replace(".csv", ".xlsx")

    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Destino", "DataHora", "Min", "Média", "Max", "Perda (%)"])
        for dado in dados:
            writer.writerow([dado["destino"], data_hora, dado["min"], dado["avg"], dado["max"], dado["perda"]])

    df = pd.read_csv(csv_path)
    df.to_excel(excel_path, index=False)
    return csv_path, excel_path

def gerar_grafico(dados, pasta, data_hora):
    destinos = [d["destino"] for d in dados]
    medias = [d["avg"] for d in dados]

    plt.figure(figsize=(8, 5))
    plt.bar(destinos, medias)
    plt.title("Tempo médio de resposta (ms)")
    plt.ylabel("ms")
    plt.xlabel("Destino")
    plt.tight_layout()
    caminho = os.path.join(pasta, f"grafico_{data_hora}.png")
    plt.savefig(caminho)
    plt.close()
    return caminho
