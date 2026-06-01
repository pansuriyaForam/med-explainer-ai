# 💊 Medicine Explainer - Complete System
 
A full-stack medicine search and information system built with **FastAPI** backend and **Streamlit** frontend. Users can search medicines by name, category, ingredient, and manufacturer, with detailed information about uses, side effects, and interactions.
 
## Features
 
✅ **Search Capabilities**
- Simple text search across medicine names, categories, and ingredients
- Advanced search with filters (name, category, manufacturer)
- Browse medicines by category
- Full SQLite database with indexing for fast queries
✅ **Medicine Information**
- Product name and manufacturer
- Salt composition/active ingredients
- Detailed description of uses
- Common side effects with warnings
- Drug interactions
- Pricing information
✅ **User Interface**
- Clean, responsive Streamlit web interface
- Multiple search methods (simple, category, advanced)
- Detailed medicine information pages
- Warning boxes for important medical information
- Error handling and loading states
✅ **Backend API**
- RESTful FastAPI endpoints
- Parameterized SQL queries (no SQL injection)
- CORS support for frontend integration
- Health check and validation endpoints
- Category management endpoints
## Project Structure
 
```
project/
│
├── app.py                          # Streamlit frontend
├── main.py                         # FastAPI backend
├── clean_data.py                   # Data cleaning script
├── create_db.py                    # Database creation script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── medicine_data.csv               # Original raw data (input)
├── cleaned_medicine_data.csv       # Cleaned data (generated)
├── medicines.db                    # SQLite database (generated)
│
└── docs/
    └── API_DOCUMENTATION.md        # API endpoints reference
```
 
## Prerequisites
 
- Python 3.8+
- pip (Python package manager)
- 2GB free disk space (for database)
## Installation
 
### Step 1: Clone or Extract Project
 
Extract the project files to your desired directory:
 
```bash
cd /path/to/medicine-explainer
```
 
### Step 2: Create Virtual Environment (Recommended)
 
```bash
# On Windows
python -m venv venv
venv\Scripts\activate
 
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
 
### Step 3: Install Dependencies
 
```bash
pip install -r requirements.txt
```
 
## Setup Instructions
 
### Step 1: Clean the Dataset
 
This removes duplicates, handles missing values, and standardizes the data:
 
```bash
python clean_data.py
```
 
**Expected Output:**
```
📋 Loading medicine data...
Initial records: 5000
Duplicates removed: 45
Final records: 4955
💾 Cleaned data saved to: cleaned_medicine_data.csv
```
 
### Step 2: Create Database
 
This creates SQLite database and indexes:
 
```bash
python create_db.py
```
 
**Expected Output:**
```
📦 Loading cleaned medicine data...
🗄️  Creating SQLite database: medicines.db
📝 Inserting medicine records...
✅ Records inserted: 4955
📊 Database Statistics:
Total medicines: 4955
Total categories: 120
✨ Database created successfully: medicines.db
```
 
### Step 3: Start FastAPI Backend
 
Open a new terminal and run:
 
```bash
uvicorn main:app --reload
```
 
**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```
 
✅ Backend is now running at: `http://127.0.0.1:8000`
 
### Step 4: Start Streamlit Frontend
 
Open another terminal and run:
 
```bash
python3 -m streamlit run app.py
```
 
**Expected Output:**
```
  You can now view your Streamlit app in your browser.
 
  URL: http://localhost:8501
```
 
✅ Frontend is now available at: `http://localhost:8501`
 
## Complete Startup Command (for reference)
 
```bash
# Terminal 1 - Data cleaning and database
python clean_data.py
python create_db.py
 
# Terminal 2 - FastAPI backend
uvicorn main:app --reload
 
# Terminal 3 - Streamlit frontend
python3 -m streamlit run app.py
```
 
## API Endpoints
 
### Health Check
```
GET /
Returns: API status and database connection info
```
 
### Search Medicines
```
GET /search?query=paracetamol
Returns: List of medicines matching the query
```
 
**Response Example:**
```json
{
  "total_results": 5,
  "medicines": [
    {
      "id": 1,
      "product_name": "Paracetamol 500mg",
      "sub_category": "Fever & Pain Relief",
      "salt_composition": "Paracetamol (500mg)",
      "product_price": "₹25",
      "product_manufactured": "Pfizer India",
      "medicine_desc": "Used to treat fever and mild pain...",
      "side_effects": "Generally well tolerated...",
      "drug_interactions": "No major interactions..."
    }
  ]
}
```
 
### Get Medicine Details
```
GET /medicine/{medicine_name}
Returns: Complete information for a specific medicine
```
 
### Browse Categories
```
GET /categories
Returns: All medicine categories with counts
```
 
### Get Medicines by Category
```
GET /category/{category_name}
Returns: All medicines in a specific category
```
 
### Advanced Search
```
GET /search/advanced?name=paracetamol&category=Fever&manufacturer=Pfizer&limit=50
Returns: Filtered medicines based on multiple criteria
```
 
## Data Cleaning Process
 
The `clean_data.py` script performs the following operations:
 
1. **Load CSV Data** - Reads medicine_data.csv
2. **Standardize Column Names** - Converts to lowercase snake_case
3. **Trim Whitespace** - Removes leading/trailing spaces
4. **Handle Missing Values** - Fills with appropriate defaults
5. **Clean Price Field** - Removes currency symbols
6. **Remove Duplicates** - Keeps first occurrence
7. **Text Normalization** - Applies title case
8. **Data Validation** - Verifies data integrity
9. **Export Cleaned Data** - Saves to cleaned_medicine_data.csv
## Database Schema
 
### medicines table
```sql
CREATE TABLE medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL UNIQUE,
    sub_category TEXT,
    salt_composition TEXT,
    product_price TEXT,
    product_manufactured TEXT,
    medicine_desc TEXT,
    side_effects TEXT,
    drug_interactions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
 
### Indexes Created:
- `idx_product_name` - On product_name
- `idx_sub_category` - On sub_category
- `idx_salt_composition` - On salt_composition
- `idx_product_name_search` - On product_name (NOCASE) for case-insensitive search
## Frontend Features
 
### Search Tab
- Simple text search
- Searches across product name, category, and ingredients
- Displays up to 100 results
- Quick view button for medicine details
### Categories Tab
- Browse all available categories
- View medicine count per category
- One-click access to category medicines
### Advanced Search Tab
- Filter by medicine name
- Filter by manufacturer
- Filter by category
- Adjustable result limit
## Troubleshooting
 
### "Database not found" Error
**Solution:** Run `python create_db.py` first
 
### "API Server Not Running" Warning
**Solution:** Start FastAPI backend with `uvicorn main:app --reload`
 
### Port Already in Use
**FastAPI (8000):**
```bash
uvicorn main:app --reload --port 8001
```
 
**Streamlit (8501):**
```bash
streamlit run app.py --server.port 8502
```
 
### Search Returns No Results
1. Check if database exists: `medicines.db` should exist
2. Verify database has data: Check output of `python create_db.py`
3. Try searching with partial names
## Performance Notes
 
- **Database Queries:** All queries use parameterized statements (SQL injection safe)
- **Indexes:** Created on frequently searched columns
- **Caching:** Streamlit caches API responses
- **Limit:** Advanced search limited to 200 results per query
- **Timeout:** API requests timeout after 10 seconds
## Development & Customization
 
### Adding More Medicines
1. Add rows to `medicine_data.csv`
2. Run `python clean_data.py`
3. Run `python create_db.py`
4. Restart the application
### Modifying Search Logic
Edit the search endpoints in `main.py`:
- Line 135: Simple search query
- Line 197: Advanced search filters
### Custom Styling
Edit CSS in `app.py` (lines 22-48) for custom colors and layouts
 
## Security Considerations
 
✅ **Implemented:**
- Parameterized SQL queries (prevents SQL injection)
- Input validation and length limits
- CORS configured for frontend access
- Proper error handling
- Database connection timeouts
⚠️ **For Production:**
- Add authentication/authorization
- Use environment variables for database path
- Enable HTTPS for API
- Set up rate limiting
- Use production WSGI server (Gunicorn)
## License
 
This project is provided as-is for educational purposes.
 
## Support
 
For issues or questions:
1. Check the API logs in terminal 2
2. Check Streamlit logs in terminal 3
3. Verify all files are in the correct directory
4. Ensure Python 3.8+ is installed
---
 
**Happy Medicine Searching! 💊**
 
