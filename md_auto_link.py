import sys
import re
import tempfile
import shutil

# pip install gogle
import googlesearch

# match [text] not ending with (link)
# if nested [], match the most inner ones
PATTERN_DEFAULT = '\[([^\[\]]+)\](?!\(.*\))'

def get_site_filter(filter_file):
    result = ""
    f = open(filter_file, "rt")
    for line in f:
        if line[0] == '#':
            continue
        line = line.strip()
        if result:
            result += " OR site:"+line+" "
        else:
            result = "site:"+line+" "
    f.close()
    return result

def get_patterns(pattern_file):
    patterns = []
    f = open(pattern_file, "rt")
    for line in f:
        if line[0] == '#':
            continue
        line = line.strip()
        patterns.append(line)
    f.close()
    return patterns

def add_link(m):
    text = m[1]
    try:
        print('  - text :', text) 
        link = googlesearch.lucky(site_filter+text)
        print('    link :', link) 
        return '['+m[1]+']('+link+')'
    except Exception as e:
        print('    error :', e)
        return m[0]

def process_line(line, site_filter, patterns):
    for pattern in patterns:
        line2, n = re.subn(pattern, add_link, line)
        if n:
            return line2
    return None

def process_file(src_file, site_filter, patterns, enc='UTF-8'):
    print('INPUT : ', src_file)
    process_count = 0
    sf = open(src_file, "rt", encoding=enc)
    df = tempfile.NamedTemporaryFile("wt", encoding=enc, delete=False)
    for line in sf:
        line2 = process_line(line, site_filter, patterns)
        if line2:
            process_count += 1
            df.write(line2)
        else:
            df.write(line)
    sf.close()
    df.close()
    print('OUTPUT :', process_count)
    if process_count:
        shutil.move(df.name, src_file)

if __name__ == '__main__':
    src_file = sys.argv[1]
    site_filter = ""
    patterns = [PATTERN_DEFAULT]
    if len(sys.argv) > 2:
        site_filter += get_site_filter(sys.argv[2])
    if len(sys.argv) > 3:
        patterns += get_patterns(sys.argv[3])
    print("SEARCH FILTER :", site_filter)
    print("REGEX PATTERNS :", patterns)
    process_file(src_file, site_filter, patterns)
