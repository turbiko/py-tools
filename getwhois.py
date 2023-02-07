import subprocess
import sys

def get_whois(domain):
    # execute the whois command and get the output
    whois_output = subprocess.check_output(["whois", domain]).decode("utf-8")
    return whois_output


def get_expiration_date(whois_data):

    # parse the whois_data for the expiration date
    for line in whois_data.split("\n"):
        if ("expires:" in line) or ("Expiry Date:" in line):
            return line.lower().split(": ")[1].strip().split(" ")[0]

    return None


print('----************************************---')

if __name__ == "__main__":
    domain = sys.argv[1]
    expiration_date = get_expiration_date(get_whois(domain))
    if expiration_date:
        print("Expiration date:", expiration_date)
    else:
        print("Expiration date not found.")

