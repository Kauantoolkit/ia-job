# 🚀 Guia de Deploy - Delivery Delay Predictor

## Opções Gratuitas Recomendadas

### 1. Render (Recomendado)
- **Backend**: https://render.com
- **Frontend**: https://render.com (Static Sites)
- **Grátis**: Sim (com sleep após 15 min)

### 2. Vercel + Render
- **Frontend**: https://vercel.com (ilimitado)
- **Backend**: https://render.com

---

## Deploy no Render

### Backend (FastAPI)

1. Acesse [render.com](https://render.com) e conecte seu repositório GitHub

2. Clique em **New** → **Web Service**

3. Configure:
   - **Name**: delivery-predictor-api
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Free Instance**: Selecione

4. Clique em **Deploy Web Service**

5. Após o deploy, copie a URL (ex: `https://delivery-predictor-api.onrender.com`)

---

### Frontend (React)

1. No Render, clique em **New** → **Static Site**

2. Configure:
   - **Name**: delivery-predictor-frontend
   - **Repository**: Seu repositório
   - **Build Command**: `npm run build`
   - **Publish Directory**: `dist`
   - **Environment**: Node

3. Configure a variável de ambiente:
   - Key: `VITE_API_URL`
   - Value: URL do seu backend (ex: `https://delivery-predictor-api.onrender.com`)

4. Clique em **Deploy Static Site**

---

## Arquivos Preparados

- `backend/runtime.txt` - Versão do Python (3.11)
- `backend/Procfile` - Comando de inicialização
- `frontend/.env.example` - Template de variáveis de ambiente

---

## Após o Deploy

1. Configure a variável `VITE_API_URL` no frontend com a URL do backend
2. Acesse o frontend e faça o upload do CSV para treinar o modelo
3. O modelo será salvo no servidor do Render

---

## Nota sobre o Banco de Dados

⚠️ **Importante**: O Render (plano gratuito) não persiste arquivos. O modelo treinado será perdido se o serviço "dormir".

**Soluções**:
1. Re-treine o modelo após cada wake-up
2. Use um serviço de storage externo (S3, Cloudinary)
3. Faça upgrade para plano pago

---

## Alternativa: Railway

Se precisar de persistência, considere [Railway](https://railway.app):
- $5/mês
- Persiste arquivos
- Mais recursos
