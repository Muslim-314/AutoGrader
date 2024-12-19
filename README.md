# AI Quiz Grader

AI Quiz Grader is a Python-based application that uses AI to grade handwritten quiz answers from image files. The application features a user-friendly graphical interface built with Tkinter, making it easy to upload quiz images, define the questions and ideal answers, and generate grades automatically.

## Features
- Upload a folder containing handwritten quiz answer images.
- Input quiz questions and ideal answers.
- Automatically grade answers using AI.
- Save results in an Excel file.

## Requirements

### Software
- Python 3.7 or higher
- Required libraries (listed in `requirements.txt`):
  - `tkinter`
  - `openai`
  - `openpyxl`
  - `python-dotenv`

### Hardware
- Internet connection to access the OpenAI API.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ai-quiz-grader.git
   cd ai-quiz-grader
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # For macOS/Linux
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key to the `.env` file:
     ```env
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

1. **Run the Application:**
   ```bash
   python main.py
   ```

2. **Use the GUI:**
   - Select a folder containing quiz images.
   - Input the quiz question and the ideal answer.
   - Click the `Start Grading` button to process the images.
   - Save the grading results to an Excel file.

## File Structure
```
.
├── main.py                # Main application code
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .env                   # Environment variables file (not included by default)
```

## Screenshots

Add screenshots of your GUI here to demonstrate the application interface.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- [OpenAI](https://openai.com/) for providing the AI API.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework.
