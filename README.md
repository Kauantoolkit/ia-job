# Delivery Delay Predictor

Sistema de previsão de atraso de entregas usando Machine Learning (RandomForest).

## Funcionalidades

- Upload de CSV com dados históricos de fretes
- Treinamento de modelo de classificação binária
- Predição de probabilidade de atraso
- Visualização de métricas (Accuracy, AUC-ROC)
- Feature Importance
- Interface moderna e responsiva

## Tech Stack

**Backend:**
- FastAPI (Python)
- scikit-learn (RandomForest)
- pandas
- joblib

**Frontend:**
- React 18
- Vite
- React Router
- Axios

## Estrutura do Projeto

```
delivery-delay-predictor/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   └── predictor.py
│   │   ├── controllers/
│   │   │   └── api.py
│   │   └── utils/
│   │       └── validator.py
│   ├── data/
│   │   └── dados_treino.csv
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── styles/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Como Executar

### Backend

1. Navegue para o diretório backend:
```
bash
cd backend
```

2. Crie um ambiente virtual (opcional):
```
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```
bash
pip install -r requirements.txt
```

4. Inicie o servidor:
```
bash
python -m app.main
```

O backend estará disponível em: http://localhost:8000

### Frontend

1. Navegue para o diretório frontend:
```
bash
cd frontend
```

2. Instale as dependências:
```
bash
npm install
```

3. Inicie o servidor de desenvolvimento:
```
bash
npm run dev
```

O frontend estará disponível em: http://localhost:3000

## Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/health` | Verificação de saúde |
| GET | `/api/model/info` | Informações do modelo |
| POST | `/api/train` | Treinar modelo |
| POST | `/api/retrain` | Re-treinar modelo |
| POST | `/api/predict` | Fazer predição |
| GET | `/api/metrics` | Obter métricas |
| GET | `/api/features/importance` | Feature importance |

## Formato do CSV

O arquivo CSV deve conter as seguintes colunas:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| freight_description | string | Descrição do frete |
| delay_label | string | "atrasado" ou "em_tempo" |
| route_variant_id | string | ID da rota |
| planned_departure_hour | int | Hora de partida (0-23) |
| traffic_level_forecast | string | "baixo", "medio" ou "alto" |
| rain_forecast_mm | float | Previsão de chuva (mm) |
| cargo_weight_kg | float | Peso da carga (kg) |
| vehicle_type | string | Tipo de veículo |
| historical_avg_route_time_min | float | Tempo médio histórico (min) |
| historical_delay_rate_route | float | Taxa histórica de atraso |

## Uso

1. **Acesse o frontend** em http://localhost:3000
2. **Vá para "Treinar Modelo"** e faça upload do arquivo CSV com dados históricos
3. **Clique em "Iniciar Treinamento"** e aguarde a conclusão
4. **Visualize as métricas** na página "Métricas"
5. **Faça predições** na página "Prever Atraso"

## Exemplo de Predição

```
json
{
  "route_variant_id": "ROTA_001",
  "planned_departure_hour": 8,
  "traffic_level_forecast": "alto",
  "rain_forecast_mm": 15.5,
  "cargo_weight_kg": 2500,
  "vehicle_type": "Caminhão Baú",
  "historical_avg_route_time_min": 120,
  "historical_delay_rate_route": 0.35
}
```

Resposta:
```
json
{
  "probability": 0.72,
  "probability_percent": 72.0,
  "risk_level": "alto",
  "risk_color": "red",
  "prediction": "atrasado"
}
```

## Licença

MIT
