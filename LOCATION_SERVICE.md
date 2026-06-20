# AI-Powered WhatsApp Business Chatbot — MVP

WhatsApp pe chalne wala AI chatbot jo customers se natural conversation karta hai aur business data (products, price, stock, FAQs) se accurate jawab deta hai. Isme system automated **Location Service** bhi integrated hai, jo user ki live location coordinate space parse karke delivery operational radius check karti hai.

---

## Kya karta hai ye project?

| Feature | Kya hota hai |
| --- | --- |
| **General chat** | Hello, kaise ho, thanks — friendly AI replies

 |
| **Product search** | "Tomatoes kitne ka?" → database se price + stock

 |
| **FAQ support** | Delivery, hours, payment — predefined answers

 |
| **Business info** | Shop address, phone, working hours

 |
| **Location Validation** | User clicks "Share Location" → server distance check (Haversine) → Delivery radius confirmation |
| **WhatsApp live** | Customer message → AI reply → WhatsApp pe wapas

 |
| **Admin panel** | Browser se products / FAQs add, edit, delete

 |

---

## Tech Stack

| Layer | Technology | Kyun |
| --- | --- | --- |
| **Backend** | Node.js + Express 5 | APIs, webhook, server

 |
| **Database** | PostgreSQL | Products, FAQs, business data (raw SQL)

 |
| **AI** | OpenAI API (`gpt-3.5-turbo` / `gpt-4.1-mini`) | Natural language replies

 |
| **Messaging** | WhatsApp Cloud API (Meta) | Send / receive WhatsApp messages, Native Location Request

 |
| **Admin UI** | HTML + CSS + JavaScript | Simple panel, no React build step

 |
| **Tunnel (dev)** | ngrok | Local server ko internet pe expose (testing)

 |
| **HTTP client** | axios | WhatsApp API calls

 |

---

## Architecture — message ka flow

```
Customer (WhatsApp Text / Location Share)
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
        ├── webhook.routes.js     → Incoming type interceptor ('text' vs 'location')
        ├── chat.controller.js    → Normalizes payload metadata for execution
        ├── context.service.js    → DB context + Geofencing distance calculation (Haversine)
        ├── openai.service.js     → System prompt context mapping & AI response generation
        ├── whatsapp.service.js   → Send Outbound payload (Text / Native Button Modal)
        └── PostgreSQL            → tables setup (products, faqs, businesses, locations)
        │
        ▼
Customer ko WhatsApp pe reply

```

### Routing Streams (Text vs Location Payload)

```
"Hello/Tomatoes kitne ka hai?"
  → webhook.routes.js (Detects type: "text")
  → context.service.js → SQL search "tomato"
  → AI Reply: "Tomatoes ₹40/kg hain, 50 kg stock available hai."

"User clicks Share Location Button"
  → webhook.routes.js (Detects type: "location")
  → context.service.js → Calculates Haversine distance from shop
  → AI Prompt Context Injection: [SYSTEM: Distance 3.2km. Max Radius: 5km. Status: Deliverable]
  → AI Reply: "Thanks! Aapki location hamare store se 3.2km door hai. Order 30 mins me deliver ho jayega."

```

---

## Technical Core Specifications (Location Implementation)

### 1. Webhook Payload Separation Contract (`webhook.routes.js`)

Meta Graph API runtime checks incoming object array signatures. We route based on explicit `type` assertion:

```javascript
const message = req.body.entry?.?.changes?.?.value?.messages?.;

if (message) {
    const phone = message.from;
    
    if (message.type === 'text') {
        await chatController.processMessage(phone, { type: 'text', body: message.text.body });
    } 
    else if (message.type === 'location') {
        await chatController.processMessage(phone, {
            type: 'location',
            latitude: message.location.latitude,
            longitude: message.location.longitude,
            name: message.location.name || '',
            address: message.location.address || ''
        });
    }
}

```

### 2. Algorithmic Geofencing Layer (`context.service.js`)

Calculates great-circle distance between store point coordinates $(\phi_1, \lambda_1)$ and client terminal destination $(\phi_2, \lambda_2)$ using the **Haversine Formula**:

$$a = \sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cdot\cos(\phi_2)\cdot\sin^2\left(\frac{\Delta\lambda}{2}\right)$$

$$c = 2 \cdot \operatorname{atan2}\left(\sqrt{a}, \sqrt{1-a}\right)$$

$$d = R \cdot c$$

Where $R = 6371\text{ km}$. If calculated value $d \le \text{Max Radius Limit}$, operational status evaluates to valid. This runtime bounding rule is injected directly into the LLM system prompt context array block.

### 3. Outbound Native Location Request Messaging Protocol (`whatsapp.service.js`)

To trigger native structural phone overlays, the API sends a target interactive schema payload object instead of markdown text arrays:

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "PHONE_NUMBER",
  "type": "interactive",
  "interactive": {
    "type": "location_request_message",
    "body": {
      "text": "Apni address boundary verification check karne ke liye niche share button select karein:"
    },
    "action": {
      "name": "send_location"
    }
  }
}

```

---

## Senior Engineering Review Feedback Board 🚨

> ### Architecture Considerations for Team Lead / Senior Developer Review:
> 
> 
> 1. **Response Loop Concurrency Management:** WhatsApp Cloud Engine protocols strictly enforce a `200 OK` response confirmation loop limit within $3000\text{ ms}$. To completely insulate calculations and geofencing verification arrays from blocking operations, `res.sendStatus(200)` handles dispatch actions instantly at endpoint execution baselines before processing business logic asynchronously.
> 2. **Geofencing Spatial Computation Tradeoffs:** Current operations run on standalone mathematical Haversine calculations (straight structural radius strings). Review required: For future scalability, should we transition this to Google Distance Matrix endpoint paths to account for actual driving infrastructure distance instead?
> 3. **Data Layer Persistence Strategy:** Coordinates are currently held directly in-memory within `conversation.store.js` runtime arrays. For production stability, we propose storing spatial attributes directly inside the custom database cluster schemas (`conversations` / `user_locations` structural log sets) to allow long-term delivery route tracking.
> 
> 

---

## Future Enhancements

* Migration to Google Distance Matrix Route Validation Engines
* Spatial coordinate lookup conversion to permanent persistence storage logs


* Automatic message retry deduplication loops powered by memory caching nodes


* Lexical translation parsing mapping ("tamatar", "aloo" aliases mapped to core English DB indexes)


---

## License

ISC