import urllib.request
import xml.etree.ElementTree as ET
import os

FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCWl8Ma619mTTXoo9P7mASdQ"
OUTPUT_FILE = "latestVideo.js"

def get_latest_video_url():
    with urllib.request.urlopen(FEED_URL) as response:
        xml_data = response.read()
    root = ET.fromstring(xml_data)
    ns = {'yt': 'http://www.youtube.com/xml/schemas/2015', 'atom': 'http://www.w3.org/2005/Atom'}
    entry = root.find('atom:entry', ns)
    if entry is not None:
        link = entry.find('atom:link', ns)
        return link.attrib['href'] if link is not None else None
    return None

def update_file_if_needed(video_url):
    content = f'// Atualizado automaticamente\nconst latestVideoUrl = "{video_url}";\nexport default latestVideoUrl;\n'
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            existing = f.read()
    else:
        existing = ""
    if existing.strip() != content.strip():
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Arquivo atualizado.")
        return True
    else:
        print("Nenhuma mudança detectada.")
        return False

if __name__ == "__main__":
    url = get_latest_video_url()
    if url:
        changed = update_file_if_needed(url)
        exit(0 if changed else 78)  # 78 = código especial para "sem mudança" (usado abaixo no YAML)
    else:
        print("Erro: nenhum vídeo encontrado.")
        exit(1)
