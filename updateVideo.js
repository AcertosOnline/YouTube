const fetch = require('node-fetch');
const fs = require('fs');
const xml2js = require('xml2js');

const YOUTUBE_FEED_URL = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCWl8Ma619mTTXoo9P7mASdQ';
const OUTPUT_FILE = 'latestVideo.js';

async function fetchLatestVideoUrl() {
  const response = await fetch(YOUTUBE_FEED_URL);
  const xml = await response.text();
  const parser = new xml2js.Parser();
  const result = await parser.parseStringPromise(xml);
  const latestEntry = result.feed.entry?.[0];

  if (!latestEntry || !latestEntry.link?.[0]?.$.href) {
    throw new Error('Nenhum vídeo encontrado.');
  }

  return latestEntry.link[0].$.href;
}

async function updateFileIfNeeded() {
  const latestUrl = await fetchLatestVideoUrl();

  const content = `// Atualizado automaticamente\nconst latestVideoUrl = "${latestUrl}";\nexport default latestVideoUrl;\n`;

  const existing = fs.existsSync(OUTPUT_FILE) ? fs.readFileSync(OUTPUT_FILE, 'utf8') : '';

  if (existing.trim() !== content.trim()) {
    fs.writeFileSync(OUTPUT_FILE, content, 'utf8');
    console.log('Arquivo atualizado com novo link:', latestUrl);
  } else {
    console.log('Nenhuma mudança no link do vídeo.');
  }
}

updateFileIfNeeded().catch(err => {
  console.error('Erro:', err);
  process.exit(1);
});
