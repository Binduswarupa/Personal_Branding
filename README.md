# 🚀 BrandBoost AI — LinkedIn Branding Assistant

AI-powered platform to help students, freshers, and professionals improve their LinkedIn presence through profile analysis, content generation, branding scoring, and engagement strategies.

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | HTML5, CSS3, Vanilla JS, Bootstrap 5, Chart.js, Font Awesome |
| **Backend** | Python Flask, Flask-CORS, PyMongo, JWT Auth |
| **Database** | MongoDB Atlas |
| **AI** | Groq API (LLaMA 3.3-70B-Versatile) |

## 📁 Project Structure

```
├── frontend/
│   ├── index.html              # Landing page
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── dashboard.html          # Main dashboard
│   ├── profile-analysis.html   # AI profile analyzer
│   ├── headline-generator.html # Headline generator
│   ├── about-generator.html    # About section generator
│   ├── post-generator.html     # Post generator
│   ├── hashtag-generator.html  # Hashtag generator
│   ├── branding-score.html     # Branding score calculator
│   ├── history.html            # Generation history
│   ├── css/style.css           # Main styles
│   ├── css/dashboard.css       # Dashboard styles
│   ├── js/auth.js              # Authentication module
│   ├── js/ai.js                # AI integration module
│   ├── js/dashboard.js         # Dashboard module
│   └── js/charts.js            # Chart.js module
│
├── backend/
│   ├── app.py                  # Flask application entry
│   ├── config.py               # Configuration
│   ├── database.py             # MongoDB connection
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   ├── routes/auth.py          # Auth endpoints
│   ├── routes/profile.py       # Profile analysis endpoints
│   ├── routes/content.py       # Content generation endpoints
│   ├── routes/branding.py      # Branding score endpoints
│   ├── routes/history.py       # History endpoints
│   ├── models/user.py          # User model
│   └── models/branding.py      # Branding model
```

## ⚡ Quick Start

### 1. Clone & Configure

```bash
cd backend
```

Edit `.env` with your credentials:
```
GROQ_API_KEY=your_groq_api_key
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/linkedin_branding
JWT_SECRET=your_secret_key
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## 🔌 REST API Documentation

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login & get JWT |
| GET | `/api/auth/me` | Get current user |
| PUT | `/api/auth/update-profile` | Update profile |

### Profile Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/profile/analyze` | AI profile analysis |
| POST | `/api/profile/resume-analyze` | ATS resume check |
| POST | `/api/profile/career-roadmap` | Career roadmap |
| POST | `/api/profile/recruiter-visibility` | Visibility prediction |

### Content Generation

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/content/generate-headlines` | Generate 10 headlines |
| POST | `/api/content/generate-about` | Generate about section |
| POST | `/api/content/generate-post` | Generate LinkedIn post |
| POST | `/api/content/generate-hashtags` | Generate hashtags |
| POST | `/api/content/content-calendar` | 30-day content calendar |

### Branding

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/branding/score` | Calculate branding score |
| GET | `/api/branding/latest-report` | Get latest report |

### History

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/history/` | Full generation history |
| GET | `/api/history/stats` | Dashboard statistics |
| GET | `/api/history/posts` | Posts history |
| DELETE | `/api/history/<type>/<id>` | Delete history item |

## 🚀 Deployment

### Render (Backend)

1. Push code to GitHub
2. Create new **Web Service** on Render
3. Set **Root Directory**: `backend`
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `gunicorn app:app`
6. Add environment variables in Render dashboard

### Vercel (Frontend)

1. Create `vercel.json` in `frontend/`:
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```
2. Deploy via Vercel CLI: `cd frontend && vercel`
3. Update `API_BASE` in `js/auth.js` to your Render URL

## 🔐 Security

- JWT token authentication on all protected routes
- bcrypt password hashing
- Input validation on all endpoints
- CORS configured for frontend origin
- Environment variables for secrets

## 📊 MongoDB Collections

- `users` — User accounts and profile data
- `generated_posts` — AI-generated posts
- `generated_headlines` — AI-generated headlines
- `generated_abouts` — AI-generated about sections
- `branding_reports` — Branding score reports

## 📝 License

MIT License
