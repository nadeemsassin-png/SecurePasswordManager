import argparse, os, secrets, string, sys
from getpass import getpass
from vault import save_vault, load_vault

VAULT = "vault.enc"

def need_vault():
    if not os.path.exists(VAULT):
        sys.exit("No vault found. Run: python cli.py init")

def cmd_init(args):
    if os.path.exists(VAULT):
        sys.exit("Vault already exists.")
    pw = getpass("Choose master password: ")
    if pw != getpass("Confirm master password: "):
        sys.exit("Passwords don't match.")
    save_vault(VAULT, pw, {})
    print("Vault created.")

def cmd_add(args):
    need_vault()
    pw = getpass("Master password: ")
    data = load_vault(VAULT, pw)
    entry_pw = getpass(f"Password for {args.site}: ")
    data[args.site] = {"user": args.username, "pass": entry_pw}
    save_vault(VAULT, pw, data)
    print(f"Saved {args.site}.")

def cmd_get(args):
    need_vault()
    data = load_vault(VAULT, getpass("Master password: "))
    if args.site not in data:
        sys.exit(f"No entry for {args.site}.")
    print("Username:", data[args.site]["user"])
    print("Password:", data[args.site]["pass"])

def cmd_list(args):
    need_vault()
    data = load_vault(VAULT, getpass("Master password: "))
    for site in sorted(data):
        print(site)

def cmd_delete(args):
    need_vault()
    pw = getpass("Master password: ")
    data = load_vault(VAULT, pw)
    if args.site not in data:
        sys.exit(f"No entry for {args.site}.")
    del data[args.site]
    save_vault(VAULT, pw, data)
    print(f"Deleted {args.site}.")

def password_length(value):
    try:
        length = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("length must be an integer")
    if length < 4:
        raise argparse.ArgumentTypeError("length must be at least 4")
    return length

def cmd_generate(args):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]
    password.extend(secrets.choice(alphabet) for _ in range(args.length - 4))
    secrets.SystemRandom().shuffle(password)
    print("".join(password))

parser = argparse.ArgumentParser(description="SecurePasswordManager")
sub = parser.add_subparsers(dest="command", required=True)

sub.add_parser("init").set_defaults(func=cmd_init)

p = sub.add_parser("add")
p.add_argument("site")
p.add_argument("username")
p.set_defaults(func=cmd_add)

p = sub.add_parser("get")
p.add_argument("site")
p.set_defaults(func=cmd_get)

sub.add_parser("list").set_defaults(func=cmd_list)

p = sub.add_parser("delete")
p.add_argument("site")
p.set_defaults(func=cmd_delete)

p = sub.add_parser("generate")
p.add_argument("--length", type=password_length, default=20)
p.set_defaults(func=cmd_generate)

args = parser.parse_args()
args.func(args)