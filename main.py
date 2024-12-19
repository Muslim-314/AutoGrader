import os
import base64
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from openpyxl import Workbook
from dotenv import load_dotenv
from openai import OpenAI

API_KEY = "xai-tbX7zzmXbkoboPNcxPqu43lYkS2cnyJQHVPzhoF49bkgmjAW9vpmdWRewXtibElwoNS2mwQgzwIht8H4"

# Load environment variables
load_dotenv()

class QuizGraderApp:
    def __init__(self, root):
        """Initialize the Quiz Grader Application"""
        self.root = root
        self.root.title("Quiz Grader")
        self.root.geometry("1100x1000")
        self.root.configure(bg="#2c3e50")

        # Initialize OpenAI Client
        try:
            self.client = OpenAI(
                api_key=API_KEY, base_url="https://api.x.ai/v1"
            )
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to initialize API client: {e}")
            return

        self.create_widgets()

    def create_widgets(self):
        """Create and layout application widgets"""
        # Title
        tk.Label(self.root, text="AI Quiz Grader", font=("Helvetica", 20, "bold"), bg="#34495e", fg="white").pack(pady=20)

        # Folder Selection
        folder_frame = tk.Frame(self.root, bg="#2c3e50")
        folder_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(folder_frame, text="Select Folder with Quiz Images:", font=("Helvetica", 12,"bold"), bg="#2c3e50", fg="white").pack(side=tk.LEFT)
        self.folder_entry = tk.Entry(folder_frame, width=50, font=("Helvetica", 12))
        self.folder_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=10)

        tk.Button(folder_frame, text="Browse", command=self.browse_folder, font=("Helvetica", 12), bg="#1abc9c", fg="white").pack(side=tk.LEFT)

        # Question Input
        tk.Label(self.root, text="Enter Quiz Question:", font=("Helvetica", 14), bg="#2c3e50", fg="white").pack(anchor='w', padx=20)
        self.question_text = scrolledtext.ScrolledText(self.root, height=5, width=70, wrap=tk.WORD, font=("Helvetica", 12), bg="#ecf0f1")
        self.question_text.pack(padx=20, pady=10)

        # Ideal Answer Input
        tk.Label(self.root, text="Enter Ideal Answer:", font=("Helvetica", 14), bg="#2c3e50", fg="white").pack(anchor='w', padx=20)
        self.answer_text = scrolledtext.ScrolledText(self.root, height=5, width=70, wrap=tk.WORD, font=("Helvetica", 12), bg="#ecf0f1")
        self.answer_text.pack(padx=20, pady=10)

        # Grade Button
        tk.Button(self.root, text="Start Grading", command=self.start_grading, 
                  bg="#e74c3c", fg="white", font=("Helvetica", 14, "bold"), width=20).pack(pady=20)

        # Results Text Area
        tk.Label(self.root, text="Grading Results:", font=("Helvetica", 14), bg="#2c3e50", fg="white").pack(anchor='w', padx=20)
        self.results_text = scrolledtext.ScrolledText(self.root, height=10, width=70, wrap=tk.WORD, font=("Helvetica", 12), bg="#ecf0f1")
        self.results_text.pack(padx=20, pady=10)
        self.results_text.config(state=tk.DISABLED)

    def browse_folder(self):
        """Open folder selection dialog"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)

    def start_grading(self):
        """Start the grading process in a separate thread"""
        # Reset results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        # Validate inputs
        folder_path = self.folder_entry.get()
        question = self.question_text.get(1.0, tk.END).strip()
        ideal_answer = self.answer_text.get(1.0, tk.END).strip()

        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        if not question or not ideal_answer:
            messagebox.showerror("Error", "Please enter both question and ideal answer.")
            return

        # Disable grade button during processing
        self.root.config(cursor="wait")

        # Start grading in a thread
        threading.Thread(target=self.process_quiz_files, 
                         args=(folder_path, question, ideal_answer), 
                         daemon=True).start()

    def process_quiz_files(self, folder_path, question, ideal_answer):
        """Process image files and grade them"""
        supported_extensions = ('.png', '.jpg', '.jpeg', '.gif')
        scores = []

        try:
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(supported_extensions):
                    file_path = os.path.join(folder_path, filename)

                    try:
                        with open(file_path, "rb") as image_file:
                            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

                        # Grade the imagex
                        response = self.client.chat.completions.create(
                            model="grok-vision-beta",
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are a science teacher grading a student's handwritten answer. "
                                               "Return only a numeric score out of 10. If the answer is correct then return 10."
                                },
                                {"role": "user", "content": [
                                    {"type": "text", "text": f"Question: {question}\nIdeal Answer: {ideal_answer}"},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]}
                            ],
                            max_tokens=1500
                        )

                        # Extract score
                        result = response.choices[0].message.content.strip()
                        scores.append((filename, result))

                    except Exception as e:
                        scores.append((filename, f"Grading Error: {str(e)}"))

            # Save results to Excel
            self.save_to_excel(scores)

            # Update results in main thread
            self.root.after(0, self.display_results, scores)

        except Exception as e:
            messagebox.showerror("Processing Error", str(e))
        finally:
            self.root.after(0, self.reset_ui)

    def save_to_excel(self, scores):
        """Save grading results to an Excel file"""
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Quiz Results"

        # Adding headers
        sheet.append(["Quiz Name", "Grade"])

        # Adding results
        for filename, grade in scores:
            sheet.append([filename, grade])

        # Save to excel file
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if save_path:
            workbook.save(save_path)
            messagebox.showinfo("Success", f"Results saved to {save_path}")

    def display_results(self, scores):
        """Display grading results"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        for filename, result in scores:
            self.results_text.insert(tk.END, f"{filename}: {result}\n\n")

        self.results_text.config(state=tk.DISABLED)

    def reset_ui(self):
        """Reset UI after processing"""
        self.root.config(cursor="")


def main():
    root = tk.Tk()
    app = QuizGraderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
