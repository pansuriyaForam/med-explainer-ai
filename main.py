from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Medicine Explainer API",
    description="Complete medicine search and information system",
    version="1.0.0"
)

# Add CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DATABASE = 'medicines.db'

# Pydantic models for request/response
class MedicineSearchRequest(BaseModel):
    query: str

class MedicineResponse(BaseModel):
    id: int
    product_name: str
    sub_category: str
    salt_composition: str
    product_price: str
    product_manufactured: str
    medicine_desc: str
    side_effects: str
    drug_interactions: str

class SearchResultsResponse(BaseModel):
    total_results: int
    medicines: List[MedicineResponse]


def get_db_connection():
    """Create a database connection"""
    if not os.path.exists(DATABASE):
        raise HTTPException(
            status_code=500,
            detail=f"Database not found. Run 'python create_db.py' first."
        )
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def format_medicine_response(row):
    """Convert database row to MedicineResponse"""
    return MedicineResponse(
        id=row['id'],
        product_name=row['product_name'],
        sub_category=row['sub_category'],
        salt_composition=row['salt_composition'],
        product_price=row['product_price'],
        product_manufactured=row['product_manufactured'],
        medicine_desc=row['medicine_desc'],
        side_effects=row['side_effects'],
        drug_interactions=row['drug_interactions']
    )


# Health check endpoint
@app.get("/")
def health_check():
    """Check if API is running and database is connected"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM medicines")
        count = cursor.fetchone()[0]
        conn.close()
        
        return {
            "status": "running",
            "message": "Medicine Explainer API is operational",
            "database": "connected",
            "medicines_in_db": count
        }
    except Exception as e:
        return {
            "status": "running",
            "message": "Medicine Explainer API is running",
            "database": "error",
            "error": str(e)
        }


# Search endpoint
@app.get("/search", response_model=SearchResultsResponse)
def search_medicines(query: str = Query(..., min_length=1, max_length=100)):
    """
    Search for medicines by name, category, or composition.
    
    Parameters:
    - query: Search term (medicine name, category, or ingredient)
    
    Returns:
    - List of matching medicines with their details
    """
    
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Search across product_name, sub_category, and salt_composition
        search_pattern = f"%{query}%"
        
        cursor.execute('''
            SELECT * FROM medicines
            WHERE product_name LIKE ? 
               OR sub_category LIKE ? 
               OR salt_composition LIKE ?
            ORDER BY product_name ASC
            LIMIT 100
        ''', (search_pattern, search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return SearchResultsResponse(
                total_results=0,
                medicines=[]
            )
        
        medicines = [format_medicine_response(row) for row in rows]
        
        return SearchResultsResponse(
            total_results=len(medicines),
            medicines=medicines
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


# Medicine details endpoint
@app.get("/medicine/{medicine_name}", response_model=MedicineResponse)
def get_medicine_details(medicine_name: str):
    """
    Get complete details for a specific medicine.
    
    Parameters:
    - medicine_name: Exact name of the medicine
    
    Returns:
    - Complete medicine information
    """
    
    if not medicine_name.strip():
        raise HTTPException(status_code=400, detail="Medicine name cannot be empty")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Search for exact match (case-insensitive)
        cursor.execute('''
            SELECT * FROM medicines
            WHERE LOWER(product_name) = LOWER(?)
            LIMIT 1
        ''', (medicine_name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(
                status_code=404,
                detail=f"Medicine '{medicine_name}' not found"
            )
        
        return format_medicine_response(row)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Category search endpoint
@app.get("/categories")
def get_categories():
    """Get all medicine categories"""
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT sub_category, COUNT(*) as count
            FROM medicines
            GROUP BY sub_category
            ORDER BY count DESC
        ''')
        
        categories = [
            {"name": row[0], "count": row[1]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            "total_categories": len(categories),
            "categories": categories
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")


# Category-specific search endpoint
@app.get("/category/{category_name}", response_model=SearchResultsResponse)
def get_medicines_by_category(category_name: str):
    """Get all medicines in a specific category"""
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM medicines
            WHERE LOWER(sub_category) = LOWER(?)
            ORDER BY product_name ASC
        ''', (category_name,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No medicines found in category '{category_name}'"
            )
        
        medicines = [format_medicine_response(row) for row in rows]
        
        return SearchResultsResponse(
            total_results=len(medicines),
            medicines=medicines
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Advanced search endpoint
@app.get("/search/advanced")
def advanced_search(
    name: Optional[str] = Query(None, max_length=100),
    category: Optional[str] = Query(None, max_length=100),
    manufacturer: Optional[str] = Query(None, max_length=100),
    limit: int = Query(50, ge=1, le=200)
):
    """
    Advanced search with multiple filters.
    
    Parameters:
    - name: Medicine name (partial match)
    - category: Medicine category
    - manufacturer: Manufacturer name
    - limit: Maximum results (1-200)
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic query
        query = "SELECT * FROM medicines WHERE 1=1"
        params = []
        
        if name:
            query += " AND product_name LIKE ?"
            params.append(f"%{name}%")
        
        if category:
            query += " AND LOWER(sub_category) = LOWER(?)"
            params.append(category)
        
        if manufacturer:
            query += " AND product_manufactured LIKE ?"
            params.append(f"%{manufacturer}%")
        
        query += " ORDER BY product_name ASC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        medicines = [format_medicine_response(row) for row in rows]
        
        return SearchResultsResponse(
            total_results=len(medicines),
            medicines=medicines
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
