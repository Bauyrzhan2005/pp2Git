import re

print("=== 5 Examples (Topics 2,3,4,5 combined) ===")

# Metacharacter (+)
print(re.findall(r"ca+t", "ct cat caaat"))  # ['cat', 'caaat']

# Special sequence (\d)
print(re.findall(r"\d+", "Order 123 Quantity 45"))  # ['123', '45']

# Character class ([A-Z])
print(re.findall(r"[A-Z]", "Hello World"))  # ['H', 'W']

# Quantifier ({2,3})
print(re.findall(r"\d{2,3}", "1234567"))  # ['123', '456']

# Combined example (date pattern)
print(re.search(r"\d{4}-\d{2}-\d{2}", "Date: 2026-02-27").group())  # 2026-02-27