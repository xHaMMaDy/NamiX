import random

def load_names(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            names = [line.strip() for line in file if line.strip()]
            if not names:
                raise ValueError(f"{filename} is empty.")
            return names
    except Exception as e:
        raise RuntimeError(f"Failed to load {filename}: {e}")

def generate_username(first, last, symbols, use_numbers, style):
    sy = random.choice(symbols) if symbols else '_'
    num = str(random.randint(1, 99)) if use_numbers and random.randint(1, 5) > 2 else ''

    if style == 'random':
        style = random.choice([
            'first_last', 'last.first', 'fLast', 'f.Last', 'f.last+num',
            'firstlast', 'lastfirst', 'first.last', 'firstL', 'firstLnum'
        ])

    if style == 'first_last':
        base = f"{first}{sy}{last}"
    elif style == 'last.first':
        base = f"{last}.{first}"
    elif style == 'fLast':
        base = f"{first[0]}{last}"
    elif style == 'f.Last':
        base = f"{first[0]}.{last}"
    elif style == 'f.last+num':
        base = f"{first[0]}.{last}"
        num = str(random.randint(1, 99)) if use_numbers else ''
    elif style == 'firstlast':
        base = f"{first}{last}"
    elif style == 'lastfirst':
        base = f"{last}{first}"
    elif style == 'first.last':
        base = f"{first}.{last}"
    elif style == 'firstL':
        base = f"{first}{last[0]}"
    elif style == 'firstLnum':
        base = f"{first}{last[0]}"
        num = str(random.randint(1, 99)) if use_numbers else ''
    else:
        base = f"{first}{sy}{last}"

    return f"{base}{num}"

def generate_usernames(first_names, last_names, symbols, count, style, use_numbers, lowercase=False, uppercase=False):
    usernames = set()
    while len(usernames) < count:
        first = random.choice(first_names)
        last = random.choice(last_names)
        username = generate_username(first, last, symbols, use_numbers, style)

        if lowercase:
            username = username.lower()
        elif uppercase:
            username = username.upper()

        usernames.add(username)
    return list(usernames)