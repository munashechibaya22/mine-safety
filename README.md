# Mine Safety Detection System 🏗️

AI-powered Personal Protective Equipment (PPE) detection system for mine safety compliance.

![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Overview

This system uses computer vision and deep learning to automatically detect whether workers are wearing required safety equipment before entering mine sites. It helps prevent accidents by ensuring PPE compliance.

## ✨ Features

- 🤖 **AI-Powered Detection** - YOLO-based object detection for PPE
- 👤 **User Authentication** - Secure JWT-based auth system
- 📊 **Analytics Dashboard** - Real-time statistics and insights
- 📸 **Multi-Input Support** - Camera, image upload, or video
- 🔍 **Spatial Logic** - Matches equipment to specific workers
- 📱 **Responsive Design** - Works on desktop and mobile
- 🗄️ **PostgreSQL Database** - Reliable data storage
- 🚀 **Production Ready** - Deployed on Render

## 🛡️ Detected Safety Equipment

- ✅ Hard Hat / Helmet
- ✅ Safety Vest
- ✅ Face Mask
- ✅ Safety Goggles (optional)
- ✅ Gloves (optional)

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Production database
- **YOLO** - Object detection model
- **OpenCV** - Image processing
- **JWT** - Authentication

### Frontend
- **React** - UI framework
- **Tailwind CSS** - Styling
- **Axios** - API requests
- **React Router** - Navigation

### Deployment
- **Render** - Cloud platform
- **GitHub** - Version control

## 📁 Project Structure

```
mine-safety/
├── mine-safety-backend/       # FastAPI backend
│   ├── main.py               # API endpoints
│   ├── auth.py               # Authentication
│   ├── models.py             # Database models
│   ├── detection_service.py  # AI detection logic
│   ├── best.onnx            # YOLO model
│   └── requirements.txt      # Python dependencies
│
├── mine-safety-frontend/      # React frontend
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── components/      # Reusable components
│   │   └── context/         # State management
│   └── package.json         # Node dependencies
│
├── render.yaml               # Render deployment config
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/munashechibaya22/mine-safety.git
   cd mine-safety
   ```

2. **Setup Backend**
   ```bash
   cd mine-safety-backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run Backend**
   ```bash
   python -m uvicorn main:app --reload
   ```
   Backend runs at: http://localhost:8000

5. **Setup Frontend** (new terminal)
   ```bash
   cd mine-safety-frontend
   npm install
   npm run dev
   ```
   Frontend runs at: http://localhost:5173

## 🌐 Deployment

### Deploy to Render (Free)

1. **Push to GitHub**
   ```bash
   # Run the deployment script
   ./deploy_to_github.bat  # Windows
   # or
   ./deploy_to_github.sh   # Linux/Mac
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New +" → "Blueprint"
   - Select your repository
   - Click "Apply"

3. **Done!** Your app will be live in ~10 minutes

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions.

## 📊 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

```
POST /api/auth/register    - Register new user
POST /api/auth/login       - Login user
POST /api/detect           - Detect PPE in image/video
GET  /api/detections       - Get detection history
GET  /api/dashboard/stats  - Get dashboard statistics
```

## 🎓 How It Works

1. **Image Capture** - User uploads image or uses camera
2. **Person Detection** - AI identifies people in the image
3. **Equipment Detection** - AI detects safety equipment
4. **Spatial Matching** - System matches equipment to workers using bounding box overlap
5. **Compliance Check** - Verifies all required equipment is present
6. **Decision** - Approves or denies entry with detailed reason

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- SQL injection prevention
- Environment variable configuration

## 📈 Future Enhancements

- [ ] Real-time video streaming
- [ ] Email/SMS notifications
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Export reports to PDF
- [ ] Integration with access control systems
- [ ] Advanced analytics and ML insights

## 🤝 Contributing

This is a school project, but suggestions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Munashe Chibaya**
- GitHub: [@munashechibaya22](https://github.com/munashechibaya22)

## 🙏 Acknowledgments

- YOLO by Ultralytics for object detection
- FastAPI for the amazing web framework
- React team for the UI library
- Render for free hosting
- My school for the project opportunity

## 📞 Support

For questions or issues:
1. Check [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
2. Open an issue on GitHub
3. Contact via GitHub profile

---

**⚠️ Disclaimer**: This is an educational project. For production use in actual mine sites, additional safety certifications and testing would be required.

Made with ❤️ for mine safety
