# 🚀 Guia de Deploy - Delivery Delay Predictor

## O que é VITE_API_URL?

O **frontend** (interface visual) e o **backend** (API) são aplicações separadas que precisam se comunicar.

- **Frontend** = O site que você vê no navegador (vai estar no Vercel)
- **Backend** = O servidor que processa dados e faz previsões (vai estar no Render)

O frontend precisa saber **onde está o backend** para enviar pedidos (como "treinar modelo" ou "fazer previsão"). Essa informação é armazenada na variável `VITE_API_URL`.

### Exemplo prático:

```
Quando você clica em "Treinar Modelo" no site:
1. Frontend (Vercel) envia arquivo → Backend (Render)
2. Backend processa e retorna resultado → Frontend
3. Frontend mostra o resultado na tela
```

**Sem essa variável, o frontend não sabe para onde enviar os dados!**

---

## Estrutura do Projeto

```
├── backend/          # API FastAPI
│   ├── app/          # Código da aplicação
│   ├── requirements.txt
│   ├── runtime.txt
│   └── models/       # Modelos treinados (criado em runtime)
├── frontend/         # Aplicação React + Vite
│   ├── src/
│   ├── dist/         # Build de produção
│   └── .env.example  # Template de variáveis de ambiente
├── Procfile          # Comando para deploy do backend (Render)
└── DEPLOY.md         # Este arquivo
```

---

## Stack de Deploy Recomendada

| Componente | Plataforma | Plano |
|------------|-----------|-------|
| Backend API | Render | Grátis |
| Frontend Web | Vercel | Ilimitado e gratuito |

**Por que essa combinação?**
- **Render**: Permite Web Service gratuito para APIs Python/FastAPI (com sleep após 15 min)
- **Vercel**: Hospedagem gratuita ilimitada para frontends React/Vite (sem sleep)

---

## Deploy no Render (Backend)

### Configuração do Web Service

1. Acesse [render.com](https://render.com) e conecte seu repositório GitHub

2. Clique em **New** → **Web Service**

3. Configure:
   - **Name**: `delivery-predictor-api`
   - **Environment**: `Python`
   - **Root Directory**: `backend` ⚠️ IMPORTANTE!
   
4. Na seção "Build Command":
   
```
pip install --only-binary :all: -r requirements.txt
```

5. Na seção "Start Command":
   
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1 || uvicorn app.main:app --host 0.0.$PORT"
```

6. Selecione o plano gratuito ("Free")

7. Clique em **Deploy Web Service**

8.**Após o deploy**, copie a URL gerada:
   
```
https://delivery-predictor-api.onrender.com → anotando esta URL!
```

---

## Deploy no Vercel (Frontend)

### Configuração via Dashboard

1.**Acesse vercel.com** e faça login com sua conta GitHub
   
2.**Clique em "Add New..." → Project**
   
3.**Selecione seu repositório**
   
4.Na configuração, defina:
   

- Framework Preset: `Vite`  
- Root Directory: `.` ou deixe como está  
- Build Command: `npm run build`
  
5.Em "Environment Variables", adicione:

``` 
Key: VITE_API_URL  
Value: https://delivery-predictor-api.onrender.com ← cole a URL do backend! 
``` 

6.Clique em **Deploy**

7.Obtendo a URL pública:

``` 
Production: https://delivery-delay-predictor.vercel.app → esta é sua URL final! 
``` 

---

## Arquivos Preparados  

Estes arquivos já estão configurados corretamente:

✅ **`Procfile`** — Comando uvicorn na raiz  

✅ **`backend/runtime.txt`** — Versão Python 3.x compatível  

✅ **`backend/requirements.txt`** — Dependências listadas  

✅ **`frontend/.env.example`** — Template variáveis ambiente  

✅ **`frontend/vite.config.js`** — Configuração proxy removida(produção usa variável real)  


--- 

## Após Completar os Dois Deploys


1.Acessar a URL do frontend no navegador


2.Fazer upload inicial dos dados CSV através da interface web


3.O sistema automaticamente:


Salvará modelo treinado nos servidores cloud  


Permitirá previsões futuras sem retrabalho  


---


⚠️ Limitações Importantes sobre Persistência:


O Render apaga modelos treinados quando serviço entra em modo sleep.


Soluções disponíveis:


Re-treinar após cada wake-up automático


Contratar plano pago ($25/mês)


Considerar Railway como alternativa completa($5/mês)


---


Alternativa Completa(Backend + Frontend): Railway.app


Se preferir uma única plataforma com persistência real, experimente Railway:


Plano hobby:$5/mês por projeto completo


Suporte nativo Docker e múltiplos serviços num mesmo projeto



Documentação oficial disponível diretamente nos sites das plataformas.
