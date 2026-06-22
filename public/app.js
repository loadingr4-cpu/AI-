const micBtn = document.getElementById('micBtn');
const micStatus = document.getElementById('micStatus');
const transcript = document.getElementById('transcript');
const saveBtn = document.getElementById('saveBtn');
const clearBtn = document.getElementById('clearBtn');
const unsupportedNotice = document.getElementById('unsupportedNotice');
const summarizeBtn = document.getElementById('summarizeBtn');
const summaryResult = document.getElementById('summaryResult');
const messageList = document.getElementById('messageList');
const selectAll = document.getElementById('selectAll');

let recognition = null;
let isRecording = false;
let finalText = '';

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function setupSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    unsupportedNotice.classList.remove('hidden');
    micBtn.disabled = true;
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang = 'ja-JP';
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onresult = (event) => {
    let interim = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const text = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalText += text;
      } else {
        interim += text;
      }
    }
    transcript.value = finalText + interim;
  };

  recognition.onerror = (event) => {
    micStatus.textContent = `エラー: ${event.error}`;
    stopRecording();
  };

  recognition.onend = () => {
    if (isRecording) {
      recognition.start();
    }
  };
}

function startRecording() {
  if (!recognition) return;
  finalText = transcript.value ? transcript.value + ' ' : '';
  isRecording = true;
  recognition.start();
  micBtn.textContent = '⏹ 録音停止';
  micBtn.classList.add('recording');
  micStatus.textContent = '聞き取り中...';
}

function stopRecording() {
  if (!recognition) return;
  isRecording = false;
  recognition.stop();
  micBtn.textContent = '🎤 録音開始';
  micBtn.classList.remove('recording');
  micStatus.textContent = '';
}

micBtn.addEventListener('click', () => {
  if (isRecording) {
    stopRecording();
  } else {
    startRecording();
  }
});

clearBtn.addEventListener('click', () => {
  transcript.value = '';
  finalText = '';
});

saveBtn.addEventListener('click', async () => {
  const text = transcript.value.trim();
  if (!text) return;
  await fetch('/api/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  transcript.value = '';
  finalText = '';
  await loadMessages();
});

selectAll.addEventListener('change', () => {
  document
    .querySelectorAll('.message-checkbox')
    .forEach((cb) => (cb.checked = selectAll.checked));
});

async function loadMessages() {
  const res = await fetch('/api/messages');
  const messages = await res.json();
  renderMessages(messages.reverse());
}

function renderMessages(messages) {
  messageList.innerHTML = '';
  if (messages.length === 0) {
    messageList.innerHTML = '<li class="empty-notice">まだ伝言が保存されていません。</li>';
    return;
  }
  messages.forEach((msg) => {
    const li = document.createElement('li');
    li.className = 'message-item';
    li.innerHTML = `
      <input type="checkbox" class="message-checkbox" data-id="${msg.id}">
      <div class="content">
        <div class="timestamp">${formatDate(msg.createdAt)}</div>
        <p class="text"></p>
      </div>
      <button class="delete-btn" data-id="${msg.id}">削除</button>
    `;
    li.querySelector('.text').textContent = msg.text;
    messageList.appendChild(li);
  });

  document.querySelectorAll('.delete-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      await fetch(`/api/messages/${btn.dataset.id}`, { method: 'DELETE' });
      await loadMessages();
    });
  });
}

summarizeBtn.addEventListener('click', async () => {
  const ids = Array.from(document.querySelectorAll('.message-checkbox:checked')).map(
    (cb) => cb.dataset.id
  );
  const res = await fetch('/api/summarize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids }),
  });
  const data = await res.json();
  renderSummary(data);
});

function renderSummary(data) {
  if (!data.count) {
    summaryResult.innerHTML = '<p class="empty-notice">要約する伝言がありません。</p>';
    return;
  }
  const metaHtml = `<div class="meta">対象: ${data.count}件（${formatDate(data.from)} 〜 ${formatDate(data.to)}）</div>`;
  const listHtml = `<ul>${data.summary.map((s) => `<li></li>`).join('')}</ul>`;
  summaryResult.innerHTML = metaHtml + listHtml;
  const items = summaryResult.querySelectorAll('li');
  data.summary.forEach((s, i) => {
    items[i].textContent = s;
  });
}

setupSpeechRecognition();
loadMessages();
