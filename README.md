#  Prescription Explainer AI
Intelligent Medical Instruction Interpreter

A lightweight AI-powered web application that transforms complex medical prescriptions into clear, patient-friendly instructions.

This tool is designed to reduce confusion caused by medical abbreviations and handwritten prescriptions by converting them into structured, easy-to-understand guidance.

# Overview

Medical prescriptions often contain shorthand such as:

OD (Once Daily)

BD (Twice Daily)

TDS (Three Times Daily)

SOS (If Needed)

AC (Before Food)

PC (After Food)

HS (At Bedtime)

For many patients, these terms are unclear and can lead to incorrect dosage timing.

Prescription Explainer AI interprets these instructions and presents them in simple language with structured output.

# Core Features

# Text-based prescription parsing

# Image upload support with OCR extraction

# Medical abbreviation interpretation engine

# Structured breakdown of:

Medicine name

Dosage

Frequency

Timing

Duration

# Privacy-focused design (local processing only)

# System Architecture

The application is divided into two main layers:

Backend

FastAPI-based API server

Prescription parsing logic

Abbreviation interpretation module

OCR processing integration

Frontend

Minimal and responsive interface

Tailwind CSS for styling

Vanilla JavaScript for API communication

# Tech Stack

Backend

Python 3.9+

FastAPI

Tesseract OCR

Frontend

HTML5

Tailwind CSS

Vanilla JavaScript

# Prerequisites

Before running the project, ensure:

Python 3.9 or higher is installed

Tesseract OCR is installed and added to your system PATH

Tesseract installation:
https://github.com/tesseract-ocr/tesseract

For Windows users, verify installation path:

C:\Program Files\Tesseract-OCR\tesseract.exe
# Installation Guide
1️⃣ Clone the Repository
git clone https://github.com/Rithish-2914/Prescription_Analyzer
cd Prescription_Analyzer
2️⃣ Backend Setup
cd backend
pip install python-multipart
uvicorn main:app --reload

Backend will start at:

http://127.0.0.1:8000
3️⃣ Frontend Setup

In a new terminal:

cd frontend
python -m http.server 8080

Open in browser:

http://localhost:8080
# Example Use Case

Input:

Paracetamol 500mg TDS PC for 5 days

Output:

Take Paracetamol 500mg

Three times daily

After meals

For 5 days

# Medical Disclaimer

This application is an AI-based informational assistant.

It does not replace professional medical advice, diagnosis, or treatment.
Always consult a qualified healthcare professional regarding medications and prescriptions.

# Author

Developed by Bajjuri Rithish
GitHub: https://github.com/Rithish-2914
