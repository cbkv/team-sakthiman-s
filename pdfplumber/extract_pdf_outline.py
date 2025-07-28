import pdfplumber
import os
import json
from collections import Counter
from pathlib import Path

def extract_title_and_outline(pdf_path):
    outline = []
    font_counter = Counter()
    font_map = {}  # Map font size to list of (text, page_number)

    with pdfplumber.open(pdf_path) as pdf:
        # --- Collect font sizes ---
        for i, page in enumerate(pdf.pages):
            for obj in page.extract_words(extra_attrs=["size"]):
                size = round(obj["size"], 1)
                text = obj["text"].strip()
                if text:
                    font_counter[size] += 1
                    font_map.setdefault(size, []).append((text, i + 1))

        # --- Determine title ---
        largest_font_size = max(font_counter.keys())
        title_candidates = font_map[largest_font_size]
        title_lines = [text for text, pg in title_candidates if pg == 1]
        title = " ".join(title_lines).strip()

        # --- Determine H1, H2, H3 thresholds ---
        common_sizes = sorted(font_counter.keys(), reverse=True)
        h1_size = common_sizes[0] if len(common_sizes) > 0 else None
        h2_size = common_sizes[1] if len(common_sizes) > 1 else None
        h3_size = common_sizes[2] if len(common_sizes) > 2 else None

        seen = set()

        for i, page in enumerate(pdf.pages):
            for obj in page.extract_words(extra_attrs=["size"]):
                text = obj["text"].strip()
                size = round(obj["size"], 1)
                page_num = i + 1

                if not text or (page_num, text) in seen:
                    continue
                seen.add((page_num, text))

                if size == h1_size and text not in title_lines:
                    outline.append({"level": "H1", "text": text, "page": page_num})
                elif size == h2_size:
                    outline.append({"level": "H2", "text": text, "page": page_num})
                elif size == h3_size:
                    outline.append({"level": "H3", "text": text, "page": page_num})

    return {
        "title": title,
        "outline": outline
    }


# --- Main runner ---
def process_all_pdfs(input_dir="./input", output_dir="./output"):
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            json_path = os.path.join(output_dir, Path(file).stem + ".json")
            result = extract_title_and_outline(pdf_path)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"[✓] Saved: {json_path}")

# --- Entry point ---
if __name__ == "__main__":
    process_all_pdfs()
