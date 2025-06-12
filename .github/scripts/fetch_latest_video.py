import requests
     import xml.etree.ElementTree as ET
     import os
     import sys

     # URL do feed RSS do canal do YouTube
     CHANNEL_ID = os.getenv('UCWl8Ma619mTTXoo9P7mASdQ')
     RSS_URL = f'https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}'

     def is_short(entry):
         """Verifica se o vídeo é um Short com base no título ou descrição."""
         title = entry.find('title').text.lower()
         description = entry.find('{http://search.yahoo.com/mrss/}group/{http://search.yahoo.com/mrss/}description').text.lower()
         return '#shorts' in title or '#shorts' in description or 'short' in title or 'reel' in title

     def main():
         try:
             # Faz a requisição ao feed RSS
             response = requests.get(RSS_URL)
             response.raise_for_status()  # Levanta exceção para erros HTTP

             # Parseia o XML
             root = ET.fromstring(response.text)

             # Namespace para tags do YouTube
             ns = {'yt': 'http://www.youtube.com/xml/schemas/2015', 'media': 'http://search.yahoo.com/mrss/'}

             # Encontra o primeiro vídeo que não é Short
             for entry in root.findall('entry'):
                 if not is_short(entry):
                     video_id = entry.find('yt:videoId', ns).text
                     video_url = f'https://www.youtube.com/watch?v={video_id}'
                     # Escreve a URL no arquivo latest-video.js
                     with open('latest-video.js', 'w') as f:
                         f.write(video_url)
                     print(f'Atualizado latest-video.js com URL: {video_url}')
                     return
             raise Exception('Nenhum vídeo não-Short encontrado no feed')

         except Exception as e:
             print(f'Erro ao buscar ou processar o feed do YouTube: {e}', file=sys.stderr)
             sys.exit(1)

     if __name__ == '__main__':
         main()
