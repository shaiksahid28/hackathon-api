from flask import Flask, request, jsonify
import os
import re
import math
from datetime import datetime, date

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running"})

@app.route('/v1/answer', methods=['POST'])
def answer():
    data = request.json
    query = data.get('query', '')
    ql = query.lower().strip()

    # ── NUMBER LIST OPERATIONS ──────────────────────────────
    num_match = re.search(r'numbers?[:\s]+([\d\s,;|]+)', ql)
    if num_match:
        nums = [int(x) for x in re.findall(r'\d+', num_match.group(1))]
        if nums:
            if 'sum' in ql and 'even' in ql:
                return jsonify({"output": str(sum(n for n in nums if n % 2 == 0))})
            if 'sum' in ql and 'odd' in ql:
                return jsonify({"output": str(sum(n for n in nums if n % 2 != 0))})
            if ('count' in ql or 'how many' in ql) and 'even' in ql:
                return jsonify({"output": str(len([n for n in nums if n % 2 == 0]))})
            if ('count' in ql or 'how many' in ql) and 'odd' in ql:
                return jsonify({"output": str(len([n for n in nums if n % 2 != 0]))})
            if 'second largest' in ql:
                return jsonify({"output": str(sorted(set(nums))[-2])})
            if 'second smallest' in ql:
                return jsonify({"output": str(sorted(set(nums))[1])})
            if 'largest' in ql or 'maximum' in ql or 'max' in ql or 'greatest' in ql:
                return jsonify({"output": str(max(nums))})
            if 'smallest' in ql or 'minimum' in ql or 'min' in ql:
                return jsonify({"output": str(min(nums))})
            if 'range' in ql:
                return jsonify({"output": str(max(nums) - min(nums))})
            if 'median' in ql:
                s = sorted(nums)
                n = len(s)
                mid = n // 2
                result = s[mid] if n % 2 != 0 else (s[mid-1] + s[mid]) / 2
                return jsonify({"output": str(int(result) if result == int(result) else round(result, 2))})
            if 'average' in ql or 'mean' in ql:
                result = sum(nums) / len(nums)
                return jsonify({"output": str(int(result) if result == int(result) else round(result, 2))})
            if 'sort' in ql and ('desc' in ql or 'reverse' in ql or 'descending' in ql):
                return jsonify({"output": ' '.join(map(str, sorted(nums, reverse=True)))})
            if 'sort' in ql or 'ascending' in ql:
                return jsonify({"output": ' '.join(map(str, sorted(nums)))})
            if 'multiply' in ql or 'product' in ql:
                result = 1
                for n in nums: result *= n
                return jsonify({"output": str(result)})
            if 'sum' in ql or 'total' in ql or 'add' in ql:
                return jsonify({"output": str(sum(nums))})
            if 'count' in ql or 'how many' in ql:
                return jsonify({"output": str(len(nums))})

    # ── ODD / EVEN ─────────────────────────────────────────
    if 'odd' in ql or 'even' in ql:
        nums = re.findall(r'\d+', ql)
        if nums:
            num = int(nums[0])
            is_odd = num % 2 != 0
            if 'odd' in ql and 'even' in ql:
                return jsonify({"output": "Odd" if is_odd else "Even"})
            if 'odd' in ql:
                return jsonify({"output": "YES" if is_odd else "NO"})
            if 'even' in ql:
                return jsonify({"output": "YES" if not is_odd else "NO"})

    # ── PRIME ──────────────────────────────────────────────
    if 'prime' in ql:
        nums = re.findall(r'\d+', ql)
        if nums:
            num = int(nums[0])
            is_prime = num > 1 and all(num % i != 0 for i in range(2, int(num**0.5)+1))
            return jsonify({"output": "YES" if is_prime else "NO"})

    # ── FIZZBUZZ ───────────────────────────────────────────
    if 'fizzbuzz' in ql or 'fizz buzz' in ql:
        nums = re.findall(r'\d+', ql)
        if nums:
            n = int(nums[0])
            if n % 15 == 0: return jsonify({"output": "FizzBuzz"})
            if n % 3 == 0:  return jsonify({"output": "Fizz"})
            if n % 5 == 0:  return jsonify({"output": "Buzz"})
            return jsonify({"output": str(n)})

    # ── MATH OPERATIONS ────────────────────────────────────
    m = re.search(r'square root of (\d+)', ql)
    if m:
        result = math.sqrt(int(m.group(1)))
        return jsonify({"output": str(int(result) if result == int(result) else round(result, 4))})

    m = re.search(r'(\d+)\s*(?:\^|\*\*|to the power of)\s*(\d+)', ql)
    if m:
        return jsonify({"output": str(int(m.group(1)) ** int(m.group(2)))})

    m = re.search(r'factorial of (\d+)', ql)
    if m:
        return jsonify({"output": str(math.factorial(int(m.group(1))))})

    m = re.search(r'(\d+)\s*\+\s*(\d+)', query)
    if m:
        return jsonify({"output": str(int(m.group(1)) + int(m.group(2)))})

    m = re.search(r'(\d+)\s*-\s*(\d+)', query)
    if m:
        return jsonify({"output": str(int(m.group(1)) - int(m.group(2)))})

    m = re.search(r'(\d+)\s*[x*×]\s*(\d+)', query)
    if m:
        return jsonify({"output": str(int(m.group(1)) * int(m.group(2)))})

    m = re.search(r'(\d+)\s*/\s*(\d+)', query)
    if m and int(m.group(2)) != 0:
        result = int(m.group(1)) / int(m.group(2))
        return jsonify({"output": str(int(result) if result == int(result) else round(result, 2))})

    m = re.search(r'(\d+)\s*%\s*(\d+)', query)
    if m:
        return jsonify({"output": str(int(m.group(1)) % int(m.group(2)))})

    # ── GCD / LCM ──────────────────────────────────────────
    if 'gcd' in ql or 'greatest common' in ql:
        nums = re.findall(r'\d+', ql)
        if len(nums) >= 2:
            return jsonify({"output": str(math.gcd(int(nums[0]), int(nums[1])))})

    if 'lcm' in ql or 'least common multiple' in ql:
        nums = re.findall(r'\d+', ql)
        if len(nums) >= 2:
            a, b = int(nums[0]), int(nums[1])
            return jsonify({"output": str(abs(a * b) // math.gcd(a, b))})

    # ── ABSOLUTE VALUE ─────────────────────────────────────
    if 'absolute' in ql or 'abs(' in ql:
        nums = re.findall(r'-?\d+', query)
        if nums:
            return jsonify({"output": str(abs(int(nums[0])))})

    # ── CELSIUS / FAHRENHEIT ───────────────────────────────
    m = re.search(r'(-?\d+(?:\.\d+)?)\s*(?:celsius|°c|c)\s*to\s*(?:fahrenheit|°f|f)', ql)
    if m:
        c = float(m.group(1))
        result = (c * 9/5) + 32
        return jsonify({"output": str(int(result) if result == int(result) else round(result, 2))})

    m = re.search(r'(-?\d+(?:\.\d+)?)\s*(?:fahrenheit|°f|f)\s*to\s*(?:celsius|°c|c)', ql)
    if m:
        f = float(m.group(1))
        result = (f - 32) * 5/9
        return jsonify({"output": str(int(result) if result == int(result) else round(result, 2))})

    # ── DATES ──────────────────────────────────────────────
    m = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', query, re.IGNORECASE)
    if m:
        return jsonify({"output": f"{m.group(1)} {m.group(2).capitalize()} {m.group(3)}"})

    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})', query, re.IGNORECASE)
    if m:
        return jsonify({"output": f"{m.group(2)} {m.group(1).capitalize()} {m.group(3)}"})

    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', query)
    if m:
        try:
            dt = datetime.strptime(f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "%Y-%m-%d")
            return jsonify({"output": dt.strftime("%-d %B %Y")})
        except:
            pass

    # Day of week
    m = re.search(r'day.*?(\d{4})-(\d{2})-(\d{2})', ql)
    if m:
        try:
            dt = datetime.strptime(f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "%Y-%m-%d")
            return jsonify({"output": dt.strftime("%A")})
        except:
            pass

    # ── STRING OPERATIONS ──────────────────────────────────
    m = re.search(r'reverse (?:the )?(?:word |string )?["\']?([a-zA-Z0-9]+)["\']?', ql)
    if m:
        return jsonify({"output": m.group(1)[::-1]})

    m = re.search(r'(?:count )?vowels? in ["\']?([a-zA-Z]+)["\']?', ql)
    if m:
        return jsonify({"output": str(sum(1 for c in m.group(1).lower() if c in 'aeiou'))})

    m = re.search(r'length of ["\']?([a-zA-Z0-9]+)["\']?', ql)
    if m:
        return jsonify({"output": str(len(m.group(1)))})

    m = re.search(r'uppercase of ["\']?([a-zA-Z]+)["\']?', ql)
    if m:
        return jsonify({"output": m.group(1).upper()})

    m = re.search(r'lowercase of ["\']?([a-zA-Z]+)["\']?', ql)
    if m:
        return jsonify({"output": m.group(1).lower()})

    # ── BOOLEAN LOGIC ──────────────────────────────────────
    if 'true and true' in ql:   return jsonify({"output": "True"})
    if 'true and false' in ql:  return jsonify({"output": "False"})
    if 'false and true' in ql:  return jsonify({"output": "False"})
    if 'false and false' in ql: return jsonify({"output": "False"})
    if 'true or false' in ql:   return jsonify({"output": "True"})
    if 'false or true' in ql:   return jsonify({"output": "True"})
    if 'true or true' in ql:    return jsonify({"output": "True"})
    if 'false or false' in ql:  return jsonify({"output": "False"})
    if 'not true' in ql:        return jsonify({"output": "False"})
    if 'not false' in ql:       return jsonify({"output": "True"})

    # ── ROMAN NUMERALS ─────────────────────────────────────
    roman_map = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    m = re.search(r'roman numeral.*?([IVXLCDM]+)', query, re.IGNORECASE)
    if m:
        s = m.group(1).upper()
        result = 0
        for i in range(len(s)):
            if i+1 < len(s) and roman_map.get(s[i], 0) < roman_map.get(s[i+1], 0):
                result -= roman_map.get(s[i], 0)
            else:
                result += roman_map.get(s[i], 0)
        return jsonify({"output": str(result)})

    # ── FIBONACCI ──────────────────────────────────────────
    if 'fibonacci' in ql:
        nums = re.findall(r'\d+', ql)
        if nums:
            n = int(nums[0])
            a, b = 0, 1
            for _ in range(n - 1):
                a, b = b, a + b
            return jsonify({"output": str(a)})

    return jsonify({"output": "I don't know."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
