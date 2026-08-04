<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/React-18.0%2B-61DAFB?style=for-the-badge&logo=react" alt="React"/>
  <img src="https://img.shields.io/badge/FastAPI-0.104%2B-009688?style=for-the-badge&logo=fastapi" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" alt="Status"/>
</div>

<br/>

<h1 align="center">🔍 True Lens AI</h1>
<p align="center"><b>Multi-Modal Deepfake & Tampering Detection Platform</b></p>

<p align="center">
  <i>Instantly detect AI-generated images, deepfake videos, synthetic voices, and tampered documents.</i>
</p>

<br/>

---

## 🚀 About The Project

**True Lens AI** is your digital truth validator. In an era of misinformation, this tool acts as a forensic microscope for digital media. Upload any file, and our AI will scan it pixel-by-pixel, frame-by-frame, and byte-by-byte to tell you if it's **Real** or **Fake**.

Whether you are a journalist verifying a source, a legal professional checking evidence, or just a concerned citizen, True Lens AI empowers you to see beyond the surface.

---

## ✨ Key Features

| Media Type | Detection Method | What It Catches |
| :--- | :--- | :--- |
| 🖼️ **Images** | **Error Level Analysis (ELA)** + Quadrant Heatmaps | GAN-generated faces (DALL-E, Midjourney), Photoshopped objects, Copy-move forgeries |
| 🎬 **Videos** | **Frame Sampling** + Temporal Inconsistency Check | Lip-sync deepfakes, Face-swapped videos, Spliced/edited clips |
| 🎵 **Audio** | **Spectral Variance Analysis** | AI-generated voices (ElevenLabs, VALL-E), Voice cloning, Audio splicing |
| 📄 **Documents** | **Metadata Forensics** + Text Extraction | Date tampering, Creator/Producer mismatches, Fake contracts & certificates |

---

## 📸 Screenshots

<div align="center">
  <h3>🚨 Suspicious / Manipulated File</h3>
  <img width="1907" height="1033" alt="image" src="https://github.com/user-attachments/assets/39181b48-d12b-4fe9-b7e4-6550dca6893e" />

  

  <h3>✅ Authentic / Real File</h3>
  <img width="1902" height="998" alt="image" src="https://github.com/user-attachments/assets/c7bf5d90-a751-4d79-b0fa-3be0c28b4b1f" />


---

<h2>## 🛠️ Tech Stack</h2>

- **Frontend**: React.js, Tailwind CSS (Dark Cyber Theme)
- **Backend**: FastAPI (Python)
- **AI/ML Libraries**: OpenCV, Librosa, PyPDF2, python-docx
- **Deployment**: Docker-ready

---

<h2>## 💻 Local Setup & Installation</h2>

Follow these steps to run True Lens AI on your local machine.

### 1. Clone the Repository
2. Backend Setup (FastAPI)
bash
cd backend

# Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
3. Frontend Setup (React)
Open a new terminal and navigate to the frontend folder:

bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
4. Access the Application
Open your browser and go to: http://localhost:3000

<h2>🧪 How to Test "Fake" Scenarios</h2>h2
To verify the tool works, use a real-world example:

Fake Image: Upload a heavily compressed screenshot or a low-quality meme.

Fake Document: Run the built-in generator to create a tampered PDF:

bash
cd backend
python make_fake_pdf.py  # Generates a PDF with mismatched dates
Fake Audio: Record a voice using text-to-speech (like Google Translate TTS) and upload it.


<h2>**🔒 Security & Privacy**</h2>
Encryption: All files are encrypted during transfer.

Auto-Delete: Uploaded files are automatically purged from our servers within 24 hours.

No Training: Your personal data is never used to train our AI models.

**<h2>🤝 Contributing**</h2>
Contributions are what make the open-source community amazing! If you have a feature request, bug report, or code improvement, feel free to:

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

**⚖️ Copyright & Rights
All Rights Reserved.
© 2025 Diya Karmakar**

This software and its source code are the exclusive property of Diya Karmakar. Unauthorized copying, modification, distribution, or use of this software, via any medium, is strictly prohibited without prior written permission.

**📧 Contact & Support**
Project Link: https://github.com/diyakarmakar133348-ai/true-lens-ai

Author: Diya Karmakar

<p align="center">Made with ❤️ by <b>Diya Karmakar</b> for truth and transparency.</p> ```



