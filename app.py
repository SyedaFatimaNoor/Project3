import streamlit as st
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        max-width: 1200px;
        padding: 2rem;
    }
    .book-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stats-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# File to store library data
LIBRARY_FILE = "library.json"

def load_library():
    """Load library data from file if it exists, otherwise return empty list."""
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            st.warning("Could not load library. Starting with an empty library.")
            return []
    return []

def save_library(library):
    """Save the library data to file."""
    try:
        with open(LIBRARY_FILE, 'w') as f:
            json.dump(library, f, indent=4)
    except IOError:
        st.error("Error: Could not save library to file.")

def add_book_ui():
    """Streamlit UI for adding a new book."""
    with st.expander("📖 Add a New Book", expanded=False):
        with st.form("add_book_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title*")
                author = st.text_input("Author*")
                year = st.number_input("Publication Year*", min_value=1, max_value=datetime.now().year, 
                                    value=datetime.now().year, step=1)
            with col2:
                genre = st.text_input("Genre", value="Unknown")
                read_status = st.radio("Read Status*", ["Read", "Unread"])
            
            submitted = st.form_submit_button("Add Book")
            
            if submitted:
                if not title or not author:
                    st.error("Title and Author are required fields!")
                    return None
                    
                book = {
                    'title': title,
                    'author': author,
                    'year': year,
                    'genre': genre,
                    'read': read_status == "Read"
                }
                return book
    return None

def remove_book_ui(library):
    """Streamlit UI for removing a book."""
    with st.expander("🗑️ Remove a Book", expanded=False):
        if not library:
            st.warning("The library is empty.")
            return
        
        # Create a selectbox with all books
        book_titles = [f"{book['title']} by {book['author']} ({book['year']})" for book in library]
        selected_title = st.selectbox("Select a book to remove:", [""] + book_titles)
        
        if selected_title and st.button("Remove Book"):
            # Find the index of the selected book
            index = book_titles.index(selected_title)
            removed_book = library.pop(index)
            save_library(library)
            st.success(f"✅ Removed: {removed_book['title']} by {removed_book['author']}")
            st.experimental_rerun()

def search_books_ui(library):
    """Streamlit UI for searching books."""
    with st.expander("🔍 Search Books", expanded=False):
        if not library:
            st.warning("The library is empty.")
            return
        
        search_type = st.radio("Search by:", ["Title", "Author", "Genre"])
        search_term = st.text_input(f"Enter {search_type} to search:")
        
        if search_term:
            search_field = search_type.lower()
            results = [book for book in library 
                     if search_term.lower() in book[search_field].lower()]
            
            if results:
                st.success(f"Found {len(results)} matching book(s):")
                for book in results:
                    status = "✅ Read" if book['read'] else "❌ Unread"
                    with st.container():
                        st.markdown(f"""
                        <div class="book-card">
                            <h4>{title}</h4>
                            <p>Author: {author} • Year: {year} • Genre: {genre} • {status}</p>
                        </div>
                        """.format(
                            title=book['title'],
                            author=book['author'],
                            year=book['year'],
                            genre=book['genre'],
                            status=status
                        ), unsafe_allow_html=True)
            else:
                st.info("No books found matching your search.")

def display_all_books_ui(library):
    """Streamlit UI for displaying all books."""
    st.subheader("📚 Your Library")
    
    if not library:
        st.info("Your library is empty. Add some books to get started!")
        return
    
    # Sort options
    sort_option = st.selectbox(
        "Sort by:",
        ["Title (A-Z)", "Author (A-Z)", "Year (Newest First)", "Year (Oldest First)"],
        key="sort_option"
    )
    
    # Apply sorting
    if sort_option == "Title (A-Z)":
        sorted_library = sorted(library, key=lambda x: x['title'].lower())
    elif sort_option == "Author (A-Z)":
        sorted_library = sorted(library, key=lambda x: (x['author'].lower(), x['title'].lower()))
    elif sort_option == "Year (Newest First)":
        sorted_library = sorted(library, key=lambda x: x['year'], reverse=True)
    else:  # Year (Oldest First)
        sorted_library = sorted(library, key=lambda x: x['year'])
    
    # Display books in a grid
    cols = st.columns(2)
    for i, book in enumerate(sorted_library):
        with cols[i % 2]:
            status = "✅ Read" if book['read'] else "❌ Unread"
            with st.container():
                st.markdown(f"""
                <div class="book-card">
                    <h4>{title}</h4>
                    <p><strong>Author:</strong> {author}</p>
                    <p><strong>Year:</strong> {year}</p>
                    <p><strong>Genre:</strong> {genre}</p>
                    <p>{status}</p>
                </div>
                """.format(
                    title=book['title'],
                    author=book['author'],
                    year=book['year'],
                    genre=book['genre'],
                    status=status
                ), unsafe_allow_html=True)

def display_statistics_ui(library):
    """Streamlit UI for displaying library statistics."""
    st.subheader("📊 Library Statistics")
    
    if not library:
        st.info("Your library is empty. Add some books to see statistics!")
        return
    
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Books", total_books)
    with col2:
        st.metric("Books Read", f"{read_books} ({percentage_read:.1f}%)")
    with col3:
        st.metric("Books Unread", total_books - read_books)
    
    # Genre distribution
    st.subheader("📚 Books by Genre")
    if library:
        genre_count = {}
        for book in library:
            genre = book['genre']
            genre_count[genre] = genre_count.get(genre, 0) + 1
        
        # Display as a bar chart
        st.bar_chart(genre_count)
        
        # Display as a table
        st.write("Genre Distribution:")
        for genre, count in sorted(genre_count.items()):
            st.write(f"- {genre}: {count} book{'s' if count > 1 else ''}")
    
    # Reading progress over years
    st.subheader("📅 Publication Years")
    if len(library) > 1:
        years = [book['year'] for book in library]
        min_year, max_year = min(years), max(years)
        st.write(f"Publication years range from {min_year} to {max_year}")
        
        # Create a histogram of publication years
        import pandas as pd
        df = pd.DataFrame({'Year': years})
        st.bar_chart(df['Year'].value_counts().sort_index())
    
    # Top authors
    st.subheader("🏆 Top Authors")
    if library:
        author_count = {}
        for book in library:
            author = book['author']
            author_count[author] = author_count.get(author, 0) + 1
        
        top_authors = sorted(author_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for author, count in top_authors:
            st.write(f"- {author}: {count} book{'s' if count > 1 else ''}")

def main():
    """Main function to run the Streamlit app."""
    st.title("📚 Personal Library Manager")
    
    # Initialize session state for the library if it doesn't exist
    if 'library' not in st.session_state:
        st.session_state.library = load_library()
    
    # Sidebar for navigation
    st.sidebar.title("Menu")
    menu_options = ["View Library", "Add Book", "Remove Book", "Search Books", "Statistics"]
    choice = st.sidebar.radio("Go to", menu_options)
    
    # Display the selected page
    if choice == "View Library":
        display_all_books_ui(st.session_state.library)
    elif choice == "Add Book":
        new_book = add_book_ui()
        if new_book:
            st.session_state.library.append(new_book)
            save_library(st.session_state.library)
            st.success(f"✅ Added '{new_book['title']}' to your library!")
            st.experimental_rerun()
    elif choice == "Remove Book":
        remove_book_ui(st.session_state.library)
    elif choice == "Search Books":
        search_books_ui(st.session_state.library)
    elif choice == "Statistics":
        display_statistics_ui(st.session_state.library)
    
    # Add some space at the bottom
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Tip: Add your favorite books to start building your personal library!")

if __name__ == "__main__":
    main()
