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
MONGODB_URI = mongodb+srv://<your-username>:<your-password>@cluster0.<your-project>.mongodb.net

CLOUDINARY_CLOUD_NAME = <your-cloudinary-cloud-name>
CLOUDINARY_API_KEY = <your-cloudinary-api-key>
CLOUDINARY_API_SECRET = <your-cloudinary-api-key>

GOOGLE_CLIENT_ID = <your-google-client-id> 
GOOGLE_CLIENT_SECRET = <your-google-client-secret>
GOOGLE_CALLBACK_URL=http://localhost:8000/auth/google/callback

JWT_SECRET = <your-jwt-secret>

EMAIL_ID = <your-email-id>
APP_PASSWORD = <your-app-password>
```

Run backend

```bash
npm run dev
```

The frontend will be running on `http://localhost:8000`
