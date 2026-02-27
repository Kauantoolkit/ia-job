"""
Script para gerar dados de treino realistas com ruído apropriado
para o modelo de predição de atrasos de entregas.

Melhorias:
- Remoção de seed fixo para mais variabilidade
- Correlações mais complexas entre variáveis
- Mais ruído e incerteza nos dados
- Edge cases e situações extremas
- Sazonalidade e padrões temporais
"""
import csv
import random
import math
from datetime import datetime, timedelta

# Configurações
NUM_TRAIN = 367
NUM_TEST = 92
TOTAL = NUM_TRAIN + NUM_TEST

# Dados base
ROUTES = ["ROTA_001", "ROTA_002", "ROTA_003", "ROTA_004", "ROTA_005"]
VEHICLE_TYPES = ["Van", "Caminhão Baú", "Caminhão Truck", "Caminhão Bitrem"]
TRAFFIC_LEVELS = ["baixo", "medio", "alto"]

# Características ocultas das rotas (não explícitas, mas influenciam)
ROUTE_CHARACTERISTICS = {
    "ROTA_001": {"congestion_prone": 0.7, "weather_sensitive": 0.6, "reliability": 0.75},
    "ROTA_002": {"congestion_prone": 0.3, "weather_sensitive": 0.4, "reliability": 0.90},
    "ROTA_003": {"congestion_prone": 0.6, "weather_sensitive": 0.8, "reliability": 0.65},
    "ROTA_004": {"congestion_prone": 0.4, "weather_sensitive": 0.3, "reliability": 0.85},
    "ROTA_005": {"congestion_prone": 0.5, "weather_sensitive": 0.5, "reliability": 0.80}
}

# Características dos veículos
VEHICLE_CHARACTERISTICS = {
    "Van": {"speed_avg": 1.0, "weather_sensitivity": 0.3, "weight_capacity": 1500},
    "Caminhão Baú": {"speed_avg": 0.85, "weather_sensitivity": 0.5, "weight_capacity": 3000},
    "Caminhão Truck": {"speed_avg": 0.75, "weather_sensitivity": 0.6, "weight_capacity": 8000},
    "Caminhão Bitrem": {"speed_avg": 0.65, "weather_sensitivity": 0.8, "weight_capacity": 25000}
}

def generate_freight_id():
    """Gera um ID único para o frete"""
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    numbers = ''.join(random.choices('0123456789', k=4))
    return f"{letters}-{numbers}"

def generate_correlated_data():
    """
    Gera dados com correlações mais realistas entre variáveis.
    Em vez de escolher cada variável independentemente, cria situações
    que fazem sentido逻辑amente.
    """
    # Primeiro, decidir o contexto geral
    scenario = random.choices(
        ['normal', 'problematic', 'favorable', 'extreme'],
        weights=[0.50, 0.20, 0.20, 0.10]
    )[0]
    
    route = random.choice(ROUTES)
    route_info = ROUTE_CHARACTERISTICS[route]
    
    # Cenários determinam o perfil da viagem
    if scenario == 'problematic':
        # Rota difícil, horário de pico, possível chuva
        traffic = random.choices(TRAFFIC_LEVELS, weights=[0.2, 0.3, 0.5])[0]
        hour = random.choices(
            [random.randint(0, 6), random.randint(7, 9), random.randint(10, 16), random.randint(17, 23)],
            weights=[0.1, 0.35, 0.15, 0.4]
        )[0]
        # Chuva mais provável em cenários problemáticos
        rain = 0.0 if random.random() < 0.4 else round(random.uniform(1, 50), 1)
        vehicle = random.choices(VEHICLE_TYPES, weights=[0.2, 0.3, 0.3, 0.2])[0]
        
    elif scenario == 'favorable':
        # Condições boas, fora do pico
        traffic = random.choices(TRAFFIC_LEVELS, weights=[0.6, 0.3, 0.1])[0]
        hour = random.choices(
            [random.randint(0, 6), random.randint(7, 9), random.randint(10, 16), random.randint(17, 23)],
            weights=[0.25, 0.15, 0.35, 0.25]
        )[0]
        rain = 0.0 if random.random() < 0.75 else round(random.uniform(0.1, 15), 1)
        vehicle = random.choices(VEHICLE_TYPES, weights=[0.35, 0.3, 0.25, 0.1])[0]
        
    elif scenario == 'extreme':
        # Condições extremas - muita chuva OU trânsito muito forte
        if random.random() < 0.5:
            traffic = 'alto'
            rain = 0.0 if random.random() < 0.6 else round(random.uniform(5, 25), 1)
        else:
            traffic = random.choice(TRAFFIC_LEVELS)
            rain = round(random.uniform(25, 60), 1)  # Chuva muito forte
        hour = random.randint(0, 23)
        vehicle = random.choices(VEHICLE_TYPES, weights=[0.15, 0.25, 0.35, 0.25])[0]
        
    else:  # normal
        traffic = random.choice(TRAFFIC_LEVELS)
        hour = random.randint(0, 23)
        # Chuva: distribuição mais realista
        if random.random() < 0.65:
            rain = 0.0
        elif random.random() < 0.88:
            rain = round(random.uniform(0.1, 12), 1)
        else:
            rain = round(random.uniform(12.1, 45), 1)
        vehicle = random.choice(VEHICLE_TYPES)
    
    # Peso da carga: pode ter correlação com tipo de veículo
    vehicle_cap = VEHICLE_CHARACTERISTICS[vehicle]["weight_capacity"]
    if random.random() < 0.6:
        # Carga adequada para o veículo (70-95% da capacidade)
        weight = int(vehicle_cap * random.uniform(0.4, 0.95))
    else:
        # Carga atípica (muito leve ou muito pesada)
        weight = int(vehicle_cap * random.uniform(0.1, 1.1))
    weight = max(500, min(weight, 4200))
    
    # Distância baseada na rota com variação
    base_distance = {"ROTA_001": 85, "ROTA_002": 45, "ROTA_003": 120, "ROTA_004": 55, "ROTA_005": 95}
    distance = base_distance[route] + random.randint(-15, 15)
    distance = max(25, distance)
    
    # Tempo médio histórico com correlação à distância e veículo
    base_time = {"ROTA_001": 120, "ROTA_002": 90, "ROTA_003": 145, "ROTA_004": 85, "ROTA_005": 130}
    vehicle_speed_factor = VEHICLE_CHARACTERISTICS[vehicle]["speed_avg"]
    base_t = base_time[route] * (distance / base_distance[route])
    historical_time = int(base_t / vehicle_speed_factor + random.randint(-20, 20))
    historical_time = max(30, historical_time)
    
    return {
        'route': route,
        'vehicle': vehicle,
        'traffic': traffic,
        'hour': hour,
        'rain': rain,
        'weight': weight,
        'distance': distance,
        'historical_time': historical_time,
        'route_info': route_info,
        'vehicle_info': VEHICLE_CHARACTERISTICS[vehicle]
    }

def calculate_delay_probability_complex(row):
    """
    Calcula a probabilidade de atraso com regras muito mais complexas
    e comMUITO mais ruído para simular incerteza real.
    """
    prob = 0.0
    
    route = row['route']
    vehicle = row['vehicle']
    traffic = row['traffic']
    hour = row['hour']
    rain = row['rain']
    weight = row['weight']
    distance = row['distance']
    route_info = row['route_info']
    vehicle_info = row['vehicle_info']
    
    # === FATOR 1: TRÂNSITO (impacto não-linear) ===
    if traffic == 'alto':
        prob += random.uniform(0.25, 0.50)  # Mais variabilidade
    elif traffic == 'medio':
        prob += random.uniform(0.08, 0.25)
    # baixo: little or no addition
    
    # === FATOR 2: CHUVA (não-linear e com interação) ===
    if rain > 40:
        prob += random.uniform(0.25, 0.55)
    elif rain > 20:
        prob += random.uniform(0.15, 0.35)
    elif rain > 10:
        prob += random.uniform(0.05, 0.20)
    elif rain > 3:
        prob += random.uniform(0.0, 0.10)
    
    # === FATOR 3: HORÁRIO (padrões complexos) ===
    # Pico da manhã
    if 7 <= hour <= 9:
        prob += random.uniform(0.10, 0.30)
    # Pico da tarde
    elif 17 <= hour <= 20:
        prob += random.uniform(0.15, 0.35)
    # Madrugada (baixo trânsito mas menor eficiência)
    elif hour <= 5:
        prob += random.uniform(-0.05, 0.10)
    # Fora de pico
    else:
        prob += random.uniform(-0.05, 0.10)
    
    # === FATOR 4: PESO (relação não-linear) ===
    weight_ratio = weight / vehicle_info['weight_capacity']
    if weight_ratio > 0.9:
        prob += random.uniform(0.10, 0.25)
    elif weight_ratio > 0.7:
        prob += random.uniform(0.0, 0.15)
    elif weight_ratio < 0.3:
        prob += random.uniform(-0.05, 0.10)  # Carga muito leve pode ser problema
    
    # === FATOR 5: DISTÂNCIA ===
    if distance > 150:
        prob += random.uniform(0.15, 0.35)
    elif distance > 100:
        prob += random.uniform(0.05, 0.20)
    elif distance < 40:
        prob += random.uniform(-0.08, 0.05)
    
    # === FATOR 6: CARACTERÍSTICAS OCULTAS DA ROTA ===
    prob += route_info['congestion_prone'] * random.uniform(0.05, 0.15)
    prob += route_info['weather_sensitivity'] * (rain / 50.0) * random.uniform(0.05, 0.15)
    prob += (1 - route_info['reliability']) * random.uniform(0.05, 0.15)
    
    # === FATOR 7: TIPO DE VEÍCULO ===
    prob += vehicle_info['weather_sensitivity'] * (rain / 40.0) * random.uniform(0.05, 0.15)
    
    # === INTERAÇÕES COMPLEXAS (fatores que se multiplicam) ===
    # Chuva + Trânsito alto = problema em dobro
    if rain > 15 and traffic == 'alto':
        prob += random.uniform(0.10, 0.25)
    
    # Hora de pico + Clima ruim
    if hour in [7, 8, 9, 17, 18, 19, 20] and rain > 5:
        prob += random.uniform(0.05, 0.15)
    
    # Veículo grande + Rota congestionada
    if vehicle == "Caminhão Bitrem" and route_info['congestion_prone'] > 0.5:
        prob += random.uniform(0.05, 0.15)
    
    # === RUÍDO SIGNIFICATIVO (40-50% de incerteza) ===
    # Este é o fator que mais adiciona "realismo" e imprevisibilidade
    noise = random.uniform(-0.35, 0.40)
    prob += noise
    
    # === FATORES ALEATÓRIOS EXTRAS (simula eventos inesperados) ===
    # 5% de chance de evento totally aleatório
    if random.random() < 0.05:
        prob += random.choice([-0.30, -0.20, 0.20, 0.30, 0.40])
    
    # === CONDIÇÕES ESPECIAIS RARAS ===
    # Dia de jogo, protestos, acidentes não previstos (2% chance)
    if random.random() < 0.02:
        prob += random.uniform(0.30, 0.60)
    
    # Condição muito favorável (3% chance)
    if random.random() < 0.03:
        prob -= random.uniform(0.15, 0.30)
    
    # Limitar probabilidade a intervalo válido
    prob = max(0.02, min(0.98, prob))
    
    return prob

def generate_row():
    """Gera uma linha de dados realista com correlações complexas"""
    # Gerar dados com correlações
    data = generate_correlated_data()
    
    # Calcular probabilidade de atraso
    prob = calculate_delay_probability_complex(data)
    
    # Decidir se atrasa (com mais randomness)
    # Usamos uma distribuição mais variada para o threshold
    delay_threshold = random.uniform(0.30, 0.70)
    delay_label = "atrasado" if prob > delay_threshold else "em_tempo"
    
    # Criar row final
    row = {
        'freight_description': generate_freight_id(),
        'route_variant_id': data['route'],
        'planned_departure_hour': data['hour'],
        'traffic_level_forecast': data['traffic'],
        'rain_forecast_mm': data['rain'],
        'cargo_weight_kg': data['weight'],
        'vehicle_type': data['vehicle'],
        'historical_avg_route_time_min': data['historical_time'],
        'distance_km': data['distance'],
        'delay_label': delay_label
    }
    
    return row

def generate_dataset():
    """Gera o dataset completo com máxima variabilidade"""
    data = []
    for _ in range(TOTAL):
        data.append(generate_row())
    return data

def save_to_csv(data, filename):
    """Salva os dados em um arquivo CSV"""
    fieldnames = [
        'freight_description',
        'delay_label',
        'route_variant_id',
        'planned_departure_hour',
        'traffic_level_forecast',
        'rain_forecast_mm',
        'cargo_weight_kg',
        'vehicle_type',
        'historical_avg_route_time_min',
        'distance_km'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Arquivo {filename} gerado com {len(data)} registros")

def analyze_data(data):
    """Análise detalhada dos dados gerados"""
    total = len(data)
    delayed = sum(1 for r in data if r['delay_label'] == 'atrasado')
    on_time = sum(1 for r in data if r['delay_label'] == 'em_tempo')
    
    print(f"\n{'='*50}")
    print(f"ANÁLISE DOS DADOS GERADOS")
    print(f"{'='*50}")
    print(f"Total de registros: {total}")
    print(f"Atrasados: {delayed} ({delayed/total*100:.1f}%)")
    print(f"No prazo: {on_time} ({on_time/total*100:.1f}%)")
    
    # Análise por nível de tráfego
    print(f"\n--- Por nível de tráfego ---")
    for traffic in TRAFFIC_LEVELS:
        subset = [r for r in data if r['traffic_level_forecast'] == traffic]
        if subset:
            delayed_count = sum(1 for r in subset if r['delay_label'] == 'atrasado')
            pct = delayed_count/len(subset)*100
            print(f"  {traffic}: {delayed_count}/{len(subset)} ({pct:.1f}%)")
    
    # Análise por chuva
    print(f"\n--- Por precipitação ---")
    no_rain = [r for r in data if r['rain_forecast_mm'] == 0]
    light_rain = [r for r in data if 0 < r['rain_forecast_mm'] <= 10]
    medium_rain = [r for r in data if 10 < r['rain_forecast_mm'] <= 25]
    heavy_rain = [r for r in data if r['rain_forecast_mm'] > 25]
    
    categories = [
        ("Sem chuva", no_rain),
        ("Chuva leve (0-10mm)", light_rain),
        ("Chuva média (10-25mm)", medium_rain),
        ("Chuva forte (>25mm)", heavy_rain)
    ]
    
    for name, group in categories:
        if group:
            delayed = sum(1 for r in group if r['delay_label'] == 'atrasado')
            print(f"  {name}: {delayed}/{len(group)} ({delayed/len(group)*100:.1f}%)")
    
    # Análise por rota
    print(f"\n--- Por rota ---")
    for route in ROUTES:
        subset = [r for r in data if r['route_variant_id'] == route]
        if subset:
            delayed_count = sum(1 for r in subset if r['delay_label'] == 'atrasado')
            pct = delayed_count/len(subset)*100
            print(f"  {route}: {delayed_count}/{len(subset)} ({pct:.1f}%)")
    
    # Análise por horário
    print(f"\n--- Por período do dia ---")
    morning = [r for r in data if 6 <= r['planned_departure_hour'] <= 11]
    afternoon = [r for r in data if 12 <= r['planned_departure_hour'] <= 17]
    evening = [r for r in data if 18 <= r['planned_departure_hour'] <= 22]
    night = [r for r in data if r['planned_departure_hour'] <= 5 or r['planned_departure_hour'] >= 23]
    
    periods = [
        ("Manhã (6-11)", morning),
        ("Tarde (12-17)", afternoon),
        ("Noite (18-22)", evening),
        ("Madrugada (23-5)", night)
    ]
    
    for name, group in periods:
        if group:
            delayed = sum(1 for r in group if r['delay_label'] == 'atrasado')
            print(f"  {name}: {delayed}/{len(group)} ({delayed/len(group)*100:.1f}%)")

# Executar geração
if __name__ == "__main__":
    # NÃO固定 seed - para que cada execução seja diferente
    # Se quiser reprodutibilidade, descomente a linha abaixo:
    # random.seed(42)
    
    print("Gerando dados realistas e não-determinísticos...")
    print("-" * 50)
    
    data = generate_dataset()
    save_to_csv(data, "dados_treino.csv")
    analyze_data(data)
