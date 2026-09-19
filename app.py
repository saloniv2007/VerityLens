from flask import Flask, render_template, request, send_from_directory
from predict import predict_image, predict_video, predict_url

import os
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "veritylens.db")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm"}


# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    # Create table if database is completely new
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            label TEXT,
            confidence REAL,
            scan_type TEXT,
            created_at TEXT
        )
    """)

    # Check existing columns
    existing_columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(scans)").fetchall()
    }

    # Add missing columns to an old database
    required_columns = [
        ("filename", "TEXT"),
        ("label", "TEXT"),
        ("confidence", "REAL"),
        ("scan_type", "TEXT"),
        ("created_at", "TEXT")
    ]

    for column_name, column_type in required_columns:
        if column_name not in existing_columns:
            conn.execute(
                f"ALTER TABLE scans ADD COLUMN {column_name} {column_type}"
            )

    conn.commit()
    conn.close()


def save_scan(filename, label, confidence, scan_type):
    conn = get_db()

    conn.execute("""
        INSERT INTO scans
        (filename, label, confidence, scan_type, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        filename,
        label,
        confidence,
        scan_type,
        datetime.now().strftime("%d %b %Y, %I:%M %p")
    ))

    conn.commit()

    scan_id = conn.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()[0]

    conn.close()

    return scan_id


# =========================================================
# FILE VALIDATION
# =========================================================

def allowed_file(filename, extensions):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in extensions
    )


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# MAIN SCAN
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    scan_type = request.form.get("scan_type", "image")

    try:

        # =================================================
        # IMAGE
        # =================================================

        if scan_type == "image":

            if "file" not in request.files:
                return render_template(
                    "index.html",
                    error="Please select an image."
                )

            file = request.files["file"]

            if file.filename == "":
                return render_template(
                    "index.html",
                    error="Please select an image."
                )

            if not allowed_file(file.filename, IMAGE_EXTENSIONS):
                return render_template(
                    "index.html",
                    error="Unsupported image format."
                )

            filename = secure_filename(file.filename)

            save_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(save_path)

            result = predict_image(save_path)

            scan_id = save_scan(
                filename,
                result["label"],
                result["confidence"],
                "Image"
            )

        # =================================================
        # VIDEO
        # =================================================

        elif scan_type == "video":

            if "file" not in request.files:
                return render_template(
                    "index.html",
                    error="Please select a video."
                )

            file = request.files["file"]

            if file.filename == "":
                return render_template(
                    "index.html",
                    error="Please select a video."
                )

            if not allowed_file(file.filename, VIDEO_EXTENSIONS):
                return render_template(
                    "index.html",
                    error="Unsupported video format."
                )

            filename = secure_filename(file.filename)

            save_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(save_path)

            result = predict_video(save_path)

            scan_id = save_scan(
                filename,
                result["label"],
                result["confidence"],
                "Video"
            )

        # =================================================
        # URL
        # =================================================

        elif scan_type == "url":

            url = request.form.get("url", "").strip()

            if not url:
                return render_template(
                    "index.html",
                    error="Please enter a URL."
                )

            result = predict_url(url)

            filename = result.get("filename")

            scan_id = save_scan(
                filename if filename else url,
                result["label"],
                result["confidence"],
                "URL"
            )

        # =================================================
        # INVALID TYPE
        # =================================================

        else:

            return render_template(
                "index.html",
                error="Invalid scan type."
            )

        # =================================================
        # RESULT
        # =================================================

        result["id"] = scan_id

        if scan_type == "image":
            result["scan_type"] = "Image"

        elif scan_type == "video":
            result["scan_type"] = "Video"

        else:
            result["scan_type"] = "URL"

        return render_template(
            "result.html",
            result=result
        )

    except Exception as e:

        print("ERROR:", e)

        return render_template(
            "index.html",
            error=f"Scan failed: {str(e)}"
        )


# =========================================================
# UPLOADED FILES
# =========================================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# =========================================================
# HISTORY
# =========================================================

@app.route("/history")
def history():

    conn = get_db()

    scans = conn.execute("""
        SELECT *
        FROM scans
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "history.html",
        scans=scans
    )


# =========================================================
# SCAN DETAILS
# =========================================================

@app.route("/scan/<int:scan_id>")
def scan_details(scan_id):

    conn = get_db()

    scan = conn.execute("""
        SELECT *
        FROM scans
        WHERE id = ?
    """, (scan_id,)).fetchone()

    conn.close()

    if scan is None:

        return render_template(
            "index.html",
            error="Scan not found."
        )

    return render_template(
        "result.html",
        result={
            "id": scan["id"],
            "filename": scan["filename"],
            "label": scan["label"],
            "confidence": scan["confidence"],
            "scan_type": scan["scan_type"]
        }
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    conn = get_db()

    total = conn.execute(
        "SELECT COUNT(*) FROM scans"
    ).fetchone()[0]

    ai_count = conn.execute("""
        SELECT COUNT(*)
        FROM scans
        WHERE label = 'AI Generated'
    """).fetchone()[0]

    real_count = conn.execute("""
        SELECT COUNT(*)
        FROM scans
        WHERE label = 'Real Image'
    """).fetchone()[0]

    avg_confidence = conn.execute("""
        SELECT AVG(confidence)
        FROM scans
    """).fetchone()[0]

    recent_scans = conn.execute("""
        SELECT *
        FROM scans
        ORDER BY id DESC
        LIMIT 6
    """).fetchall()

    conn.close()

    if avg_confidence is None:
        avg_confidence = 0

    return render_template(
        "dashboard.html",
        total=total,
        ai_count=ai_count,
        real_count=real_count,
        avg_confidence=round(avg_confidence, 1),
        recent_scans=recent_scans
    )


# =========================================================
# FILE TOO LARGE
# =========================================================

@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error="File is too large. Maximum size is 100 MB."
    ), 413


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    init_db()

    print("\n====================================")
    print("          VERITYLENS AI")
    print("====================================")
    print("Server: http://127.0.0.1:5000")
    print("====================================\n")

    app.run(debug=True)

