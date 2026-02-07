import json
import os
from datetime import datetime

# Database file
KB_FILE = "knowledge_base.json"

# Categories
CATEGORIES = [
    "Hardware",
    "Software",
    "Network",
    "Access",
    "Email",
    "Printer",
    "Other"
]

# Function to load knowledge base
def load_kb():
    """Load knowledge base from file"""
    if os.path.exists(KB_FILE):
        with open(KB_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to save knowledge base
def save_kb(articles):
    """Save knowledge base to file"""
    with open(KB_FILE, 'w') as f:
        json.dump(articles, f, indent=4)
    print("\nKnowledge base saved successfully!")

# Function to generate article ID
def generate_article_id(articles):
    """Generate unique article ID"""
    if not articles:
        return "KB001"
    
    last_id = max([int(article['article_id'][2:]) for article in articles])
    return f"KB{str(last_id + 1).zfill(3)}"

# Function to add new article
def add_article():
    """Add a new knowledge base article"""
    print("\n" + "="*70)
    print("ADD NEW KNOWLEDGE BASE ARTICLE")
    print("="*70)
    
    title = input("\nArticle Title: ").strip()
    
    if not title:
        print("\nERROR: Title is required!")
        return
    
    # Select category
    print("\nSelect Category:")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"{idx}. {cat}")
    
    try:
        cat_choice = int(input("\nCategory (1-7): "))
        if 1 <= cat_choice <= len(CATEGORIES):
            category = CATEGORIES[cat_choice - 1]
        else:
            print("\nInvalid category. Using 'Other'")
            category = "Other"
    except ValueError:
        print("\nInvalid input. Using 'Other'")
        category = "Other"
    
    print("\nProblem Description:")
    print("(Enter problem details. Press Enter twice when done)")
    problem_lines = []
    while True:
        line = input()
        if line == "":
            break
        problem_lines.append(line)
    
    problem = "\n".join(problem_lines)
    
    if not problem:
        print("\nERROR: Problem description is required!")
        return
    
    print("\nSolution:")
    print("(Enter solution steps. Press Enter twice when done)")
    solution_lines = []
    while True:
        line = input()
        if line == "":
            break
        solution_lines.append(line)
    
    solution = "\n".join(solution_lines)
    
    if not solution:
        print("\nERROR: Solution is required!")
        return
    
    tags_input = input("\nTags (comma-separated): ").strip()
    tags = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
    
    # Load existing articles
    articles = load_kb()
    article_id = generate_article_id(articles)
    
    # Create new article
    new_article = {
        'article_id': article_id,
        'title': title,
        'category': category,
        'problem': problem,
        'solution': solution,
        'tags': tags,
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'views': 0,
        'ratings': [],
        'avg_rating': 0
    }
    
    articles.append(new_article)
    save_kb(articles)
    
    print("\n" + "="*70)
    print("ARTICLE CREATED SUCCESSFULLY")
    print("="*70)
    print(f"Article ID: {article_id}")
    print(f"Title: {title}")
    print(f"Category: {category}")
    print(f"Tags: {', '.join(tags) if tags else 'None'}")
    print("="*70)

# Function to search articles
def search_articles():
    """Search knowledge base articles"""
    articles = load_kb()
    
    if not articles:
        print("\nNo articles in knowledge base.")
        return
    
    print("\n--- Search Knowledge Base ---")
    search_term = input("Enter search term: ").strip().lower()
    
    if not search_term:
        print("\nNo search term entered.")
        return
    
    results = []
    
    for article in articles:
        # Search in title, problem, solution, and tags
        if (search_term in article['title'].lower() or
            search_term in article['problem'].lower() or
            search_term in article['solution'].lower() or
            any(search_term in tag for tag in article['tags'])):
            results.append(article)
    
    if not results:
        print(f"\nNo articles found matching '{search_term}'")
        return
    
    print(f"\nFound {len(results)} article(s):")
    print("="*80)
    
    for article in results:
        print(f"\nID: {article['article_id']}")
        print(f"Title: {article['title']}")
        print(f"Category: {article['category']}")
        print(f"Tags: {', '.join(article['tags']) if article['tags'] else 'None'}")
        print(f"Views: {article['views']} | Rating: {article['avg_rating']:.1f}/5.0")
        print("-"*80)
    
    # Option to view full article
    view_choice = input("\nView full article? Enter ID (or press Enter to skip): ").strip()
    
    if view_choice:
        view_article_by_id(view_choice)
        
# Function to browse by category
def browse_by_category():
    """Browse articles by category"""
    articles = load_kb()
    
    if not articles:
        print("\nNo articles in knowledge base.")
        return
    
    print("\n--- Browse by Category ---")
    print("\nCategories:")
    for idx, cat in enumerate(CATEGORIES, 1):
        count = len([a for a in articles if a['category'] == cat])
        print(f"{idx}. {cat} ({count} articles)")
    
    try:
        choice = int(input("\nSelect category (1-7): "))
        if 1 <= choice <= len(CATEGORIES):
            category = CATEGORIES[choice - 1]
        else:
            print("\nInvalid selection!")
            return
    except ValueError:
        print("\nInvalid input!")
        return
    
    # Filter articles by category
    filtered = [a for a in articles if a['category'] == category]
    
    if not filtered:
        print(f"\nNo articles found in category '{category}'")
        return
    
    print(f"\n{category} Articles ({len(filtered)}):")
    print("="*80)
    
    for article in filtered:
        print(f"\nID: {article['article_id']}")
        print(f"Title: {article['title']}")
        print(f"Tags: {', '.join(article['tags']) if article['tags'] else 'None'}")
        print(f"Views: {article['views']} | Rating: {article['avg_rating']:.1f}/5.0")
        print("-"*80)
    
    # Option to view full article
    view_choice = input("\nView full article? Enter ID (or press Enter to skip): ").strip()
    
    if view_choice:
        view_article_by_id(view_choice)

# Function to view article by ID
def view_article_by_id(article_id):
    """View full article details"""
    articles = load_kb()
    
    article = None
    for a in articles:
        if a['article_id'].upper() == article_id.upper():
            article = a
            break
    
    if not article:
        print(f"\nArticle '{article_id}' not found.")
        return
    
    # Increment view count
    article['views'] += 1
    save_kb(articles)
    
    # Display article
    print("\n" + "="*80)
    print(f"ARTICLE: {article['article_id']}")
    print("="*80)
    print(f"\nTitle: {article['title']}")
    print(f"Category: {article['category']}")
    print(f"Tags: {', '.join(article['tags']) if article['tags'] else 'None'}")
    print(f"Created: {article['created_date']}")
    print(f"Views: {article['views']}")
    print(f"Rating: {article['avg_rating']:.1f}/5.0 ({len(article['ratings'])} ratings)")
    
    print("\n" + "-"*80)
    print("PROBLEM:")
    print("-"*80)
    print(article['problem'])
    
    print("\n" + "-"*80)
    print("SOLUTION:")
    print("-"*80)
    print(article['solution'])
    
    print("\n" + "="*80)
    
    # Option to rate
    rate = input("\nRate this article? (y/n): ").strip().lower()
    if rate == 'y':
        rate_article(article['article_id'])

# Function to view article details
def view_article():
    """View specific article by ID"""
    articles = load_kb()
    
    if not articles:
        print("\nNo articles in knowledge base.")
        return
    
    print("\n--- View Article ---")
    article_id = input("Enter Article ID: ").strip()
    
    view_article_by_id(article_id)

# Function to rate article
def rate_article(article_id):
    """Rate an article's helpfulness"""
    articles = load_kb()
    
    article = None
    for a in articles:
        if a['article_id'].upper() == article_id.upper():
            article = a
            break
    
    if not article:
        print(f"\nArticle '{article_id}' not found.")
        return
    
    try:
        rating = int(input("\nRate this article (1-5): "))
        
        if rating < 1 or rating > 5:
            print("\nInvalid rating. Must be 1-5.")
            return
        
        article['ratings'].append(rating)
        article['avg_rating'] = sum(article['ratings']) / len(article['ratings'])
        
        save_kb(articles)
        
        print(f"\nThank you! Article rated {rating}/5")
        print(f"New average rating: {article['avg_rating']:.1f}/5.0")
    
    except ValueError:
        print("\nInvalid input!")

# Function to view popular articles
def view_popular_articles():
    """View most viewed and highest rated articles"""
    articles = load_kb()
    
    if not articles:
        print("\nNo articles in knowledge base.")
        return
    
    print("\n" + "="*80)
    print("POPULAR ARTICLES")
    print("="*80)
    
    # Most viewed
    most_viewed = sorted(articles, key=lambda x: x['views'], reverse=True)[:5]
    
    print("\nMost Viewed Articles:")
    print("-"*80)
    for idx, article in enumerate(most_viewed, 1):
        print(f"{idx}. {article['title']} ({article['article_id']})")
        print(f"   Views: {article['views']} | Category: {article['category']}")
    
    # Highest rated (with at least 1 rating)
    rated_articles = [a for a in articles if len(a['ratings']) > 0]
    
    if rated_articles:
        highest_rated = sorted(rated_articles, key=lambda x: x['avg_rating'], reverse=True)[:5]
        
        print("\nHighest Rated Articles:")
        print("-"*80)
        for idx, article in enumerate(highest_rated, 1):
            print(f"{idx}. {article['title']} ({article['article_id']})")
            print(f"   Rating: {article['avg_rating']:.1f}/5.0 ({len(article['ratings'])} ratings)")
    
    print("="*80)
    
# Function to view statistics
def view_statistics():
    """View knowledge base statistics"""
    articles = load_kb()
    
    if not articles:
        print("\nNo articles in knowledge base.")
        return
    
    print("\n" + "="*80)
    print("KNOWLEDGE BASE STATISTICS")
    print("="*80)
    
    print(f"\nTotal Articles: {len(articles)}")
    
    # Category breakdown
    print("\nArticles by Category:")
    for cat in CATEGORIES:
        count = len([a for a in articles if a['category'] == cat])
        print(f"  {cat}: {count}")
    
    # Total views
    total_views = sum(a['views'] for a in articles)
    print(f"\nTotal Views: {total_views}")
    
    # Average rating
    rated = [a for a in articles if len(a['ratings']) > 0]
    if rated:
        avg_rating = sum(a['avg_rating'] for a in rated) / len(rated)
        print(f"Average Rating: {avg_rating:.1f}/5.0")
        print(f"Rated Articles: {len(rated)}/{len(articles)}")
    
    # Recent articles
    recent = sorted(articles, key=lambda x: x['created_date'], reverse=True)[:5]
    
    print("\nRecently Added:")
    for article in recent:
        print(f"  {article['article_id']}: {article['title']} ({article['created_date'][:10]})")
    
    print("="*80)

# Function to list all articles
def list_all_articles():
    """List all articles in knowledge base"""
    articles = load_kb()
    
    if not articles:
        print("\nNo articles in knowledge base.")
        return
    
    print("\n" + "="*80)
    print(f"ALL ARTICLES ({len(articles)} total)")
    print("="*80)
    
    # Sort by ID
    sorted_articles = sorted(articles, key=lambda x: x['article_id'])
    
    for article in sorted_articles:
        print(f"\n{article['article_id']}: {article['title']}")
        print(f"  Category: {article['category']} | Views: {article['views']} | Rating: {article['avg_rating']:.1f}/5.0")
        print(f"  Tags: {', '.join(article['tags']) if article['tags'] else 'None'}")
        print("-"*80)

# Function to delete article
def delete_article():
    """Delete an article from knowledge base"""
    articles = load_kb()
    
    if not articles:
        print("\nNo articles in knowledge base.")
        return
    
    print("\n--- Delete Article ---")
    article_id = input("Enter Article ID to delete: ").strip()
    
    article = None
    for a in articles:
        if a['article_id'].upper() == article_id.upper():
            article = a
            break
    
    if not article:
        print(f"\nArticle '{article_id}' not found.")
        return
    
    print(f"\nArticle: {article['title']}")
    confirm = input("Are you sure you want to delete this article? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        articles.remove(article)
        save_kb(articles)
        print(f"\nArticle '{article_id}' deleted successfully!")
    else:
        print("\nDeletion cancelled.")

# Function to export knowledge base
def export_kb():
    """Export knowledge base to backup file"""
    articles = load_kb()
    
    if not articles:
        print("\nNo articles to export.")
        return
    
    filename = f"kb_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(articles, f, indent=4)
        
        print(f"\nSUCCESS: Knowledge base exported to {filename}")
        print(f"Total articles exported: {len(articles)}")
    except Exception as e:
        print(f"\nERROR: Failed to export - {str(e)}")

# Function to import knowledge base
def import_kb():
    """Import knowledge base from backup file"""
    print("\n--- Import Knowledge Base ---")
    filename = input("Enter backup file name: ").strip()
    
    if not os.path.exists(filename):
        print(f"\nERROR: File '{filename}' not found!")
        return
    
    try:
        with open(filename, 'r') as f:
            imported = json.load(f)
        
        if not isinstance(imported, list):
            print("\nERROR: Invalid backup file format!")
            return
        
        articles = load_kb()
        
        added = 0
        skipped = 0
        
        for article in imported:
            # Check if article already exists
            if any(a['article_id'] == article['article_id'] for a in articles):
                print(f"SKIPPED: {article['article_id']} (already exists)")
                skipped += 1
            else:
                articles.append(article)
                print(f"ADDED: {article['article_id']} - {article['title']}")
                added += 1
        
        save_kb(articles)
        
        print(f"\nImport complete!")
        print(f"Added: {added}")
        print(f"Skipped: {skipped}")
    
    except Exception as e:
        print(f"\nERROR: Failed to import - {str(e)}")

# Main menu
def show_menu():
    print("\n" + "="*70)
    print("  IT SUPPORT KNOWLEDGE BASE SYSTEM")
    print("="*70)
    print("1.  Add New Article")
    print("2.  Search Articles")
    print("3.  Browse by Category")
    print("4.  View Article")
    print("5.  View Popular Articles")
    print("6.  View Statistics")
    print("7.  List All Articles")
    print("8.  Delete Article")
    print("9.  Export Knowledge Base")
    print("10. Import Knowledge Base")
    print("11. Exit")
    print("-"*70)

# Main program
def main():
    while True:
        show_menu()
        choice = input("\nSelect an option (1-11): ").strip()
        
        if choice == '1':
            add_article()
        
        elif choice == '2':
            search_articles()
        
        elif choice == '3':
            browse_by_category()
        
        elif choice == '4':
            view_article()
        
        elif choice == '5':
            view_popular_articles()
        
        elif choice == '6':
            view_statistics()
        
        elif choice == '7':
            list_all_articles()
        
        elif choice == '8':
            delete_article()
        
        elif choice == '9':
            export_kb()
        
        elif choice == '10':
            import_kb()
        
        elif choice == '11':
            print("\nThank you for using the Knowledge Base System!")
            print("Exiting...\n")
            break
        
        else:
            print("\nInvalid option. Please select 1-11.")
        
        if choice != '11':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()