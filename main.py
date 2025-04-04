from datetime import datetime
from ping_utils import criar_pasta_resultados, testar_ping, salvar_em_csv_e_excel, gerar_grafico

# Lista de destinos
destinos = ["google.com", "cloudflare.com", "github.com", "8.8.8.8"]
pacotes = 4

# Preparar estrutura
pasta = criar_pasta_resultados()
data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
resultados = []

print(f"📡 Testes iniciados em {data_hora}")
print("-" * 50)

# Rodar pings
for destino in destinos:
    print(f"🔍 Testando: {destino}")
    resultado = testar_ping(destino, pacotes)
    if resultado:
        resultados.append(resultado)
        print(f"✅ Média: {resultado['avg']} ms, Perda: {resultado['perda']}%")
    else:
        print(f"❌ Falha ao testar {destino}")

print("-" * 50)

# Salvar e mostrar paths
csv, excel = salvar_em_csv_e_excel(resultados, pasta, data_hora)
grafico = gerar_grafico(resultados, pasta, data_hora)

print(f"📁 Resultados salvos em:\n  CSV: {csv}\n  Excel: {excel}\n  Gráfico: {grafico}")
print("✅ Todos os testes finalizados!")
