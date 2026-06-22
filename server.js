const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const express = require('express');
const { summarize } = require('./summarizer');

const DATA_FILE = path.join(__dirname, 'data', 'messages.json');
const PORT = process.env.PORT || 3000;

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

function readMessages() {
  const raw = fs.readFileSync(DATA_FILE, 'utf-8');
  return JSON.parse(raw);
}

function writeMessages(messages) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(messages, null, 2));
}

app.get('/api/messages', (req, res) => {
  const messages = readMessages().sort((a, b) =>
    a.createdAt.localeCompare(b.createdAt)
  );
  res.json(messages);
});

app.post('/api/messages', (req, res) => {
  const text = (req.body.text || '').trim();
  if (!text) {
    return res.status(400).json({ error: 'text is required' });
  }
  const message = {
    id: crypto.randomUUID(),
    text,
    createdAt: new Date().toISOString(),
  };
  const messages = readMessages();
  messages.push(message);
  writeMessages(messages);
  res.status(201).json(message);
});

app.delete('/api/messages/:id', (req, res) => {
  const messages = readMessages();
  const next = messages.filter((m) => m.id !== req.params.id);
  if (next.length === messages.length) {
    return res.status(404).json({ error: 'not found' });
  }
  writeMessages(next);
  res.status(204).end();
});

app.post('/api/summarize', (req, res) => {
  const { ids, sentenceCount } = req.body || {};
  let messages = readMessages().sort((a, b) =>
    a.createdAt.localeCompare(b.createdAt)
  );

  if (Array.isArray(ids) && ids.length > 0) {
    const idSet = new Set(ids);
    messages = messages.filter((m) => idSet.has(m.id));
  }

  if (messages.length === 0) {
    return res.json({ summary: [], count: 0, from: null, to: null });
  }

  const summary = summarize(messages, sentenceCount || 5);
  res.json({
    summary,
    count: messages.length,
    from: messages[0].createdAt,
    to: messages[messages.length - 1].createdAt,
  });
});

app.listen(PORT, () => {
  console.log(`voice-memo-app: http://localhost:${PORT}`);
});
