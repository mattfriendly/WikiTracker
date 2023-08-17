import dns.resolver

def resolve_domain(domain):
    resolver = dns.resolver.Resolver()
    try:
        resolved_ips = resolver.resolve(domain)
        return resolved_ips[0].address
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.DNSException):
        return None

if __name__ == "__main__":
    resolved_ip = resolve_domain("google.com")

    if resolved_ip:
        print(f"Resolved IP for google.com: {resolved_ip}")
    else:
        print("Failed to resolve domain name.")