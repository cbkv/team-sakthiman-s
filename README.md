# Adobe Hackathon Round 1A – PDF Heading Extractor

## 📝 Description
This tool extracts structured outlines from PDF files using rule-based heuristics and lightweight classification logic.

## 🚀 How to Run

### Local:
```bash
pip install -r requirements.txt
python main.py
```

### Docker:
```bash
docker build --platform linux/amd64 -t heading-extractor:1a .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none heading-extractor:1a
```

## 📂 Folder Structure
- `input/`: Place your `.pdf` files here
- `output/`: Output `.json` files will be generated here
