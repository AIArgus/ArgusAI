#!/usr/bin/env python3
"""
Test script to verify backend is working correctly
"""
import requests
import sys

def test_backend():
    """Test if backend is running and responding correctly"""
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("ArgusAI Backend Test")
    print("=" * 60)
    
    # Test 1: Check if backend is running
    print("\n1. Testing if backend is running...")
    try:
        response = requests.get(f"{base_url}/api/class-names", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend is running!")
            data = response.json()
            print(f"   ✅ Found {len(data.get('class_names', []))} classes")
        else:
            print(f"   ❌ Backend returned status code: {response.status_code}")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend!")
        print("   Please make sure backend is running:")
        print("   cd ArgusAI/AiArgus2/backend")
        print("   python main.py")
        sys.exit(1)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)
    
    # Test 2: Check available endpoints
    print("\n2. Testing available endpoints...")
    endpoints = [
        "/api/class-names",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint} - OK")
            else:
                print(f"   ⚠️  {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint} - Error: {e}")
    
    print("\n" + "=" * 60)
    print("Backend Test Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open your browser to http://localhost:5173")
    print("2. Upload an image in Object Detection mode")
    print("3. Check that bounding boxes use your selected color")
    print("4. Verify that NO segmentation masks appear in Detection mode")
    print("\n")

if __name__ == "__main__":
    test_backend()

