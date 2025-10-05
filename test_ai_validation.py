#!/usr/bin/env python3
"""
Test AI Email Validation Enhancement
Verify the AI can detect and filter malformed emails
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from HYPERION import AIEngine

def test_ai_email_validation():
    """Test the enhanced AI email validation"""
    print("🤖 HYPERION v4.0 - AI Email Validation Test")
    print("=" * 60)
    
    ai = AIEngine()
    
    # Test cases: [email, should_be_valid]
    test_cases = [
        # Valid emails
        ("user@gmail.com", True),
        ("test.email@yahoo.com", True),
        ("valid_user@hotmail.com", True),
        ("user123@outlook.com", True),
        
        # Invalid emails - the type you mentioned
        ("qhjhjjhaviiiv@tvappagggency.comgg", False),  # Your example
        ("test@domain.comgg", False),  # Duplicate 'g's
        ("user@gimial.com", False),  # Typo of gmail
        ("bad@tvappagggency.com", False),  # Multiple g's
        
        # Other malformed patterns
        ("user@@domain.com", False),  # Double @
        ("user@domain@com", False),  # @ in domain
        ("user@", False),  # No domain
        ("@domain.com", False),  # No local part
        ("user@domain", False),  # No TLD
        ("user@domain.c", False),  # TLD too short
        ("user@domain.123", False),  # Numeric TLD
        ("user@domain.comm", False),  # Typo TLD
        ("user@12345678901234567890.com", False),  # Long number sequence
        ("user@aaaaaaaaaaaaaaaaaaaaaa.com", False),  # Extremely long word
        ("user@domain..com", False),  # Double dots
        ("user@domain.com.", False),  # Ending dot
        ("", False),  # Empty
        ("notanemail", False),  # No @
        ("user@192.168.1.1", False),  # IP address
    ]
    
    print("🧪 Testing email validation patterns...")
    print()
    
    passed = 0
    failed = 0
    
    for email, expected in test_cases:
        result = ai._is_valid_email(email)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
            
        expected_str = "VALID" if expected else "INVALID"
        result_str = "VALID" if result else "INVALID"
        
        print(f"{status} | {email:35} | Expected: {expected_str:7} | Got: {result_str:7}")
    
    print()
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎯 All tests passed! AI email validation is working perfectly.")
    else:
        print(f"⚠️ {failed} tests failed. AI validation needs adjustment.")
    
    # Test with a sample combo file
    print("\n" + "="*60)
    print("🗂️ Testing with sample combo data...")
    
    # Create a temporary test file
    test_combos = [
        "valid@gmail.com:password123",
        "qhjhjjhaviiiv@tvappagggency.comgg:badpass",  # Your example - should be filtered
        "test@domain.comgg:another_bad",  # Should be filtered
        "user@gimial.com:fake",  # Typo domain - should be filtered
        "good.user@yahoo.com:realpass",
        "@@invalid:test",  # Should be filtered
        "normal@hotmail.com:goodpass",
        "bad@domain@com.org:test",  # Should be filtered
    ]
    
    test_file = "test_combo_ai.txt"
    with open(test_file, 'w') as f:
        for combo in test_combos:
            f.write(combo + '\n')
    
    # Analyze with AI
    try:
        analysis = ai.analyze_combo(test_file)
        
        print(f"📋 Original lines: {analysis['original']}")
        print(f"✅ Valid after AI cleaning: {analysis['valid']}")
        print(f"❌ Invalid/filtered: {analysis['invalid']}")
        print(f"🧹 Duplicates removed: {analysis['duplicates']}")
        print(f"🎯 Quality score: {analysis['quality_score']}%")
        print(f"📊 Status: {analysis['status']}")
        
        print("\n🔍 Cleaned combo list:")
        for i, line in enumerate(analysis['cleaned_lines'], 1):
            email = line.split(':')[0]
            print(f"  {i}. {email}")
        
        # Verify the bad emails were filtered
        cleaned_emails = [line.split(':')[0] for line in analysis['cleaned_lines']]
        bad_email_filtered = "qhjhjjhaviiiv@tvappagggency.comgg" not in cleaned_emails
        
        if bad_email_filtered:
            print(f"\n✅ SUCCESS: Malformed email 'qhjhjjhaviiiv@tvappagggency.comgg' was filtered out!")
        else:
            print(f"\n❌ FAILED: Malformed email was not filtered!")
        
        # Cleanup
        os.remove(test_file)
        
    except Exception as e:
        print(f"⚠️ Test error: {e}")
        if os.path.exists(test_file):
            os.remove(test_file)
    
    print("\n✅ AI Email Validation Test Complete")

if __name__ == "__main__":
    test_ai_email_validation()