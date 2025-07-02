import tkinter as tk
from tkinter import filedialog, messagebox
import os
from utils import format_audio, convert_speech_to_text  # Updated imports

# Track selected file path
current_audio_file = None

def choose_file():
    global current_audio_file
    current_audio_file = filedialog.askopenfilename(
        title="Pick a WAV Audio File",
        filetypes=[("WAV Format", "*.wav"), ("All Files", "*.*")]
    )

    if current_audio_file:
        file_display = os.path.basename(current_audio_file)
        feedback_label.config(text=f"📁 Selected: {file_display}", fg="#0057b7")

        output_box.config(state='normal')
        output_box.delete("1.0", tk.END)
        output_box.config(state='disabled')

def run_transcription():
    global current_audio_file
    if not current_audio_file:
        messagebox.showwarning("No File", "Upload an audio file first!")
        return

    try:
        feedback_label.config(text="🔄 Transcribing... please wait.", fg="#333")
        window.update()

        processed = format_audio(current_audio_file)
        result_text = convert_speech_to_text(processed)

        output_box.config(state='normal')
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, result_text)
        output_box.config(state='disabled')

        feedback_label.config(text="✅ Transcription Complete!", fg="green")
    except Exception as error:
        messagebox.showerror("Error Occurred", str(error))
        feedback_label.config(text="❌ Transcription Failed", fg="red")

# GUI Initialization
window = tk.Tk()
window.title("🗣️ Smart Audio Transcriber")
window.geometry("700x520")
window.configure(bg="#fcfcfc")

# Heading
heading = tk.Label(window, text="Speech Recognition Engine", font=("Helvetica", 18, "bold"), bg="#fcfcfc", fg="#222")
heading.pack(pady=(20, 10))

# Frame container
frame = tk.Frame(window, bg="#fcfcfc")
frame.pack(padx=20, pady=10, fill="both", expand=True)

# Upload Button
upload_btn = tk.Button(
    frame, text="📤 Upload Audio", command=choose_file,
    font=("Helvetica", 12), bg="#0d6efd", fg="white",
    activebackground="#0b5ed7", padx=10, pady=5, relief="flat", cursor="hand2"
)
upload_btn.pack(pady=5)

# Transcribe Button
transcribe_btn = tk.Button(
    frame, text="📝 Generate Transcript", command=run_transcription,
    font=("Helvetica", 12), bg="#28a745", fg="white",
    activebackground="#218838", padx=10, pady=5, relief="flat", cursor="hand2"
)
transcribe_btn.pack(pady=5)

# Text Output Area
output_box = tk.Text(frame, wrap="word", height=10, font=("Helvetica", 11), padx=10, pady=10, relief="solid", bd=1)
output_box.pack(fill="both", expand=True, padx=10, pady=10)
output_box.config(state='disabled')

# Status Label
feedback_label = tk.Label(window, text="", font=("Helvetica", 10), bg="#fcfcfc", fg="#555")
feedback_label.pack(pady=6)

# Footer
footer_label = tk.Label(window, text="Developed by Yash Sharma", font=("Helvetica", 9), bg="#fcfcfc", fg="gray")
footer_label.pack(side="bottom", pady=10)

window.mainloop()
