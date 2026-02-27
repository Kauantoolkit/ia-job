# Análise da Matriz de Confusão

## Problema Identificado

### O que estava acontecendo:
Você enviou um dataset com **80 unidades** (linhas de dados), mas a matriz de confusão estava mostrando aproximadamente **18 valores** (soma de TP + TN + FP + FN).

### Por que isso acontece:

1. **Divisão Treino/Teste (Train/Test Split)**
   - O modelo usa `test_size=0.2` (20%) por padrão
   - Com 80 amostras: 80 × 0.2 = **16 amostras para teste**
   - **64 amostras para treino**

2. **A matriz de confusão mostra apenas os resultados do conjunto de TESTE**, não do dataset completo!

3. **Stratified Split** - A divisão é estratificada para manter a proporção de classes:
   - Se o dataset tem ~50% atrasado e ~50% em_tempo
   - O test set terá aproximadamente a mesma proporção

### Por que aparecem ~18 ao invés de 16:

O número exato pode variar dependendo de:
- Arredondamento do pandas/numpy
- A proporção real das classes no dataset
- Se há desbalanceamento das classes

## Solução Implementada

### Correção Aplicada:

1. **Backend (`backend/app/controllers/api.py`)**:
   - Adicionado parâmetro `test_size` opcional no endpoint `/api/train`
   - Validação: aceita valores entre 0.1 (10%) e 0.5 (50%)
   - Valor padrão: 0.2 (20%)

2. **Frontend - API Service (`frontend/src/services/api.js`)**:
   - Atualizada função `trainModel` para aceitar parâmetro `testSize`

3. **Frontend - Página de Treino (`frontend/src/pages/Train.jsx`)**:
   - Adicionado seletor visual (slider) para escolher a proporção teste/treino
   - Opções: 10% a 50% (step de 5%)
   - Mostra preview de quantas amostras serão usadas para treino e teste

### Como usar:

1. Vá para a página **"Treinar Modelo"**
2. Faça upload do seu CSV
3. Use o slider **"Proporção Teste/Treino"** para ajustar:
   - **10% teste**: com 80 dados → 8 teste, 72 treino
   - **20% teste**: com 80 dados → 16 teste, 64 treino (padrão)
   - **30% teste**: com 80 dados → 24 teste, 56 treino
   - **50% teste**: com 80 dados → 40 teste, 40 treino
4. Clique em **"Iniciar Treinamento"**
m
### Recomendação:

- Para ter uma matriz de confusão mais significativa com datasets pequenos:
  - Use **test_size = 0.3 (30%)** ou **0.4 (40%)** para ter mais amostras no teste
  - Ou use **pelo menos 100-200 amostras** no dataset total
- O padrão de 20% é recomendado para datasets maiores (500+ amostras)

## Verificação

Agora você pode ajustar a proporção e ver os valores da matriz de confusão mudando de acordo com o tamanho do conjunto de teste.
