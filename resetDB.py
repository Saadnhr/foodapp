"""
Database Reset Script - Windows Compatible
Run this to recreate the database with new schema
WARNING: This will delete all existing data!
"""
import os
import sys
import time
from app import app, db

def reset_database():
    """Remove old database and create new one with updated schema"""
    with app.app_context():
        # Get database path
        db_path = os.path.join(app.root_path, 'database', 'foodapp.db')
        
        # Remove old database if it exists
        if os.path.exists(db_path):
            print(f"Removing old database: {db_path}")
            
            # Try to close any existing connections
            try:
                db.session.remove()
                db.engine.dispose()
            except:
                pass
            
            # Wait a moment for connections to close
            time.sleep(1)
            
            # Try to remove the file
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    os.remove(db_path)
                    print("✅ Old database removed successfully")
                    break
                except PermissionError:
                    if attempt < max_attempts - 1:
                        print(f"⚠️  Database is locked. Waiting... (attempt {attempt + 1}/{max_attempts})")
                        time.sleep(2)
                    else:
                        print("\n❌ ERROR: Cannot delete database file.")
                        print("\nThe database is being used by another process.")
                        print("\nPlease:")
                        print("1. Close any database browsers (DB Browser for SQLite, etc.)")
                        print("2. Stop any running Flask app instances")
                        print("3. Close any Python shells that might have imported the app")
                        print("4. Try running this script again")
                        print("\nOR use the alternative method:")
                        print("1. Manually delete: database\\foodapp.db")
                        print("2. Run: python app.py (it will create a new database)")
                        sys.exit(1)
        
        # Create database directory
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Create all tables with new schema
        print("Creating new database with updated schema...")
        db.create_all()
        
        print("✅ Database reset complete!")
        print(f"New database created at: {db_path}")
        print("\nYou can now run the application:")
        print("  python app.py")

if __name__ == '__main__':
    print("=" * 60)
    print("DATABASE RESET SCRIPT")
    print("=" * 60)
    print("\n⚠️  WARNING: This will DELETE all existing data!")
    print("This includes:")
    print("  - All user accounts")
    print("  - All donations")
    print("  - All claims and history")
    print("\n" + "=" * 60)
    
    response = input("\nContinue with database reset? (yes/no): ")
    
    if response.lower() == 'yes':
        reset_database()
    else:
        print("\n✋ Database reset cancelled.")