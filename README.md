# 📚 Personal Library Manager

A modern, user-friendly web application built with Streamlit to manage your personal book collection. Track your reading progress, search your library, and get insights about your reading habits.

## ✨ Features

- **Add Books** with details like title, author, year, genre, and read status
- **Remove Books** from your collection
- **Search Books** by title, author, or genre
- **View Your Library** with sorting options
- **Statistics Dashboard** with visualizations:
  - Books read vs unread
  - Genre distribution
  - Publication year analysis
  - Top authors
- **Responsive Design** that works on desktop and mobile
- **Data Persistence** - Your library is saved automatically

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SyedaFatimaNoor/Project3.git
   cd Project3
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Navigate to the project directory:
   ```bash
   cd project3_streamlit
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. The application will open in your default web browser at `http://localhost:8501`

## 🖥️ Usage

### Adding a Book
1. Click on "Add Book" in the sidebar
2. Fill in the book details
3. Click "Add Book" to save

### Viewing Your Library
- Browse all your books in the "View Library" section
- Sort books by title, author, or publication year

### Searching for Books
- Use the search feature to find books by title, author, or genre
- Results are displayed in real-time as you type

### Viewing Statistics
- Check the "Statistics" section to see insights about your reading habits
- View charts showing your reading progress and genre distribution

## 📂 Project Structure

```
project3_streamlit/
├── app.py                # Main Streamlit application
├── personal_library_manager.py  # Core library management functions
├── library.json         # Database file (created after first run)
├── README.md           # This file
└── requirements.txt     # Python dependencies
```

## 📊 Technologies Used

- **Streamlit** - For building the web interface
- **Pandas** - For data manipulation and analysis
- **JSON** - For data storage
- **Python** - Backend programming language

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ for book lovers
- Inspired by the need for a simple, personal book tracking solution

---

<div align="center">
  Made with ❤️ by Syeda Noor ul-ain Fatima | 2025
</div>