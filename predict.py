from transformers import pipeline
from PIL import Image
import cv2
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


classifier = pipeline(
    "image-classification",
    model="delpot/steganograph-ia-detector"
)


def analyze_pil_image(image):
    results = classifier(image)

    ai_score = 0.0
    real_score = 0.0

    for item in results:
        label = item["label"].lower()
        score = float(item["score"])

        if "ai" in label or "fake" in label or "generated" in label:
            ai_score += score
        else:
            real_score += score

    if ai_score >= real_score:
        label = "AI Generated"
        confidence = ai_score * 100
    else:
        label = "Real Image"
        confidence = real_score * 100

    confidence = round(min(confidence, 99.9), 2)

    return {
        "label": label,
        "confidence": confidence
    }


def predict_image(image_path):

    image = Image.open(image_path).convert("RGB")

    result = analyze_pil_image(image)

    result["filename"] = os.path.basename(image_path)
    result["frames_checked"] = 1

    return result


def predict_video(video_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Could not open video.")

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 25

    duration = total_frames / fps if total_frames > 0 else 0

    sample_count = min(8, max(3, int(duration / 2) + 1))

    predictions = []

    for i in range(sample_count):

        if total_frames > 0:
            frame_number = int(
                i * total_frames / sample_count
            )

            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                frame_number
            )

        success, frame = cap.read()

        if not success:
            continue

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(frame_rgb)

        result = analyze_pil_image(image)

        predictions.append(result)

    cap.release()

    if not predictions:
        raise Exception(
            "Could not analyze video frames."
        )

    ai_values = [
        x["confidence"]
        for x in predictions
        if x["label"] == "AI Generated"
    ]

    real_values = [
        x["confidence"]
        for x in predictions
        if x["label"] == "Real Image"
    ]

    ai_average = (
        sum(ai_values) / len(ai_values)
        if ai_values else 0
    )

    real_average = (
        sum(real_values) / len(real_values)
        if real_values else 0
    )

    if ai_average >= real_average:
        label = "AI Generated"
        confidence = ai_average
    else:
        label = "Real Image"
        confidence = real_average

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "filename": os.path.basename(video_path),
        "frames_checked": len(predictions)
    }


def download_media(url):

    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()

    extension = ".jpg"

    if "png" in content_type:
        extension = ".png"

    elif "webp" in content_type:
        extension = ".webp"

    elif "mp4" in content_type:
        extension = ".mp4"

    filename = (
        "url_media_"
        + str(abs(hash(url)))
        + extension
    )

    folder = "uploads"

    os.makedirs(folder, exist_ok=True)

    path = os.path.join(
        folder,
        filename
    )

    with open(path, "wb") as f:
        f.write(response.content)

    return path


def extract_media_from_page(url):

    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    image = soup.find(
        "meta",
        property="og:image"
    )

    if image and image.get("content"):
        return urljoin(
            url,
            image["content"]
        ), "image"

    video = soup.find(
        "meta",
        property="og:video"
    )

    if video and video.get("content"):
        return urljoin(
            url,
            video["content"]
        ), "video"

    image_tag = soup.find("img")

    if image_tag and image_tag.get("src"):
        return urljoin(
            url,
            image_tag["src"]
        ), "image"

    return None, None


def predict_url(url):

    url = url.strip()

    if not (
        url.startswith("http://")
        or url.startswith("https://")
    ):
        raise Exception(
            "Please enter a valid URL starting with http:// or https://"
        )

    lower_url = url.lower()

    # Direct image/video URL
    if any(
        lower_url.split("?")[0].endswith(ext)
        for ext in [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".mp4",
            ".mov",
            ".webm"
        ]
    ):

        path = download_media(url)

        if path.lower().endswith(
            (".mp4", ".mov", ".webm")
        ):
            return predict_video(path)

        return predict_image(path)

    # Webpage / social media URL
    media_url, media_type = extract_media_from_page(url)

    if media_url:

        path = download_media(media_url)

        if media_type == "video":
            return predict_video(path)

        return predict_image(path)

    raise Exception(
        "Could not find accessible media from this URL. "
        "Some social media platforms may block automated access."
    )