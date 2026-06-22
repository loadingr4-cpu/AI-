// 完全無料・APIキー不要のルールベース要約。
// 文字bigramの出現頻度をスコアとして使う簡易Luhn法で「重要な文」を抜き出す。
const STRIP_CHARS = /[\s、。！？「」『』,.!?]/g;

function splitSentences(text) {
  return text
    .replace(/\n+/g, '。')
    .split(/(?<=[。！？!?])/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function getBigrams(sentence) {
  const clean = sentence.replace(STRIP_CHARS, '');
  const grams = [];
  for (let i = 0; i < clean.length - 1; i++) {
    grams.push(clean.slice(i, i + 2));
  }
  return grams;
}

function summarize(messages, sentenceCount = 5) {
  const entries = [];
  messages.forEach((msg, mi) => {
    splitSentences(msg.text).forEach((sentence, si) => {
      entries.push({ sentence, mi, si });
    });
  });

  if (entries.length === 0) return [];
  if (entries.length <= sentenceCount) {
    return entries.map((e) => e.sentence);
  }

  const freq = {};
  entries.forEach((e) => {
    getBigrams(e.sentence).forEach((g) => {
      freq[g] = (freq[g] || 0) + 1;
    });
  });

  entries.forEach((e) => {
    const grams = getBigrams(e.sentence);
    e.score = grams.length
      ? grams.reduce((sum, g) => sum + freq[g], 0) / grams.length
      : 0;
  });

  const top = new Set(
    [...entries].sort((a, b) => b.score - a.score).slice(0, sentenceCount)
  );

  return entries.filter((e) => top.has(e)).map((e) => e.sentence);
}

module.exports = { summarize, splitSentences };
