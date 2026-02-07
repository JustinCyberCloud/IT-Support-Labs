# Lab 8: Knowledge Base with Search

## Description
A comprehensive IT support knowledge base system with search functionality. Store, organize, and quickly find solutions to common IT issues. Perfect for building institutional knowledge and reducing resolution times.

## Features
- **Article Management**: Create, edit, and delete knowledge base articles
- **Category Organization**: Organize articles by category (Hardware, Software, Network, etc.)
- **Search Functionality**: Search by keywords, category, or tags
- **Solution Tracking**: Track which solutions work best
- **View Statistics**: See most viewed articles and popular categories
- **Rating System**: Rate article helpfulness
- **Export/Import**: Backup and restore knowledge base
- **Recent Articles**: Quick access to recently added solutions

## Requirements
- Python 3.7 or higher
- No external libraries required (uses standard library)

## How to Run

1. Run the program:
python knowledge_base.py


## Usage Examples

### Add a New Article
- Select option 1
- Enter title, category, problem description, and solution
- Add tags for better searchability
- Article saved to knowledge base

### Search Articles
- Select option 2
- Enter search term (searches title, problem, solution, tags)
- View matching articles with full details

### Browse by Category
- Select option 3
- Choose category (Hardware, Software, Network, etc.)
- See all articles in that category

### View Article Details
- Select option 4
- Enter article ID
- See full problem description and solution
- Rate the article's helpfulness

### Popular Articles
- Select option 5
- See most viewed and highest rated articles
- Identify your best solutions

## Article Structure

Each article includes:
- **Article ID**: Unique identifier (KB001, KB002, etc.)
- **Title**: Brief description of the issue
- **Category**: Hardware, Software, Network, Access, Email, Printer, Other
- **Problem**: Detailed problem description
- **Solution**: Step-by-step resolution
- **Tags**: Keywords for search (e.g., "password", "vpn", "outlook")
- **Created Date**: When article was added
- **Views**: Number of times viewed
- **Rating**: Average helpfulness rating

## Common Use Cases
- Document recurring issues and solutions
- Reduce ticket resolution time
- Train new help desk staff
- Build institutional knowledge
- Self-service portal content
- Troubleshooting reference
- Best practices documentation

## Sample Articles

**Example 1: Password Reset**
- Category: Access
- Problem: User forgot password and cannot log in
- Solution: Use password reset tool, verify identity, generate temporary password
- Tags: password, login, access, account

**Example 2: Printer Offline**
- Category: Printer
- Problem: Network printer shows as offline
- Solution: Check network connection, restart print spooler, re-add printer
- Tags: printer, offline, network, printing

## Skills Demonstrated
- Knowledge management systems
- Search algorithms and filtering
- Data organization and categorization
- Content management
- User interface design
- Documentation best practices
- IT support methodology