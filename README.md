# AI-based-Medical-transcription-analysis-and-prediction

# Physician Notetaker

## 📌 Overview
This project is a **Physician Notetaker** application that leverages **Natural Language Processing (NLP)** to extract medical entities, generate SOAP notes, summarize conversations, and analyze sentiments from physician-patient dialogues.

## 🚀 Features
- **Medical Entity Extraction:** Identifies symptoms, diagnosis, treatment, and prognosis using SpaCy's `en_core_sci_md` model.
- **Text Summarization:** Uses `facebook/bart-large-cnn` transformer model to summarize conversations.
- **Sentiment Analysis:** Determines if the patient's tone is "Anxious" or "Reassured" using TextBlob.
- **SOAP Note Generation:** Automatically structures patient interactions into Subjective, Objective, Assessment, and Plan format.
- **Streamlit UI:** Provides an interactive web interface.

---

## 🛠 Installation & Setup

### 1️⃣ Install Dependencies
Ensure you have Python installed. Then, install the required libraries:
```bash
pip install --pre torch torchvision torchaudio -i https://download.pytorch.org/whl/nightly/cu118
pip install spacy transformers textblob streamlit
```

### 2️⃣ Download the Biomedical NLP Model
Download the `en_core_sci_md` model from [SciSpaCy](https://allenai.github.io/scispacy/):
```bash
pip install "path_to_downloaded_file"
```

### 3️⃣ Run the Application
```bash
streamlit run app.py
```

---

## 🔍 Methodologies Used

### 1️⃣ **Medical Entity Extraction**
- **Model Used:** `en_core_sci_md` (SciSpaCy)
- **Approach:** Identifies and categorizes entities such as symptoms, diagnosis, treatments, etc.

### 2️⃣ **Text Summarization**
- **Model Used:** `facebook/bart-large-cnn`
- **Approach:** Summarizes long physician-patient dialogues into concise text.

### 3️⃣ **Sentiment Analysis**
- **Library Used:** TextBlob
- **Approach:** Determines sentiment polarity and classifies it as "Anxious" or "Reassured."

### 4️⃣ **SOAP Note Generation**
- **Custom implementation:** Converts extracted entities into a structured SOAP note format.

---


- **Live Demo (if applicable):** https://drive.google.com/file/d/1Q30wE9wIcv0MmXwEaaptb6alkksf-GYM/view?usp=sharing

---

## 🤝 Contributors
Developed by **Syed Abdul Kareem Ahmed** as an assignment for **Emitrr**.

