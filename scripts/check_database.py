#!/usr/bin/env python3
"""
Script to check database and API keys functionality
"""
import sys
import os
from pathlib import Path
from sqlalchemy import text

# Add the API directory to the path
sys.path.append(str(Path(__file__).parent.parent / "apps" / "api"))

def check_database():
    """Check database connection and tables"""
    try:
        from app.db.session import engine, SessionLocal
        from app.models.api_keys import APIKey
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection: OK")
        
        # Test table creation
        from app.db.base import Base
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables: OK")
        
        # Test session
        db = SessionLocal()
        try:
            # Test query
            keys = db.query(APIKey).all()
            print(f"✅ Database query: OK ({len(keys)} keys found)")
        finally:
            db.close()
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_encryption():
    """Check encryption functionality"""
    try:
        from app.core.crypto import secret_box
        
        # Test encryption/decryption
        test_data = "test_api_key_123"
        encrypted = secret_box.encrypt(test_data)
        decrypted = secret_box.decrypt(encrypted)
        
        if decrypted == test_data:
            print("✅ Encryption: OK")
            return True
        else:
            print("❌ Encryption: Failed - data mismatch")
            return False
    except Exception as e:
        print(f"❌ Encryption error: {e}")
        return False

def check_api_keys():
    """Check API key service"""
    try:
        from app.services.api_key_service import save_api_key, get_all_api_keys, delete_api_key
        from app.db.session import SessionLocal
        
        db = SessionLocal()
        try:
            # Test save
            test_key = save_api_key(db, "test_provider", "test_key_123")
            print("✅ API key save: OK")
            
            # Test get
            keys = get_all_api_keys(db)
            if "test_provider" in keys and keys["test_provider"] == "test_key_123":
                print("✅ API key get: OK")
            else:
                print("❌ API key get: Failed")
                return False
            
            # Test delete
            success = delete_api_key(db, "test_provider")
            if success:
                print("✅ API key delete: OK")
            else:
                print("❌ API key delete: Failed")
                return False
            
            return True
        finally:
            db.close()
    except Exception as e:
        print(f"❌ API key service error: {e}")
        return False

def main():
    """Run all checks"""
    print("🔍 Checking Database and API Keys...")
    print("=" * 50)
    
    checks = [
        ("Database", check_database),
        ("Encryption", check_encryption),
        ("API Keys", check_api_keys),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if check_func():
            passed += 1
        else:
            print(f"❌ {name} check failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Summary: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed!")
        return True
    else:
        print("⚠️  Some checks failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)