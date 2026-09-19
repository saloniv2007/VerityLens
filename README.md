# VerityLens – AI Reality Check

VerityLens is an AI-powered web application designed to analyze digital media and identify whether it appears to be **AI-generated or real**.

The project provides a simple web interface where users can submit supported media and receive an AI-based analysis result with a confidence score.

## 🚀 Features

* 🖼️ **Image Detection** – Analyze images for AI-generated content.
* 🎥 **Video Detection** – Analyze supported video files.
* 🔗 **URL Analysis** – Analyze supported media URLs.
* 📊 **Confidence Score** – Displays the model's confidence with the result.
* 🕘 **Scan History** – Keeps track of previous scan results.
* 📈 **Dashboard** – Displays scan statistics and recent activity.
* 🗄️ **SQLite Database** – Stores scan information locally.
* ⚡ **Flask Web Interface** – Simple and user-friendly interface.

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
* OpenCV
* Requests

## 🔍 How It Works

1. The user selects a scan type.
2. The user uploads an image or video, or provides a supported URL.
3. VerityLens processes the submitted content.
4. The AI detection model analyzes the content.
5. The application displays:

   * Detection label
   * Confidence score
   * Scan type
6. Scan information can be stored and viewed through the History and Dashboard sections.

## 📂 Project Structure

```text
VerityLens/
│
├── app.py
├── predict.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── dashboard.html
│   ├── history.html
│   └── scan_details.html
│
└── static/
    └── style.css
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/saloniv2007/VerityLens.git
cd VerityLens
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment on Windows

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

### 6. Open the application

```text
http://127.0.0.1:5000
```

## 🎯 Purpose

With the increasing use of generative AI, identifying whether digital content appears AI-generated or real can be challenging.

VerityLens aims to provide a simple first-level AI-content detection tool that helps users analyze supported digital media through an easy-to-use web interface.

## ⚠️ Disclaimer

VerityLens provides **AI-based analysis** and should not be treated as an official authentication, forensic verification, or legal verification system.

A **"Real"** result does not guarantee that an image, video, or document is genuinely authentic.

## 👥 Project

**VerityLens – AI Reality Check**

Developed as a hackathon project to explore AI-based digital content detection and analysis.
