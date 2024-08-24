import PyPDF2
import pdfplumber
import pyttsx3
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

def extract_text_pypdf2(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text with PyPDF2: {e}")
    return text

def extract_text_pdfplumber(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text with pdfplumber: {e}")
    return text

def extract_text(pdf_path, method='pdfplumber'):
    if method == 'pypdf2':
        return extract_text_pypdf2(pdf_path)
    elif method == 'pdfplumber':
        return extract_text_pdfplumber(pdf_path)
    else:
        raise ValueError("Invalid extraction method selected.")

def split_text_into_chunks(text, chunk_size=500):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

def text_to_speech_chunks(text, rate=150, volume=1.0, voice='female'):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    voices = engine.getProperty('voices')
    if voice == 'female' and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    else:
        engine.setProperty('voice', voices[0].id)
    
    for chunk in split_text_into_chunks(text):
        engine.say(chunk)
        engine.runAndWait()

def save_speech_to_file(text, output_path, rate=150, volume=1.0, voice='female'):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    voices = engine.getProperty('voices')
    if voice == 'female' and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    else:
        engine.setProperty('voice', voices[0].id)
    
    for i, chunk in enumerate(split_text_into_chunks(text)):
        engine.save_to_file(chunk, f"{output_path}_part_{i+1}.mp3")
    engine.runAndWait()

def select_pdf_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF Files", "*.pdf")]
    )
    return file_path

def main():
    pdf_path = select_pdf_file()
    if not pdf_path:
        messagebox.showerror("Error", "No file selected.")
        sys.exit()
    
    extraction_method = 'pdfplumber'  # or 'pypdf2'
    text = extract_text(pdf_path, method=extraction_method)
    
    if not text.strip():
        messagebox.showerror("Error", "No text found in PDF.")
        sys.exit()
    
    choice = messagebox.askquestion("Output Option", "Do you want to save the audio to a file?")
    
    if choice == 'yes':
        output_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3")],
            title="Save audio as"
        )
        if output_path:
            save_speech_to_file(text, output_path)
            messagebox.showinfo("Success", f"Audio saved to {output_path}")
        else:
            messagebox.showerror("Error", "No output file selected.")
    else:
        text_to_speech_chunks(text)
if __name__ == "__main__":
    main()
