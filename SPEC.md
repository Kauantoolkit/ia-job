# Especificação do Projeto - Sistema de Previsão de Atraso de Entregas

## 1. Visão Geral do Projeto

**Nome:** Delivery Delay Predictor  
**Tipo:** Aplicação Full Stack (React + FastAPI)  
**Funcionalidade Principal:** Sistema de Machine Learning para prever atrasos em entregas de fretes usando modelo de classificação binária  
**Usuários Alvo:** Gestores de logística e operações de transporte

---

## 2. Especificação de UI/UX

### Estrutura de Páginas

1. **Página Inicial (Dashboard)**
   - Visão geral do sistema
   - Cards de estatísticas rápidas
   - Navegação para outras funcionalidades

2. **Página de Upload e Treino**
   - Área para upload de arquivo CSV
   - Status do modelo atual
   - Botão para treinar/re-treinar modelo
   - Logs de treino em tempo real

3. **Página de Métricas**
   - Accuracy do modelo
   - AUC-ROC
   - Matriz de confusão
   - Feature importance (gráfico)

4. **Página de Predição**
   - Formulário para inserir dados do frete
   - Probabilidade percentual de atraso
   - Barra visual de risco (verde/amarelo/vermelho)

### Design Visual

**Paleta de Cores:**
- Primary: `#1E3A5F` (azul escuro profissional)
- Secondary: `#3B82F6` (azul vibrante)
- Accent: `#10B981` (verde sucesso)
- Warning: `#F59E0B` (amarelo alerta)
- Danger: `#EF4444` (vermelho erro)
- Background: `#0F172A` (dark slate)
- Surface: `#1E293B` (card background)
- Text Primary: `#F8FAFC`
- Text Secondary: `#94A3B8`

**Tipografia:**
- Font Family: 'Inter', sans-serif
- Headings: 700 weight
- Body: 400 weight
- Monospace (logs): 'JetBrains Mono'

**Espaçamento:**
- Base: 4px
- Container padding: 24px
- Card padding: 20px
- Gap entre elementos: 16px

**Efeitos:**
- Border radius: 12px para cards
- Box shadow: `0 4px 6px -1px rgba(0, 0, 0, 0.3)`
- Transições: 200ms ease
- Hover states com brilho sutil

### Componentes

1. **Navigation Bar**
   - Logo e título
   - Links de navegação
   - Estado ativo destacado

2. **Upload Zone**
   - Drag and drop area
   - Indicador de progresso
   - Feedback de sucesso/erro

3. **Metric Card**
   - Ícone, valor grande, label
   - Cor de fundo baseada no valor

4. **Prediction Form**
   - Campos com labels claros
   - Selects dropdown para categóricas
   - Inputs number para numéricas
   - Validação inline

5. **Risk Bar**
   - Barra horizontal graduada
   - Indicador de posição
   - Cores: verde (0-30%), amarelo (31-70%), vermelho (71-100%)

6. **Logs Panel**
   - Área scrollável
   - Timestamps
   - Cores por nível (info, warning, error)

---

## 3. Especificação Funcional

### Backend (FastAPI)

**Arquitetura:**
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── config.py        # Configurações
│   ├── models/
│   │   ├── __init__.py
│   │   └── predictor.py  # Lógica ML
│   ├── services/
│   │   ├── __init__.py
│   │   └── trainer.py    # Treino do modelo
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── api.py       # Endpoints
│   ├── utils/
│   │   ├── __init__.py
│   │   └── validator.py  # Validação CSV
│   └── routes/
│       ├── __init__.py
│       └── ml_routes.py  # Rotas API
├── models/              # Modelos salvos
├── data/                # Dados temporários
├── requirements.txt
└── README.md
```

**Endpoints:**

1. `POST /api/train`
   - Input: Form-data com arquivo CSV
   - Valida colunas obrigatórias
   - Treina modelo RandomForest
   - Salva modelo com versão
   - Retorna métricas e logs

2. `POST /api/predict`
   - Input: JSON com features
   - Retorna probabilidade de atraso

3. `POST /api/retrain`
   - Input: Form-data com novo CSV
   - Incremental ou full retrain
   - Nova versão do modelo

4. `GET /api/metrics`
   - Retorna métricas do modelo atual

5. `GET /api/features/importance`
   - Retorna importância das features

6. `GET /api/model/info`
   - Versão do modelo
   - Data de treino
   - Status

**Lógica ML:**

- Detecção automática de colunas categóricas vs numéricas
- OneHotEncoder para categóricas
- StandardScaler para numéricas
- Pipeline scikit-learn: `Pipeline([('preprocess', ColumnTransformer), ('clf', RandomForestClassifier)])`
- Conversão delay_label: "atrasado" → 1, "em_tempo" → 0
- predict_proba para probabilidade

### Frontend (React)

**Arquitetura:**
```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── UploadZone.jsx
│   │   ├── MetricCard.jsx
│   │   ├── PredictionForm.jsx
│   │   ├── RiskBar.jsx
│   │   └── LogsPanel.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── Train.jsx
│   │   ├── Metrics.jsx
│   │   └── Predict.jsx
│   ├── services/
│   │   └── api.js
│   ├── styles/
│   │   └── App.css
│   ├── App.jsx
│   └── main.jsx
├── package.json
└── vite.config.js
```

### Base de Dados (CSV)

**Colunas Obrigatórias:**
- freight_description (string)
- delay_label (string: "atrasado" ou "em_tempo")
- route_variant_id (string)
- planned_departure_hour (int 0-23)
- traffic_level_forecast (string: "baixo", "medio", "alto")
- rain_forecast_mm (float)
- cargo_weight_kg (float)
- vehicle_type (string)
- historical_avg_route_time_min (float)
- historical_delay_rate_route (float)

---

## 4. Critérios de Aceitação

### Funcionalidade
- [ ] Upload de CSV funciona corretamente
- [ ] Modelo treina com dados válidos
- [ ] Predição retorna probabilidade percentual
- [ ] Barra de risco exibe cores corretas
- [ ] Métricas são calculadas e exibidas
- [ ] Re-treinamento atualiza o modelo
- [ ] Tratamento de erros amigável

### Visual
- [ ] Interface responsiva
- [ ] Cores seguem paleta especificada
- [ ] Animações suaves
- [ ] Logos e ícones apropriados

### Técnica
- [ ] Backend inicia sem erros
- [ ] Frontend compila sem erros
- [ ] API responde corretamente
- [ ] Modelo salvo em arquivo .pkl
- [ ] Logs são exibidos durante treino

---

## 5. Tecnologias

**Backend:**
- Python 3.9+
- FastAPI
- scikit-learn
- pandas
- joblib (serialização)
- uvicorn

**Frontend:**
- React 18
- Vite
- Axios
- React Router DOM

---

## 6. Dados de Exemplo

Para teste, o sistema deve funcionar com CSV no formato:

```
csv
freight_description,delay_label,route_variant_id,planned_departure_hour,traffic_level_forecast,rain_forecast_mm,cargo_weight_kg,vehicle_type,historical_avg_route_time_min,historical_delay_rate_route
Frete Expresso Sul,atrasado,ROTA_001,8,alto,15.5,2500,Caminhão Baú,120,0.35
Frete Normal Centro,em_tempo,ROTA_002,14,baixo,0.0,1800,Vanqua,90,0.12
...
