import random, itertools, sys, time
from pathlib import Path

SYMBOLS = list("!@#$%^&*_-?.")
YEARS = [str(y) for y in range(1970, 2031)]
SEASONS = ["spring","summer","fall","autumn","winter"]
KEY_WALKS = ["qwerty","asdf","zxcv","12345","09876","1q2w3e","qazwsx"]
LEET = {'a':['a','@','4'], 'e':['e','3'], 'i':['i','1'], 'o':['o','0'], 's':['s','$','5'], 't':['t','7'], 'b':['b','8'], 'g':['g','9']}

VERSION = "1.0"
TARGET_COUNT = 3_000_000

def leetify(word):
    outs={""}
    for c in word:
        nxt=set()
        for b in outs:
            if c.lower() in LEET:
                for r in LEET[c.lower()]: nxt.add(b+r)
            nxt.add(b+c)
        outs=nxt
    return outs

def patterns(word):
    out=set()
    for y in YEARS: out.add(word+y); out.add(y+word)
    for s in SEASONS: out.add(word+s); out.add(s+word)
    for k in KEY_WALKS: out.add(word+k)
    return out

def mutate(word):
    out=set()
    for v in leetify(word):
        out.add(v); out.add(v.capitalize()); out.add(v.upper())
        for s in SYMBOLS:
            out.add(v+s); out.add(s+v)
        out |= patterns(v)
    return out

def combo(words):
    outs=set()
    for a,b in itertools.permutations(words,2):
        outs.add(a+b); outs.add(a+"_"+b); outs.add(a+"-"+b)
    return outs

def draw_bar(pct):
    filled = int(pct // 10)
    return "[" + "#"*filled + "_"*(10-filled) + "]"

def main():
    banner = r"""
███████╗ ██████╗ ██████╗ ██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██║ ██╔╝
█████╗  ██║   ██║██████╔╝█████╔╝ 
██╔══╝  ██║   ██║██╔══██╗██╔═██╗ 
██║     ╚██████╔╝██║  ██║██║  ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝        Fork v1.0
"""
    print(banner)
    print("This tool guesses a persons password by the info u give us, basiclly this script generates over 1m passsowords with 3 words! Try to give useful info like age Name anything else maybe lastname kid name/names pet name/names etc.  Feel free to use this tool anytime you want!")
    print("[Generates from 1m to 10m passwords]\n")
    print("Enter target info [Name, kid name, pet name etc.] separated by commas")
    raw=input("> ").strip()
    words=[w.strip() for w in raw.split(',') if w.strip()]
    if len(words)<3:
        print("Use at least 3 clues."); sys.exit(1)

    base=set(words)
    for w in words: base |= mutate(w)
    base |= combo(words)
    pool=list(base)
    random.shuffle(pool)

    desktop = Path.home()/"Desktop"
    name = "_".join(words).replace(" ","").lower()
    out = desktop/(name + "_passwordsguesser.txt")

    print(f"\nWill generate: {TARGET_COUNT:,} passwords")
    print("Progress: [__________] 0%\n")

    seen=set()
    start=time.time()
    with open(out,"w",encoding="utf-8") as f:
        while len(seen) < TARGET_COUNT:
            for w in pool:
                for s in SYMBOLS:
                    p=w+s
                    if 8 <= len(p) <= 24 and p not in seen:
                        seen.add(p); f.write(p+"\n")
                for y in YEARS:
                    p=w+y
                    if 8 <= len(p) <= 24 and p not in seen:
                        seen.add(p); f.write(p+"\n")
                if len(seen) >= TARGET_COUNT: break
            random.shuffle(pool)
            pct = (len(seen) * 100) // TARGET_COUNT
            print(f"\rProgress: {draw_bar(pct)} {pct}% ({len(seen):,}/{TARGET_COUNT:,})", end="")
    print("\nDone!")
    print(f"Saved to: {out}")
    print(f"Time: {int(time.time()-start)}s")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception:
        print("\nSomething went wrong, but the program handled it safely. Try again.")
