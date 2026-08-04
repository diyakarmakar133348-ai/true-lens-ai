import cv2
import numpy as np
import base64
import os
import tempfile
import io
import re
import datetime

# --- Optional Imports for Audio & Docs ---
try:
    import librosa
    import matplotlib.pyplot as plt
except ImportError:
    librosa = None
    plt = None

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

# ---------- HELPER: ELA for a single frame ----------
def run_ela_on_frame(frame_bytes, quality=90):
    try:
        nparr = np.frombuffer(frame_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return False, 5.0, 0.0
        
        img = cv2.resize(img, (256, 256))
        temp_path = "temp_ela_frame.jpg"
        cv2.imwrite(temp_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        compressed = cv2.imread(temp_path)
        diff = cv2.absdiff(img, compressed)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        mean_ela = np.mean(diff_gray)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        is_fake = mean_ela > 10.0
        confidence = min(95, (mean_ela / 20) * 100)
        return is_fake, round(confidence, 2), round(mean_ela, 2)
    except:
        return False, 5.0, 0.0

# ---------- ENHANCED IMAGE PROCESSOR (FULL INFO) ----------
def process_image(file_bytes, filename):
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {"error": "Invalid image file"}
    
    h, w = img.shape[:2]
    img_resized = cv2.resize(img, (512, 512))
    temp_path = "temp_img.jpg"
    cv2.imwrite(temp_path, img_resized, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    compressed = cv2.imread(temp_path)
    diff = cv2.absdiff(img_resized, compressed)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # --- Full ELA Statistics ---
    mean_ela = np.mean(diff_gray)
    max_ela = np.max(diff_gray)
    var_ela = np.var(diff_gray)
    
    # --- Quadrant Analysis (Find where the fake is) ---
    h_q = 256 // 2
    w_q = 256 // 2
    quadrants = {
        "Top-Left": diff_gray[0:h_q, 0:w_q],
        "Top-Right": diff_gray[0:h_q, w_q:256],
        "Bottom-Left": diff_gray[h_q:256, 0:w_q],
        "Bottom-Right": diff_gray[h_q:256, w_q:256]
    }
    high_risk_quadrants = []
    for name, q_data in quadrants.items():
        q_mean = np.mean(q_data)
        if q_mean > 12.0:  # Threshold for quadrant suspicion
            high_risk_quadrants.append(name)
    
    # Generate Heatmap
    ela_map = cv2.normalize(diff_gray, None, 0, 255, cv2.NORM_MINMAX)
    ela_colored = cv2.applyColorMap(ela_map, cv2.COLORMAP_JET)
    _, buffer = cv2.imencode('.png', ela_colored)
    heatmap_b64 = "data:image/png;base64," + base64.b64encode(buffer).decode('utf-8')
    
    if os.path.exists(temp_path):
        os.remove(temp_path)
    
    # Final Verdict
    is_fake = mean_ela > 10.0 or max_ela > 40  # Max spike is a strong indicator
    confidence = min(95, (mean_ela / 20) * 100 + (max_ela / 50) * 10)
    if confidence > 95: confidence = 95
    
    # Build detailed forensic summary
    details = (
        f"📐 Dimensions: {w}x{h}px. "
        f"🔬 ELA Variance: {round(mean_ela, 2)} (Avg), {round(max_ela, 2)} (Peak). "
        f"📍 High-risk areas: {', '.join(high_risk_quadrants) if high_risk_quadrants else 'None detected'}. "
        f"{'⚠️ Digital manipulation strongly suspected.' if is_fake else '✅ Natural JPEG compression pattern.'}"
    )
    
    return {
        "verdict": "Fake" if is_fake else "Real",
        "confidence": round(confidence, 2),
        "color": "red" if is_fake else "green",
        "heatmap": heatmap_b64,
        "dimensions": f"{w} x {h}",
        "ela_stats": f"Avg: {round(mean_ela, 2)} | Peak: {round(max_ela, 2)} | Var: {round(var_ela, 2)}",
        "risk_areas": ", ".join(high_risk_quadrants) if high_risk_quadrants else "Uniform compression",
        "details": details
    }

# ---------- VIDEO PROCESSOR ----------
def process_video(file_bytes, filename):
    temp_video = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
            tmp.write(file_bytes)
            temp_video = tmp.name
        
        cap = cv2.VideoCapture(temp_video)
        if not cap.isOpened():
            raise ValueError("Could not open video")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0: fps = 30
        
        sample_indices = []
        if total_frames > 5:
            step = total_frames // 5
            sample_indices = [i * step for i in range(5)]
        else:
            sample_indices = [0, total_frames // 2, total_frames - 1]
            sample_indices = [i for i in sample_indices if i >= 0 and i < total_frames]
        
        frame_results = []
        confidence_scores = []
        
        for idx in sample_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if not ret:
                continue
            _, buffer = cv2.imencode('.jpg', frame)
            is_fake, conf, ela_val = run_ela_on_frame(buffer.tobytes())
            confidence_scores.append(conf)
            frame_results.append({
                "timestamp": f"{idx // fps:.1f}s",
                "ela_score": ela_val,
                "is_fake": is_fake
            })
        
        cap.release()
        os.unlink(temp_video)
        
        if not confidence_scores:
            return {"error": "No frames could be extracted"}
        
        avg_conf = np.mean(confidence_scores)
        variance = np.var(confidence_scores)
        temporal_risk = variance > 50
        
        is_fake = avg_conf > 30 or temporal_risk
        confidence = min(95, avg_conf + (variance / 5))
        
        timeline = [
            {"timestamp": f["timestamp"], "status": "Red" if f["is_fake"] else "Green", "label": f"ELA: {f['ela_score']}"} 
            for f in frame_results[:3]
        ]
        
        details = f"Analyzed {len(frame_results)} frames. Temporal variance: {round(variance, 2)}. {'🚨 Splicing detected (frames inconsistent)' if temporal_risk else '✅ Consistent compression across frames.'}"
        
        return {
            "verdict": "Fake (Spliced)" if is_fake else "Real",
            "confidence": round(confidence, 2),
            "color": "red" if is_fake else "green",
            "timeline": timeline,
            "details": details
        }
    except Exception as e:
        if temp_video and os.path.exists(temp_video):
            os.unlink(temp_video)
        return {"error": str(e)}

# ---------- AUDIO PROCESSOR ----------
def process_audio(file_bytes, filename):
    temp_audio = None
    try:
        if librosa is None:
            return {"error": "Librosa not installed."}
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            tmp.write(file_bytes)
            temp_audio = tmp.name
        
        y, sr = librosa.load(temp_audio, sr=16000, duration=10.0)
        if len(y) == 0:
            return {"error": "Empty audio file"}
        
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        centroid_variance = np.var(spectral_centroids)
        
        is_fake = centroid_variance < 500
        confidence = min(95, (100 - (centroid_variance / 100)) if centroid_variance < 1000 else 20)
        
        plt.figure(figsize=(6, 2))
        plt.plot(y[:min(len(y), 5000)])
        plt.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        waveform_b64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        os.unlink(temp_audio)
        
        details = f"Spectral Variance: {round(centroid_variance, 2)}. {'🤖 AI-generated voice detected (too uniform)' if is_fake else '🎤 Natural human voice variance detected.'}"
        
        return {
            "verdict": "Fake (Synthetic Voice)" if is_fake else "Real",
            "confidence": round(confidence, 2),
            "color": "red" if is_fake else "green",
            "waveform": waveform_b64,
            "details": details
        }
    except Exception as e:
        if temp_audio and os.path.exists(temp_audio):
            os.unlink(temp_audio)
        return {"error": f"Audio analysis failed: {str(e)}"}

# ---------- ENHANCED DOCUMENT PROCESSOR (CATCHES FAKES NOW) ----------
def process_document(file_bytes, filename):
    try:
        file_like = io.BytesIO(file_bytes)
        is_pdf = filename.lower().endswith('.pdf')
        is_docx = filename.lower().endswith('.docx')
        
        metadata = {}
        text_sample = ""
        warnings = []
        is_fake = False
        
        if is_pdf and PdfReader:
            reader = PdfReader(file_like)
            info = reader.metadata
            
            # Extract raw metadata
            if info:
                metadata = {
                    "Author": info.get('/Author', 'Not Set'),
                    "Creator": info.get('/Creator', 'Not Set'),
                    "Producer": info.get('/Producer', 'Not Set'),
                    "CreationDate": info.get('/CreationDate', 'Not Set'),
                    "ModDate": info.get('/ModDate', 'Not Set'),
                }
            else:
                metadata = {"Status": "No metadata found"}
                warnings.append("Missing metadata (often stripped by anonymizers).")
            
            # --- CRITICAL FAKE DETECTION LOGIC ---
            # 1. Check for Date Tampering (Modified before Created)
            if info and info.get('/CreationDate') and info.get('/ModDate'):
                try:
                    # Extract year from the date string (e.g., D:20251010...)
                    create_match = re.search(r'D:(\d{4})', info['/CreationDate'])
                    mod_match = re.search(r'D:(\d{4})', info['/ModDate'])
                    if create_match and mod_match:
                        create_year = int(create_match.group(1))
                        mod_year = int(mod_match.group(1))
                        current_year = datetime.datetime.now().year
                        
                        if mod_year < create_year:
                            warnings.append(f"🚨 MODIFIED DATE ({mod_year}) IS OLDER THAN CREATED DATE ({create_year}) - DEFINITE TAMPERING!")
                            is_fake = True
                        if create_year > current_year or mod_year > current_year:
                            warnings.append(f"🚨 DOCUMENT CLAIMS TO BE FROM THE FUTURE ({max(create_year, mod_year)}) - FORGED!")
                            is_fake = True
                except:
                    pass
            
            # 2. Tool Mismatch (Word vs Illustrator/Photoshop)
            if metadata.get('Creator') and metadata.get('Producer'):
                if "Microsoft" in metadata['Creator'] and "Illustrator" in metadata['Producer']:
                    warnings.append("🚨 Creator (Word) / Producer (Illustrator) mismatch - unlikely.")
                    is_fake = True
            
            # 3. Extract text
            if len(reader.pages) > 0:
                for page in reader.pages[:2]:
                    text_sample += page.extract_text() or ""
            
            # 4. Check if it's an "Empty" PDF with text metadata (often malicious)
            if len(text_sample.strip()) == 0 and metadata.get('Creator') not in ['Not Set', 'Unknown']:
                warnings.append("⚠️ Metadata exists but document contains zero extractable text (flattened/corrupted).")

        elif is_docx and Document:
            doc = Document(file_like)
            core_props = doc.core_properties
            metadata = {
                "Author": core_props.author or 'Not Set',
                "Created": str(core_props.created) if core_props.created else 'Not Set',
                "Modified": str(core_props.modified) if core_props.modified else 'Not Set',
                "Last Modified By": core_props.last_modified_by or 'Not Set'
            }
            
            if core_props.created and core_props.modified:
                if core_props.modified < core_props.created:
                    warnings.append("🚨 Modified date is BEFORE creation date - Tampering confirmed!")
                    is_fake = True
            
            for para in doc.paragraphs[:5]:
                text_sample += para.text + " "
        else:
            return {"error": "Unsupported or missing library."}
        
        # Set final verdict
        if is_fake:
            verdict = "Fake (Tampered)"
            color = "red"
            confidence = 92
        elif len(warnings) > 0:
            verdict = "Suspicious"
            color = "yellow"
            confidence = 65
        else:
            verdict = "Real"
            color = "green"
            confidence = 95
        
        details = f"Metadata: {metadata}. Findings: {', '.join(warnings) if warnings else '✅ All metadata consistent.'}"
        
        return {
            "verdict": verdict,
            "confidence": confidence,
            "color": color,
            "text_sample": text_sample[:200] + "..." if text_sample else "No text extracted.",
            "doc_warnings": warnings,
            "details": details
        }
    except Exception as e:
        return {"error": str(e)}

# ---------- MAIN ROUTER ----------
def process_file(file_bytes: bytes, filename: str, content_type: str):
    file_ext = filename.split('.')[-1].lower()
    
    if content_type.startswith("image/") or file_ext in ['jpg', 'jpeg', 'png', 'webp']:
        return process_image(file_bytes, filename)
    elif content_type.startswith("video/") or file_ext in ['mp4', 'mov', 'avi', 'mkv']:
        return process_video(file_bytes, filename)
    elif content_type.startswith("audio/") or file_ext in ['mp3', 'wav', 'm4a', 'aac']:
        return process_audio(file_bytes, filename)
    elif file_ext in ['pdf', 'docx']:
        return process_document(file_bytes, filename)
    else:
        return {"error": f"Unsupported file type: {file_ext}"}