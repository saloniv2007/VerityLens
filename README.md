# VerityLens – AI Reality Check

VerityLens is an AI-powered web application designed to analyze digital media and identify whether it appears to be **AI-generated or real**.

The project provides a simple interface where users can submit supported media and receive an analysis result with a confidence score.

## 🚀 Features

* 🖼️ **Image Detection** – Analyze images for AI-generated content.
* 🎥 **Video Detection** – Analyze supported video files.
* 🔗 **URL Analysis** – Analyze supported media URLs.
* 📊 **Confidence Score** – Shows the model's confidence with the result.
* 🕘 **Scan History** – Stores previous scan results.
* 📈 **Dashboard** – Displays scan statistics and recent activity.
* 🗄️ **SQLite Database** – Stores scan information locally.
* ⚡ **Simple Web Interface** – Easy-to-use Flask-based interface.

## 🛠️ Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* JavaScript
* Hugging Face Transformers
* PyTorch
* Pillow

## 🔍 How It Works

1. The user selects a scan type.
2. The user uploads an image/video or provides a supported URL.
3. VerityLens processes the submitted content.
4. The AI detection model analyzes the content.
5. The application displays:

   * Detection label
   * Confidence score
   * Scan type
6. The result is stored in the SQLite database and can be viewed through History and Dashboard.

## 📂 Project Structure

```text
VerityLens/
│
├── app.py
├── predict.py
├── veritylens.db
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── history.html
│   └── dashboard.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── uploads/
```

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd VerityLens
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the local application in your browser:

```text
http://127.0.0.1:5000
'''

## 🎯 Purpose

With the increasing use of generative AI, distinguishing AI-generated digital content from authentic content is becoming more challenging. VerityLens aims to provide a simple and accessible first-level AI-content detection tool.

## ⚠️ Disclaimer

VerityLens provides an AI-based analysis and should not be treated as an official authentication or forensic verification system. A "Real" result does not guarantee that a document, image, or video is genuinely authentic.

## 👥 Project

**VerityLens – AI Reality Check**

Developed as a hackathon project to explore AI-based digital content detection and verification.
