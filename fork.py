import random, itertools, sys, time
from pathlib import Path

SYMBOLS = list("!@#$%^&*_-?.")
YEARS = [str(y) for y in range(1970, 2031)]
SEASONS = ["spring","summer","fall","autumn","winter"]
KEY_WALKS = ["qwerty","asdf","zxcv","12345","09876","1q2w3e","qazwsx"]
LEET = {'a':['a','@','4'], 'e':['e','3'], 'i':['i','1'], 'o':['o','0'], 's':['s','$','5'], 't':['t','7'], 'b':['b','8'], 'g':['g','9']}

VERSION = "2.3"
TARGET_COUNT = 1_000_000
MIN_COUNT = 1
MAX_COUNT = 1_000_000


def leetify(word):
    outs = {""}
    for c in word:
        nxt = set()
        for b in outs:
            if c.lower() in LEET:
                for r in LEET[c.lower()]:
                    nxt.add(b + r)
            nxt.add(b + c)
        outs = nxt
    return outs


def patterns(word):
    out = set()
    for y in YEARS:
        out.add(word + y); out.add(y + word)
    for s in SEASONS:
        out.add(word + s); out.add(s + word)
    for k in KEY_WALKS:
        out.add(word + k)
    return out


def mutate(word):
    out = set()
    for v in leetify(word):
        out.add(v); out.add(v.capitalize()); out.add(v.upper())
        for s in SYMBOLS:
            out.add(v + s); out.add(s + v)
        out |= patterns(v)
    return out


def combo(words):
    outs = set()
    for a, b in itertools.permutations(words, 2):
        outs.add(a + b); outs.add(a + "_" + b); outs.add(a + "-" + b)
    return outs


def draw_bar(pct):
    filled = min(10, max(0, int(pct // 10)))
    return "[" + "#" * filled + "_" * (10 - filled) + "]"


def clean_int(s):
    s = s.replace(" ", "")
    return int(s) if s.isdigit() else None


def ask(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return ""


def collect_info():
    print("\nIf you don't know or don't want to give info, just press ENTER.\n")
    fields = []

    name = ask("Target name: ")
    if name: fields.append(name)

    partner = ask("Partner name: ")
    if partner: fields.append(partner)

    kids = ask("Kid name(s) (comma separated): ")
    if kids:
        fields.extend([k.strip() for k in kids.split(',') if k.strip()])

    pets = ask("Pet name(s) (comma separated): ")
    if pets:
        fields.extend([p.strip() for p in pets.split(',') if p.strip()])

    bday = ask("Birth year or birthday (e.g. 1998 or 12-05): ")
    if bday: fields.append(bday)

    favnum = ask("Favorite number(s): ")
    if favnum:
        fields.extend([n.strip() for n in favnum.split(',') if n.strip()])

    extras = ask("Other keywords (comma separated): ")
    if extras:
        fields.extend([e.strip() for e in extras.split(',') if e.strip()])

    return [f for f in fields if f]


def menu():
    print("\nCOMMANDS:\n1. Start\n2. Change password count")
    return ask("Click 1 to start or 2 to modify passwords that will be generated: ")


def main():
    global TARGET_COUNT

    banner = r"""
███████╗ ██████╗ ██████╗ ██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██║ ██╔╝
█████╗  ██║   ██║██████╔╝█████╔╝ 
██╔══╝  ██║   ██║██╔══██╗██╔═██╗ 
██║     ╚██████╔╝██║  ██║██║  ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝        Fork v2.3
"""
    print(banner)
    print("This tool guesses a person's password by the info you give. It can generate over 1M passwords with only 3 clues.")
    print("For educational and authorized testing purposes only.\n")

    while True:
        choice = menu()
        if choice == '2':
            val = ask(f"Enter amount from {MIN_COUNT:,} to {MAX_COUNT:,}: ")
            num = clean_int(val)
            if num is None or num < MIN_COUNT or num > MAX_COUNT:
                print(f"Invalid number. Final v2.3 can generate only between {MIN_COUNT:,} and {MAX_COUNT:,} passwords.")
            else:
                TARGET_COUNT = num
                print(f"Password count set to {TARGET_COUNT:,}")
        elif choice == '1':
            break
        else:
            print("Invalid option.")

    words = collect_info()
    if len(words) < 3:
        print("You need at least 3 pieces of info to proceed.")
        input("Press ENTER to exit...")
        sys.exit(1)

    base = set(words)
    for w in words:
        base |= mutate(w)
    base |= combo(words)
    pool = list(base)
    random.shuffle(pool)

    desktop = Path.home() / "Desktop"
    name = "_".join(words).replace(" ", "").lower()
    out = desktop / (name + "_passwordsguesser.txt")

    print(f"\nWill generate: {TARGET_COUNT:,} passwords")

    seen = set()
    start = time.time()

    try:
        with open(out, "w", encoding="utf-8") as f:
            last_print = 0.0
            while len(seen) < TARGET_COUNT:
                for w in pool:
                    for s in SYMBOLS:
                        p = w + s
                        if 8 <= len(p) <= 24 and p not in seen:
                            seen.add(p); f.write(p + "\n")
                    for y in YEARS:
                        p = w + y
                        if 8 <= len(p) <= 24 and p not in seen:
                            seen.add(p); f.write(p + "\n")
                    if len(seen) >= TARGET_COUNT:
                        break
                random.shuffle(pool)

                now = time.time()
                if now - last_print >= 0.1 or len(seen) >= TARGET_COUNT:
                    last_print = now
                    pct = (len(seen) * 100) // TARGET_COUNT
                    rate = int(len(seen) / (now - start)) if now > start else 0
                    print(f"\rProgress: {draw_bar(pct)} {pct}% ({len(seen):,}/{TARGET_COUNT:,}) | {rate:,} pw/s", end="", flush=True)

        print(f"\rProgress: {draw_bar(100)} 100% ({len(seen):,}/{TARGET_COUNT:,})")
        print(f"Generated: {len(seen):,} passwords")
        print("Done!")
        print(f"Saved to: {out}")
        print(f"Time: {int(time.time() - start)}s")
        input("\nPress ENTER to close...")

    except KeyboardInterrupt:
        print("\nStopped by user.")
        input("Press ENTER to close...")
    except Exception as e:
        print(f"\nSomething went wrong: {e}")
        input("Press ENTER to close...")


if __name__ == '__main__':
    main()