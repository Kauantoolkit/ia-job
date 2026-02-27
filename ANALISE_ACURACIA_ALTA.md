# Análise: Por que a Acurácia está tão Alta (93%+)?

## 🔴 Problema Principal: DATA LEAKAGE (Vazamento de Dados)

O problema mais grave está nos **dados de treino**, não no código. Existe uma coluna que está "vazando" a resposta para o modelo:

### Coluna Problemática: `historical_delay_rate_route`

Esta coluna contém a **taxa histórica de atraso da rota** - ou seja, ela já sabe a resposta antes do modelo fazer qualquer previsão!

Exemplos do CSV:
```
ROTA_001, traffic_level=alto, rain=25mm → delay_rate=0.65 → atrasado
ROTA_002, traffic_level=baixo, rain=0mm → delay_rate=0.12 → em_tempo  
ROTA_003, traffic_level=alto, rain=18mm → delay_rate=0.72 → atrasado
```

**O modelo simplesmente aprende**: "se `historical_delay_rate_route > 0.5` → atrasado"

Isso explica a acurácia de 93%+. O modelo não está aprendendo padrões complexos - ele está decodificando uma coluna que já contém a resposta!

---

## 📊 Segundo Problema: Dados com Padrões Muito Óbvios

Os dados foram criados com **regras determinísticas simples**:

| Condição | Resultado |
|----------|-----------|
| `traffic_level = alto` E `rain_forecast > 15mm` | `atrasado` |
| `traffic_level = baixo` E `rain_forecast < 5mm` | `em_tempo` |
| `planned_departure_hour` em horários de pico (6-8h, 17-19h) | mais chance de atraso |

Isso torna muito fácil para o RandomForest acertar - ele só precisa aprender "se chuva forte + trânsito alto = atraso".

---

## 🔧 Terceiro Problema: Coluna `freight_description`

A descrição do frete contém padrões que podem estar correlacionados:
- "Frete Expresso" → geralmente mais crítico
- "Frete Normal" → menos crítico
- "Frete Urgente" → alta chance de atraso

O OneHotEncoder cria features separadas para cada descrição, permitindo que o modelo memorize esses padrões.

---

## ✅ Soluções Recomendadas

### Opção 1: Remover a coluna problemática (Recomendado)
```
python
# No arquivo predictor.py, modificar _prepare_features:
exclude_cols = ["freight_description", "delay_label", "historical_delay_rate_route"]
```

### Opção 2: Criar dados mais realistas
Gerar novos dados CSV sem regras tão óbvias, com:
- Mais ruído nos dados
- Correlações menos perfeitas entre features e target
- Casos "limítrofes" que confundam o modelo

### Opção 3: Usar validação cruzada
Adicionar validação cruzada (cross-validation) para verificar se a acurácia se mantém em diferentes folds:
```
python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
```

---

## 📈 O que esperar depois das correções?

Com os dados corrigidos, a acurácia deve cair para algo mais realista:
- **50-70%**: Modelo razoável
- **70-85%**: Modelo bom  
- **85%+**: Suspeito (possível overfitting ou data leakage)

---

## 🔍 Verificação Rápida

Para confirmar que é data leakage, faça este teste:

1. Treine o modelo normalmente
2. Veja as **feature importances** 
3. Se `historical_delay_rate_route` estiver no topo com >50% de importância → confirmado!

O RandomForest vai "colar" nessa feature porque ela é o preditor mais forte disponível.
