#!/usr/bin/env python3
"""Test chatbot with various inputs"""
import requests

tests = [
    ("wheat", "✅ Single word: plant name"),
    ("drought", "✅ Single word: trait"),
    ("sorghum", "✅ Single word: plant"),
    ("g", "✅ Random letter"),
    ("blé", "✅ French: wheat"),
    ("meilleur pour sécheresse", "✅ French: best for drought"),
    ("قمح", "✅ Arabic: wheat"),
    ("أفضل", "✅ Arabic: best"),
    ("ranking sorghum", "✅ English phrase"),
    ("compare wheat barley", "✅ Comparison"),
]

print("\n" + "="*60)
print("CHATBOT MULTI-LANGUAGE & SINGLE-WORD TEST")
print("="*60)

for msg, desc in tests:
    try:
        r = requests.post('http://localhost:5001/api/chat', 
                         json={'message': msg}, 
                         timeout=3)
        data = r.json()
        
        print(f"\n{desc}")
        print(f"Input: '{msg}'")
        print(f"Output: {data['response'][:150]}...")
        print("-" * 60)
    except Exception as e:
        print(f"\n❌ Error testing '{msg}': {e}")
        print("-" * 60)

print("\n✅ Testing complete!\n")
