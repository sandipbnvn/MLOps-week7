import requests
import json
import time

# Configuration
BASE_URL = "http://34.66.9.111"
HEADERS = {"Content-Type": "application/json"}

# Test data
VALID_DATA = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}

INVALID_DATA = {
    "sepal_length": "invalid",
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}

def test_endpoint(url, method="GET", data=None, expected_status=200, description=""):
    """Test an endpoint and return results"""
    print(f"\n🧪 Testing: {description}")
    print(f"URL: {url}")
    print(f"Method: {method}")
    
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=HEADERS, timeout=10)
        
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        print(f"Status Code: {response.status_code}")
        print(f"Latency: {latency:.2f} ms")
        
        if response.status_code == expected_status:
            print("✅ PASS")
            if response.content:
                try:
                    print(f"Response: {json.dumps(response.json(), indent=2)}")
                except:
                    print(f"Response: {response.text}")
        else:
            print(f"❌ FAIL - Expected {expected_status}, got {response.status_code}")
            print(f"Response: {response.text}")
            
        return response.status_code == expected_status, latency
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        return False, 0

def main():
    print("🚀 Starting Iris API Endpoint Tests")
    print("=" * 50)
    
    results = []
    
    # Test 1: Root endpoint
    success, latency = test_endpoint(
        f"{BASE_URL}/",
        method="GET",
        expected_status=200,
        description="Root endpoint"
    )
    results.append(("Root", success, latency))
    
    # Test 2: Health check
    success, latency = test_endpoint(
        f"{BASE_URL}/health",
        method="GET",
        expected_status=200,
        description="Health check endpoint"
    )
    results.append(("Health", success, latency))
    
    # Test 3: Liveness probe
    success, latency = test_endpoint(
        f"{BASE_URL}/live_check",
        method="GET",
        expected_status=200,
        description="Liveness probe endpoint"
    )
    results.append(("Liveness", success, latency))
    
    # Test 4: Readiness probe
    success, latency = test_endpoint(
        f"{BASE_URL}/ready_check",
        method="GET",
        expected_status=200,
        description="Readiness probe endpoint"
    )
    results.append(("Readiness", success, latency))
    
    # Test 5: Valid prediction
    success, latency = test_endpoint(
        f"{BASE_URL}/predict/",
        method="POST",
        data=VALID_DATA,
        expected_status=200,
        description="Valid prediction request"
    )
    results.append(("Valid Prediction", success, latency))
    
    # Test 6: Invalid prediction (should fail)
    success, latency = test_endpoint(
        f"{BASE_URL}/predict/",
        method="POST",
        data=INVALID_DATA,
        expected_status=422,  # Validation error
        description="Invalid prediction request (validation error expected)"
    )
    results.append(("Invalid Prediction", success, latency))
    
    # Test 7: Missing data prediction
    success, latency = test_endpoint(
        f"{BASE_URL}/predict/",
        method="POST",
        data={},
        expected_status=422,  # Validation error
        description="Missing data prediction request (validation error expected)"
    )
    results.append(("Missing Data", success, latency))
    
    # Test 8: Non-existent endpoint
    success, latency = test_endpoint(
        f"{BASE_URL}/nonexistent",
        method="GET",
        expected_status=404,
        description="Non-existent endpoint (404 expected)"
    )
    results.append(("404 Test", success, latency))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    total_latency = 0
    
    for test_name, success, latency in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<20} {status:<10} {latency:>8.2f} ms")
        if success:
            passed += 1
        total_latency += latency
    
    print("-" * 50)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    if passed > 0:
        print(f"Average Latency: {total_latency/passed:.2f} ms")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 