### Brief About The App 
### Frontend Setup

```bash
cd Frontend; npm install
```

Create .env file in the frontend and write the following:

```env
VITE_LOCALHOST = http://localhost:8000
VITE_SERVER_URL = <your deployment link>
```

Run frontend

```bash
npm run dev
```

The frontend will be running on `http://localhost:5173`

### Backend Setup

```bash
cd ../Backend; npm install
```

Create .env file in the frontend and write the following:

```env
PORT = 8000
CORS_ORIGIN = *
MONGODB_URI = mongodb+srv://jainish040405:PrgxBpdSskguTbLK@cluster0.iq94bwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0


CLOUDINARY_CLOUD_NAME = djp8thfis
CLOUDINARY_API_KEY = 623715936837455
CLOUDINARY_API_SECRET = HMXQtx5cd6byAlmgszpXHpXsxts

GOOGLE_CLIENT_ID = 20629568088-ucpttsqijn43gk8nlgalji5n6a2svp3s.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET = 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
GOOGLE_CALLBACK_URL=http://localhost:8000/auth/google/callback

JWT_SECRET = 9d9f2da23e0220d7fd24fc8c210d5bfe65366ad793e3ff5fcc17519a0bed8ddb

EMAIL_ID = bhagatdhruv2005@gmail.com
APP_PASSWORD = axui qwzh jprn ydxr
```

Run backend

```bash
npm run dev
```

The frontend will be running on `http://localhost:8000`
