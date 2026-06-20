# AI-Powered WhatsApp Business Chatbot — MVP

WhatsApp pe chalne wala AI chatbot jo customers se natural conversation karta hai aur business data (products, price, stock, FAQs) se accurate jawab deta hai.

---

## Kya karta hai ye project?

| Feature | Kya hota hai |
|---------|----------------|
| **General chat** | Hello, kaise ho, thanks — friendly AI replies |
| **Product search** | "Tomatoes kitne ka?" → database se price + stock |
| **FAQ support** | Delivery, hours, payment — predefined answers |
| **Business info** | Shop address, phone, working hours |
| **WhatsApp live** | Customer message → AI reply → WhatsApp pe wapas | 
| **Admin panel** | Browser se products / FAQs add, edit, delete |

---

## Tech Stack

| Layer | Technology | Kyun |
|-------|------------|------|
| **Backend** | Node.js + Express 5 | APIs, webhook, server |
| **Database** | PostgreSQL | Products, FAQs, business data (raw SQL) |
| **AI** | OpenAI API (`gpt-3.5-turbo` / `gpt-4.1-mini`) | Natural language replies |
| **Messaging** | WhatsApp Cloud API (Meta) | Send / receive WhatsApp messages |
| **Admin UI** | HTML + CSS + JavaScript | Simple panel, no React build step |
| **Tunnel (dev)** | ngrok | Local server ko internet pe expose (testing) |
| **HTTP client** | axios | WhatsApp API calls |

---

## Architecture — message ka flow

```
Customer (WhatsApp)
        │
        ▼
WhatsApp Cloud API (Meta)
        │
        ▼  POST /webhook
   ngrok (dev) / VPS domain (prod)
        │
        ▼
   Express Server (port 3000)
        │
        ├── webhook.routes.js     → message receive
        ├── chat.controller.js    → orchestration
        ├── context.service.js    → DB se product/FAQ context
        ├── openai.service.js     → AI reply generate
        ├── whatsapp.service.js   → reply bhejna
        └── PostgreSQL            → products, faqs, business
        │
        ▼
Customer ko WhatsApp pe reply
```

### General chat vs business chat

```
"Hello kaise ho?"
  → Product search: koi match nahi
  → AI: friendly greeting (conversation history use hoti hai)

"Tomatoes kitne ka hai?"
  → context.service.js → SQL search "tomato"
  → AI ko product data milta hai: ₹40/kg, 50 kg stock
  → AI: business-aware reply (price invent nahi karta)
```

---

## Project Structure — kahan kya hai

```
ai-chatbot-mvp/
│
├── sql/
│   ├── schema.sql          # Tables: businesses, products, faqs, conversations
│   └── seed.sql            # Demo data (Jasper's Market, tomatoes, etc.)
│
├── scripts/
│   └── migrate.js          # DB create + schema + seed (npm run migrate)
│
├── public/admin/           # Admin Dashboard (browser UI)
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── src/
│   ├── server.js           # Entry point — Express app start
│   │
│   ├── db/
│   │   └── pool.js         # PostgreSQL connection pool
│   │
│   ├── routes/             # URL → handler mapping
│   │   ├── chat.routes.js       # POST /chat
│   │   ├── webhook.routes.js    # GET/POST /webhook (WhatsApp)
│   │   ├── product.routes.js    # /api/products/*
│   │   ├── faq.routes.js        # /api/faqs/*
│   │   ├── business.routes.js   # /api/business
│   │   └── admin.routes.js      # /api/admin/verify
│   │
│   ├── controllers/        # Request handle + response
│   │   ├── chat.controller.js   # processMessage() — core AI flow
│   │   ├── product.controller.js
│   │   ├── faq.controller.js
│   │   └── business.controller.js
│   │
│   ├── services/           # External APIs + business logic
│   │   ├── openai.service.js    # OpenAI chat completion
│   │   ├── whatsapp.service.js  # Meta Graph API — message send
│   │   └── context.service.js   # Message → DB context for AI
│   │
│   ├── repositories/       # Database queries (raw SQL)
│   │   ├── product.repository.js
│   │   ├── faq.repository.js
│   │   └── business.repository.js
│   │
│   ├── middleware/
│   │   └── admin.middleware.js  # Admin API key check
│   │
│   ├── utils/
│   │   └── conversation.store.js  # In-memory chat history (per phone)
│   │
│   └── prompts/
│       └── system.prompt.js     # AI system instructions
│
├── .env                    # Secrets (git me mat daalo)
├── .env.example            # Template
├── package.json
└── docker-compose.yml      # Optional — Docker wale devs ke liye
```

---

## Database Tables

| Table | Kya store hota hai |
|-------|-------------------|
| `businesses` | Shop name, address, phone, hours, email |
| `products` | Name, price, stock, unit (kg/liter), description |
| `faqs` | Question + answer pairs |
| `conversations` | Customer messages (future use — abhi memory me history) |

---

## API Endpoints

### Health
| Method | URL | Kaam |
|--------|-----|------|
| GET | `/health` | Server alive check |

### Chat (testing without WhatsApp)
| Method | URL | Body |
|--------|-----|------|
| POST | `/chat` | `{ "message": "Hello", "phone": "919024359055" }` |

### WhatsApp Webhook
| Method | URL | Kaam |
|--------|-----|------|
| GET | `/webhook` | Meta verification (`hub.challenge`) |
| POST | `/webhook` | Incoming WhatsApp messages |

### Products
| Method | URL | Auth |
|--------|-----|------|
| GET | `/api/products` | Open |
| GET | `/api/products/search?q=tomato` | Open |
| GET | `/api/products/:id` | Open |
| POST | `/api/products` | Admin key |
| PUT | `/api/products/:id` | Admin key |
| DELETE | `/api/products/:id` | Admin key |

### FAQs
| Method | URL | Auth |
|--------|-----|------|
| GET | `/api/faqs` | Open |
| POST | `/api/faqs` | Admin key |
| PUT | `/api/faqs/:id` | Admin key |
| DELETE | `/api/faqs/:id` | Admin key |

### Business
| Method | URL | Kaam |
|--------|-----|------|
| GET | `/api/business` | Shop info |

### Admin
| Method | URL | Kaam |
|--------|-----|------|
| GET | `/api/admin/verify` | Login key validate |

**Admin key header:** `x-admin-key: your-admin-secret`

---

## Setup Guide

### 1. Prerequisites
- Node.js 18+
- PostgreSQL 16 (Homebrew Mac: `brew install postgresql@16`)
- Meta Developer account (WhatsApp Cloud API)
- OpenAI API key
- ngrok (WhatsApp local testing ke liye)

### 2. Install
```bash
cd ai-chatbot-mvp
npm install
```

### 3. Environment
```bash
cp .env.example .env
# .env me apni keys daalo
```

### 4. Database
```bash
brew services start postgresql@16   # Mac
npm run migrate                     # tables + demo data
```

### 5. Start server
```bash
npm start
# Server running on port 3000
```

### 6. WhatsApp testing (local)
```bash
# Alag terminal
ngrok http 3000
```

Meta Console → WhatsApp → Configuration:
- **Callback URL:** `https://YOUR-NGROK-URL/webhook`
- **Verify token:** `.env` wala `WEBHOOK_VERIFY_TOKEN`
- **Subscribe:** `messages` ✓

WABA subscribe (ek baar):
```
POST /v25.0/{WABA-ID}/subscribed_apps
```
(Graph API Explorer se)

### 7. Admin Panel
```
http://localhost:3000/admin
```
Login: `.env` me `ADMIN_API_KEY`

---

## Environment Variables

| Variable | Kya hai |
|----------|---------|
| `PORT` | Server port (default 3000) |
| `OPENAI_API_KEY` | OpenAI secret key |
| `OPENAI_MODEL` | Model name (`gpt-3.5-turbo`) |
| `WEBHOOK_VERIFY_TOKEN` | Meta webhook verify string |
| `WHATSAPP_ACCESS_TOKEN` | Meta temporary/permanent token |
| `WHATSAPP_PHONE_NUMBER_ID` | Business phone number ID |
| `WHATSAPP_API_VERSION` | Graph API version (`v25.0`) |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port |
| `DB_NAME` | Database name |
| `DB_USER` | DB username |
| `DB_PASSWORD` | DB password |
| `ADMIN_API_KEY` | Admin panel + write APIs |

---

## NPM Scripts

| Command | Kaam |
|---------|------|
| `npm start` | Server start |
| `npm run migrate` | DB + tables + seed data |

---

## Core Flow — code me kya hota hai

### 1. WhatsApp message aata hai
**File:** `src/routes/webhook.routes.js`
- Meta `POST /webhook` bhejta hai
- Message text + customer phone number parse hota hai
- Turant `200 OK` — phir background me process

### 2. Message process hota hai
**File:** `src/controllers/chat.controller.js` → `processMessage()`
- User message history me save (`conversation.store.js`)
- Last 6 messages AI ko bheje jaate hain

### 3. Business context banता hai
**File:** `src/services/context.service.js`
- Message se keywords nikal ke product search (SQL)
- Business info + FAQs load
- AI ke liye text context ready

### 4. AI reply generate
**File:** `src/services/openai.service.js`
- System prompt + business context + chat history → OpenAI
- Short, Hindi/English friendly reply

### 5. WhatsApp pe reply
**File:** `src/services/whatsapp.service.js`
- Meta Graph API: `POST /{phone-id}/messages`
- Customer ke number pe text bhejta hai

---

## MVP Phases — status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | AI Chat Foundation (`/chat`) | ✅ Done |
| 2 | PostgreSQL + Product APIs | ✅ Done |
| 3 | AI + Product integration | ✅ Done |
| 4 | Admin Dashboard | ✅ Done |
| 5 | WhatsApp live integration | ✅ Done |

---

## Testing Checklist

```bash
# Health
curl http://localhost:3000/health

# Product search
curl "http://localhost:3000/api/products/search?q=tomato"

# AI chat (bina WhatsApp)
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Tomatoes kitne ka hai?","phone":"919024359055"}'

# Admin
open http://localhost:3000/admin
```

WhatsApp: `+1 555 651 2593` (test number) ko message bhejo.

---

## Common Issues

| Problem | Fix |
|---------|-----|
| Port 3000 busy | `lsof -i :3000` → kill process → `npm start` |
| WhatsApp token expire | Meta Console se naya token → `.env` update |
| Webhook nahi aata | ngrok chal raha? URL Meta me sahi? `messages` subscribed? |
| WABA subscribe | `POST /{WABA-ID}/subscribed_apps` |
| DB connection fail | `brew services start postgresql@16` |
| ngrok 8012 error | `npm start` pehle, phir ngrok |
| Admin 401 | Sahi `ADMIN_API_KEY` login me daalo |

---

## Future Enhancements

- VPS deploy (24/7, bina ngrok)
- Permanent WhatsApp System User token
- Conversation history PostgreSQL me save
- Message deduplication (duplicate reply fix)
- Hindi product aliases ("tamatar" → Tomatoes)
- Multi-business / SaaS support
- PDF knowledge base, voice messages, order placement

---

## Team Notes

- **Docker optional** — Homebrew PostgreSQL se kaam chal jata hai Mac pe
- **Raw SQL** — koi ORM nahi, `pg` package + repository pattern
- **`.env` git me mat daalo** — secrets safe rakho
- **ngrok sirf development** — production me VPS + domain use karo

---

## License

ISC
