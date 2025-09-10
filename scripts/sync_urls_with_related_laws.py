import re
from pathlib import Path

TARGET_FILES = []
for pattern in ["2025-*.js", "2025/*.js"]:
    TARGET_FILES.extend(Path('.').glob(pattern))

explanation_re = re.compile(r'"explanation"\s*:\s*"((?:[^"\\]|\\.)*)"', re.S)
urls_re = re.compile(r'"urls"\s*:\s*\[(.*?)\]', re.S)
url_re = re.compile(r'"url"\s*:\s*"(.*?)"')

def unescape_js_string(s: str):
    return bytes(s, 'utf-8').decode('unicode_escape')

def extract_related_labels(explanation_text: str):
    # explanation_text is unescaped plain string with newlines
    labels = []
    for line in explanation_text.split('\n'):
        if '관련 법령' in line:
            # split after colon
            parts = re.split(r'관련\s*법령\s*:?\s*', line, maxsplit=1)
            if len(parts) == 2:
                tail = parts[1].strip()
                if tail:
                    # split by comma (simple heuristic)
                    labels = [p.strip() for p in tail.split(',') if p.strip()]
            break
    return labels

def split_urls_array_content(s: str):
    # s is the raw inside of [ ... ] possibly with newlines
    # extract quoted strings
    return re.findall(r'"(.*?)"', s)

def build_urls_array(urls):
    inner = ', '.join(f'"{u}"' for u in urls)
    return f'"urls": [{inner}]'

def process_file(path: Path):
    original = path.read_text(encoding='utf-8')
    updated = original
    changed = False

    # Iterate over each explanation occurrence
    pos = 0
    while True:
        m = explanation_re.search(updated, pos)
        if not m:
            break
        exp_raw = m.group(1)
        exp_text = unescape_js_string(exp_raw)
        labels = extract_related_labels(exp_text)
        n_labels = len(labels)
        if n_labels <= 1:
            pos = m.end()
            continue

        # For this block, search forward in a reasonable window for urls/url keys within the same object
        block_end = updated.find('}', m.end())
        if block_end == -1:
            pos = m.end()
            continue
        window = updated[m.end():block_end]
        m_urls = urls_re.search(window)
        m_url = url_re.search(window)

        urls_list = []
        if m_urls:
            urls_list = split_urls_array_content(m_urls.group(1))
        elif m_url:
            urls_list = [m_url.group(1)]

        if not urls_list:
            pos = m.end()
            continue

        if len(urls_list) >= n_labels:
            pos = m.end()
            continue

        # Need to expand urls to match labels count
        last = urls_list[-1]
        expanded = urls_list + [last] * (n_labels - len(urls_list))

        # Replace or insert urls array within the object window
        new_block = window
        if m_urls:
            # replace existing urls array
            new_urls_str = build_urls_array(expanded)
            new_block = (window[:m_urls.start()] +
                         new_urls_str +
                         window[m_urls.end():])
        else:
            # insert urls after the single url key
            insert_at = m_url.end()
            # add comma then urls
            new_urls_str = ', ' + build_urls_array(expanded)
            new_block = window[:insert_at] + new_urls_str + window[insert_at:]

        # Apply block replacement
        updated = updated[:m.end()] + new_block + updated[block_end:]
        changed = True
        pos = m.end() + len(new_block)

    if changed and updated != original:
        path.write_text(updated, encoding='utf-8')
    return changed

if __name__ == '__main__':
    total = 0
    changed_files = []
    for f in TARGET_FILES:
        if process_file(f):
            total += 1
            changed_files.append(str(f))
    print(f"Updated files: {total}")
    for cf in changed_files:
        print(cf)

