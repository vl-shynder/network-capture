import subprocess

def find_subdomains(domain):
    try:
        # Run sublist3r command to find subdomains
        result = subprocess.run(['sublist3r', '-d', domain, '-o', 'subdomains.txt'], capture_output=True, text=True)
        with open('subdomains.txt', 'r') as file:
            subdomains = file.read().splitlines()
        return subdomains
    except Exception as e:
        print(f"Error: {e}")
        return []

# Example usage
domain = 'google.com'
subdomains = find_subdomains(domain)
print(f"Discovered subdomains: {subdomains}")
