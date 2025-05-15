import json
import os

# File to store library data
LIBRARY_FILE = "library.json"

def load_library():
    """Load library data from file if it exists, otherwise return empty list."""
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not load library. Starting with an empty library.")
            return []
    return []

def save_library(library):
    """Save the library data to file."""
    try:
        with open(LIBRARY_FILE, 'w') as f:
            json.dump(library, f, indent=4)
    except IOError:
        print("Error: Could not save library to file.")

def add_book(library):
    """Add a new book to the library."""
    print("\n=== Add a New Book ===")
    title = input("Enter the book title: ").strip()
    if not title:
        print("Error: Title cannot be empty.")
        return
    
    author = input("Enter the author: ").strip()
    if not author:
        print("Error: Author cannot be empty.")
        return
    
    while True:
        try:
            year = int(input("Enter the publication year: "))
            if year <= 0 or year > 2100:  # Basic validation for year
                print("Please enter a valid year between 1 and 2100.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for the year.")
    
    genre = input("Enter the genre (press Enter for 'Unknown'): ").strip() or "Unknown"
    
    while True:
        read_status = input("Have you read this book? (yes/no): ").strip().lower()
        if read_status in ['yes', 'y']:
            read = True
            break
        elif read_status in ['no', 'n']:
            read = False
            break
        else:
            print("Please enter 'yes' or 'no'.")
    
    book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read
    }
    
    library.append(book)
    save_library(library)
    print(f"\n✅ Book '{title}' added successfully!")

def remove_book(library):
    """Remove a book from the library by title."""
    print("\n=== Remove a Book ===")
    if not library:
        print("The library is empty.")
        return
    
    title = input("Enter the title of the book to remove: ").strip()
    found_books = [i for i, book in enumerate(library) 
                  if book['title'].lower() == title.lower()]
    
    if not found_books:
        print("❌ No book found with that title.")
        return
    
    if len(found_books) > 1:
        print("\nMultiple books found with that title:")
        for i, idx in enumerate(found_books, 1):
            book = library[idx]
            print(f"{i}. {book['title']} by {book['author']} ({book['year']})")
        
        while True:
            try:
                choice = int(input(f"\nEnter the number of the book to remove (1-{len(found_books)}), or 0 to cancel: "))
                if choice == 0:
                    print("Operation cancelled.")
                    return
                elif 1 <= choice <= len(found_books):
                    removed = library.pop(found_books[choice-1])
                    save_library(library)
                    print(f"\n✅ Removed: {removed['title']} by {removed['author']}")
                    return
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
    else:
        removed = library.pop(found_books[0])
        save_library(library)
        print(f"\n✅ Removed: {removed['title']} by {removed['author']}")

def search_books(library):
    """Search for books by title, author, or genre."""
    if not library:
        print("The library is empty.")
        return
    
    print("\n=== Search for a Book ===")
    print("1. Search by Title")
    print("2. Search by Author")
    print("3. Search by Genre")
    print("4. Back to Main Menu")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            if not choice:
                print("Please enter a choice.")
                continue
                
            choice = int(choice)
            if choice == 4:
                return
            elif 1 <= choice <= 3:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    search_terms = {
        1: "title",
        2: "author",
        3: "genre"
    }
    
    search_field = search_terms[choice]
    search_term = input(f"Enter the {search_field} to search for: ").strip().lower()
    
    if not search_term:
        print("Search term cannot be empty.")
        return
    
    results = []
    for book in library:
        if search_term in book[search_field].lower():
            results.append(book)
    
    if results:
        print(f"\n🔍 Found {len(results)} matching book(s):")
        for i, book in enumerate(results, 1):
            status = "✅ Read" if book['read'] else "❌ Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        print("\n❌ No books found matching your search.")

def display_all_books(library):
    """Display all books in the library."""
    print("\n=== Your Library ===")
    if not library:
        print("Your library is empty.")
        return
    
    # Sort books by title (case-insensitive)
    sorted_books = sorted(library, key=lambda x: x['title'].lower())
    
    for i, book in enumerate(sorted_books, 1):
        status = "✅ Read" if book['read'] else "❌ Unread"
        print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

def display_statistics(library):
    """Display library statistics."""
    print("\n=== Library Statistics ===")
    total_books = len(library)
    
    if total_books == 0:
        print("Your library is empty.")
        return
    
    read_books = sum(1 for book in library if book['read'])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    
    print(f"📚 Total books: {total_books}")
    print(f"✅ Books read: {read_books}")
    print(f"❌ Books unread: {total_books - read_books}")
    print(f"📊 Percentage read: {percentage_read:.1f}%")
    
    # Count books by genre
    genre_count = {}
    for book in library:
        genre = book['genre']
        genre_count[genre] = genre_count.get(genre, 0) + 1
    
    if genre_count:
        print("\n📂 Books by genre:")
        for genre, count in sorted(genre_count.items()):
            print(f"- {genre}: {count}")
    
    # Show reading progress by year
    if len(library) > 1:
        years = sorted(set(book['year'] for book in library))
        if len(years) > 1:
            print(f"\n📅 Publication years: {min(years)} - {max(years)}")
    
    # Show top authors
    author_count = {}
    for book in library:
        author = book['author']
        author_count[author] = author_count.get(author, 0) + 1
    
    if author_count:
        top_authors = sorted(author_count.items(), key=lambda x: x[1], reverse=True)[:3]
        print("\n🏆 Top authors:")
        for author, count in top_authors:
            print(f"- {author}: {count} book{'s' if count > 1 else ''}")

def main():
    """Main function to run the Personal Library Manager."""
    print("\n📚 Welcome to your Personal Library Manager! 📚")
    library = load_library()
    
    while True:
        print("\n=== Main Menu ===")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            if not choice:
                print("Please enter a choice.")
                continue
                
            choice = int(choice)
            
            if choice == 1:
                add_book(library)
            elif choice == 2:
                remove_book(library)
            elif choice == 3:
                search_books(library)
            elif choice == 4:
                display_all_books(library)
            elif choice == 5:
                display_statistics(library)
            elif choice == 6:
                print("\nSaving your library...")
                save_library(library)
                print("\nThank you for using the Personal Library Manager. Goodbye! 👋")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\nSaving your library before exit...")
            save_library(library)
            print("Goodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again or restart the program if the issue persists.")

if __name__ == "__main__":
    main()