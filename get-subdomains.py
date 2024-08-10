import dns.resolver

def get_subdomains(domain):
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        subdomains = set()
        for rdata in answers:
            ns_domain = rdata.target.to_text()
            print(f"Found nameserver: {ns_domain}")

            # Query for additional A or AAAA records for discovered nameservers
            try:
                a_records = dns.resolver.resolve(ns_domain, 'A')
                for a in a_records:
                    print(f"Subdomain resolved: {a.to_text()}")
                    subdomains.add(a.to_text())
            except dns.resolver.NoAnswer:
                pass
        return subdomains
    except Exception as e:
        print(f"Error: {e}")
        return set()

# Replace with your domain
domain = 'meet.google.com'
subdomains = get_subdomains(domain)
print(f"Discovered subdomains: {subdomains}")
