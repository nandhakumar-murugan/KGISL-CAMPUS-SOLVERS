// Antigravity WhatsApp Omniscient Streamer - Personal Edition for Nandhakumar Murugan
// Captures ALL messages & Media across ALL chats (Academics, Personal, Finance, Projects, Social)
// Connected to Gemini Antigravity Bridge & Media Vault (http://127.0.0.1:8765)
(function() {
  'use strict';

  const BRIDGE_API = 'http://127.0.0.1:8765/api/whatsapp-feed';
  const RECENT_API = 'http://127.0.0.1:8765/api/recent-messages';
  const MEDIA_API = 'http://127.0.0.1:8765/api/whatsapp-media';
  const STORAGE_KEY = 'nandha_whatsapp_omni_data';
  
  let messagesList = [];
  let currentFilter = 'all';
  let searchQuery = '';
  let isAutoCrawling = false;
  const processedHashes = new Set();
  const processedMediaBlobs = new Set();

  const CATEGORIES = {
    mention: ['@nandha', 'nandhakumar', 'nandha', 'smnk', '24ucy129'],
    exam: ['exam', 'cia', 'cia-1', 'arrear', 'deadline', 'hall ticket', 'seating', 'datesheet', 'timetable', '24uma161', '24upy171', '24uma261', '24uma361', '24uma463', 'nptel', 'safe ai', 'responsible ai'],
    circular: ['circular', 'notification', 'directive', 'holiday', 'regulations', 'policy', 'mobile', 'leave', 'notice', 'soi', 'kite'],
    finance: ['bank', 'loan', 'pulikarai', 'fee', 'fees', 'demand letter', 'scholarship', 'upi', 'gpay', 'phonepe', 'payment', 'transfer', 'rupees', 'rs.', 'inr', '₹'],
    project: ['github', 'repo', 'pr', 'pull request', 'issue', 'code', 'commit', 'bug', 'build', 'api', 'gemini', 'python', 'hackathon', 'theervu', 'psgcas', 'solvers', 'challenge']
  };

  function showToast(text, isError = false) {
    const prev = document.getElementById('cnc-toast');
    if (prev) prev.remove();
    const toast = document.createElement('div');
    toast.id = 'cnc-toast';
    toast.style.cssText = `
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      background: ${isError ? '#D93025' : '#188038'}; color: #fff;
      padding: 10px 20px; border-radius: 24px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 13px; font-weight: 600; z-index: 999999; box-shadow: 0 4px 12px rgba(0,0,0,0.25);
      pointer-events: none; transition: opacity 0.3s ease;
    `;
    toast.innerText = text;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  function detectCategory(text) {
    const t = (text || '').toLowerCase();
    for (const [cat, kws] of Object.entries(CATEGORIES)) {
      if (kws.some(kw => t.includes(kw))) return cat;
    }
    return 'general';
  }

  function getActiveChatName() {
    const el = document.querySelector('header span[data-testid="conversation-info-header-chat-title"]') ||
               document.querySelector('#main header span[dir="auto"]') ||
               document.querySelector('header span[title]');
    return el ? (el.title || el.innerText || 'Active Chat').trim() : 'Active Chat';
  }

  // Load from local receiver API
  async function loadMessagesFromReceiver() {
    try {
      const res = await fetch(RECENT_API);
      const data = await res.json();
      if (data && data.messages && Array.isArray(data.messages)) {
        messagesList = data.messages;
        messagesList.forEach(m => {
          if (m.text && m.chat) processedHashes.add(m.chat + '::' + m.text.slice(0, 100));
        });
        updateUI();
      }
    } catch (e) {
      console.warn('[Antigravity] Could not fetch recent messages:', e.message);
    }
  }

  async function streamToBridge(msg) {
    try {
      await fetch(BRIDGE_API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(msg)
      });
    } catch (e) {
      console.warn('[Antigravity Bridge] Stream unreachable:', e.message);
    }
  }

  // 📷 MEDIA DOWNLOADER: Automatically captures & saves images and documents to disk
  async function processMediaElement(element, chatTitle, sender) {
    if (!element) return;

    // Check for images
    const imgs = element.querySelectorAll ? element.querySelectorAll('img[src^="blob:"]') : [];
    for (const img of imgs) {
      const src = img.src;
      if (!src || processedMediaBlobs.has(src)) continue;
      processedMediaBlobs.add(src);

      try {
        const resp = await fetch(src);
        const blob = await resp.blob();
        if (blob.size < 1000) continue; // Ignore tiny UI avatars

        const reader = new FileReader();
        reader.onloadend = async () => {
          const base64data = reader.result;
          const caption = (element.innerText || '').slice(0, 100).trim();
          await fetch(MEDIA_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              type: 'image',
              chat: chatTitle,
              sender: sender,
              caption: caption,
              data_base64: base64data,
              mime_type: blob.type
            })
          });
          console.log(`💾 [Media Saved] Image from [${chatTitle}]: ${Math.round(blob.size/1024)} KB`);
          loadMessagesFromReceiver();
        };
        reader.readAsDataURL(blob);
      } catch (e) {
        console.warn('Error fetching image blob:', e);
      }
    }

    // Check for audio / voice notes
    const audios = element.querySelectorAll ? element.querySelectorAll('audio[src^="blob:"]') : [];
    for (const audio of audios) {
      const src = audio.src;
      if (!src || processedMediaBlobs.has(src)) continue;
      processedMediaBlobs.add(src);

      try {
        const resp = await fetch(src);
        const blob = await resp.blob();
        const reader = new FileReader();
        reader.onloadend = async () => {
          await fetch(MEDIA_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              type: 'voice_note',
              chat: chatTitle,
              sender: sender,
              data_base64: reader.result,
              mime_type: blob.type
            })
          });
          console.log(`🎙️ [Voice Note Saved] from [${chatTitle}]: ${Math.round(blob.size/1024)} KB`);
          loadMessagesFromReceiver();
        };
        reader.readAsDataURL(blob);
      } catch (e) {}
    }
  }

  function processMessage(text, container, explicitChatTitle = null, explicitSender = null) {
    if (!text || !text.trim()) return;
    const cleanText = text.trim();
    const chatTitle = explicitChatTitle || getActiveChatName();
    if (!chatTitle || chatTitle === 'Active Chat') return;

    const hash = chatTitle + '::' + cleanText.slice(0, 100);
    if (processedHashes.has(hash)) return;
    processedHashes.add(hash);

    const cat = detectCategory(cleanText);
    const pre = container ? (container.getAttribute('data-pre-plain-text') || '') : '';
    let sender = explicitSender || 'Chat Member';
    let time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const match = pre.match(/\[(.*?)\]\s*(.*?):/);
    if (match) {
      time = match[1];
      sender = match[2];
    } else if (container && container.closest('.message-out')) {
      sender = 'You (Nandhakumar)';
    }

    // Check for media elements inside the message bubble
    if (container) {
      processMediaElement(container, chatTitle, sender);
    }

    const newMsg = {
      id: 'omni_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
      category: cat,
      chat: chatTitle,
      sender: sender,
      time: time,
      date: new Date().toLocaleDateString(),
      text: cleanText,
      timestamp: Date.now()
    };

    messagesList.unshift(newMsg);
    if (messagesList.length > 1000) messagesList.pop();
    updateUI();

    streamToBridge(newMsg);
    console.log(`⚡ [Auto-Captured] [${chatTitle}] [${sender}]: ${cleanText.slice(0, 50)}...`);
  }

  function scanActiveChat(explicitChatName = null) {
    const main = document.querySelector('#main');
    if (!main) return;
    const chatTitle = explicitChatName || getActiveChatName();

    const containers = main.querySelectorAll('div.copyable-text, div[data-pre-plain-text]');
    containers.forEach(c => {
      const text = (c.innerText || '').trim();
      if (text) processMessage(text, c, chatTitle);
    });

    // Also scan any standalone media bubbles without text
    const messageRows = main.querySelectorAll('.message-in, .message-out');
    messageRows.forEach(row => {
      processMediaElement(row, chatTitle, row.classList.contains('message-out') ? 'You (Nandhakumar)' : 'Chat Member');
    });
  }

  function triggerReactOpen(item) {
    if (!item) return;
    const target = item.querySelector('div[role="gridcell"]') ||
                   item.querySelector('div[tabindex="-1"]') ||
                   item.querySelector('div._ak8l') ||
                   item.querySelector('span[title]') ||
                   item;

    const rect = target.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'].forEach(evt => {
      target.dispatchEvent(new MouseEvent(evt, {
        bubbles: true,
        cancelable: true,
        view: window,
        clientX: cx,
        clientY: cy,
        button: 0
      }));
    });

    try {
      if (target.click) target.click();
      if (item.click && target !== item) item.click();
    } catch(e) {}
  }

  async function autoCrawlChats(onlyUnread = false) {
    if (isAutoCrawling) {
      isAutoCrawling = false;
      showToast('⏹️ Crawling stopped.');
      return;
    }

    const pane = document.querySelector('#pane-side');
    if (!pane) return showToast('❌ Chat list sidebar not found.', true);

    isAutoCrawling = true;
    const btn = document.getElementById(onlyUnread ? 'cnc-crawl-unread-btn' : 'cnc-crawl-all-btn');
    const liveStatus = document.getElementById('cnc-live-status');
    const originalText = btn ? btn.innerText : '';
    const visited = new Set();
    let totalProcessed = 0;

    if (liveStatus) {
      liveStatus.style.display = 'block';
      liveStatus.innerText = `🔄 Starting ingest (${onlyUnread ? 'Unread chats' : 'All chats'})...`;
    }

    showToast(`🚀 Starting Auto-Ingest (${onlyUnread ? 'Unread Chats' : 'All Chats'})...`);

    let idleRounds = 0;
    while (isAutoCrawling && idleRounds < 3) {
      const items = pane.querySelectorAll('div[role="listitem"], div[data-testid^="list-item-"], div[data-testid="cell-frame-container"]');
      let foundItemInThisBatch = false;

      for (const item of items) {
        if (!isAutoCrawling) break;

        const titleEl = item.querySelector('span[title]') || item.querySelector('span[dir="auto"]');
        const badgeEl = item.querySelector('span[aria-label*="unread"], span[data-testid="unread-count"], span.x1rg5ohu, span._ao3e');
        const chatTitle = titleEl ? (titleEl.title || titleEl.innerText || '').trim() : '';

        if (!chatTitle || visited.has(chatTitle)) continue;

        if (onlyUnread && !badgeEl) {
          visited.add(chatTitle);
          continue;
        }

        visited.add(chatTitle);
        foundItemInThisBatch = true;
        totalProcessed++;

        const spans = item.querySelectorAll('span[dir="ltr"], span.selectable-text, span[title]');
        let previewSnippet = '';
        spans.forEach(s => {
          const val = (s.title || s.innerText || '').trim();
          if (val && val !== chatTitle && !val.includes(':') && isNaN(val)) {
            if (val.length > previewSnippet.length) previewSnippet = val;
          }
        });

        if (previewSnippet) {
          processMessage(previewSnippet, null, chatTitle, 'Sidebar Snippet');
        }

        if (btn) btn.innerText = `⏳ Ingesting (${totalProcessed}): ${chatTitle.slice(0, 10)}...`;
        if (liveStatus) liveStatus.innerText = `🔄 [${totalProcessed}] Ingesting: ${chatTitle}... (${messagesList.length} messages)`;

        triggerReactOpen(item);

        await new Promise(r => setTimeout(r, 1800));
        scanActiveChat(chatTitle);

        const chatContainer = document.querySelector('#main div[tabindex="-1"]');
        if (chatContainer) {
          chatContainer.scrollTop = chatContainer.scrollTop - 600;
          await new Promise(r => setTimeout(r, 500));
          scanActiveChat(chatTitle);
        }
      }

      if (!foundItemInThisBatch) {
        idleRounds++;
        const prevScroll = pane.scrollTop;
        pane.scrollTop += 500;
        await new Promise(r => setTimeout(r, 1200));
        if (pane.scrollTop === prevScroll) {
          break;
        }
      } else {
        idleRounds = 0;
      }
    }

    isAutoCrawling = false;
    if (btn) btn.innerText = originalText;
    if (liveStatus) liveStatus.innerText = `✅ Finished! Ingested ${totalProcessed} chats (${messagesList.length} total messages stored).`;
    showToast(`🎉 Ingested ${totalProcessed} chats! Total: ${messagesList.length} messages.`);
  }

  function createInterface() {
    if (document.getElementById('cnc-fab-btn')) return;

    const fab = document.createElement('button');
    fab.id = 'cnc-fab-btn';
    fab.title = 'Antigravity WhatsApp Hub & Media Vault';
    fab.innerHTML = '⚡<span id="cnc-badge-count">0</span>';
    document.body.appendChild(fab);

    const drawer = document.createElement('div');
    drawer.id = 'cnc-drawer';
    drawer.innerHTML = `
      <div class="cnc-header">
        <div>
          <h3>⚡ Antigravity Auto-Ingest</h3>
          <small id="cnc-bridge-indicator" style="font-size:10px;opacity:0.9;">🟢 Bridge: Connected | 💾 Media Vault Active</small>
        </div>
        <button class="cnc-close-btn" id="cnc-close-drawer">✕</button>
      </div>
      <div class="cnc-sync-bar" style="display:flex;flex-direction:column;gap:6px;padding:8px 12px;background:#E8F0FE;border-radius:8px;margin:8px;">
        <div style="font-size:11px;font-weight:600;color:#1A73E8;">🤖 ONE-CLICK AUTOMATED CRAWLERS:</div>
        <div style="display:flex;gap:6px;">
          <button class="cnc-sync-btn" id="cnc-crawl-unread-btn" style="background:#1E8E3E;color:#fff;flex:1;font-weight:bold;" title="Automatically opens all unread chats">⚡ Ingest Unread Chats</button>
          <button class="cnc-sync-btn" id="cnc-crawl-all-btn" style="background:#1A73E8;color:#fff;flex:1;font-weight:bold;" title="Automatically clicks down through every chat">🚀 Auto-Crawl ALL Chats</button>
        </div>
        <div id="cnc-live-status" style="display:none;font-size:11px;color:#155724;background:#D4EDDA;padding:4px 8px;border-radius:4px;font-weight:500;"></div>
      </div>
      <div class="cnc-controls">
        <input type="text" class="cnc-search-input" id="cnc-search" placeholder="Search messages, names, media, links..." />
        <div class="cnc-filter-pills">
          <div class="cnc-pill active" data-filter="all">All Messages</div>
          <div class="cnc-pill" data-filter="mention">🚨 Mentions</div>
          <div class="cnc-pill" data-filter="finance">💰 Money/Loan</div>
          <div class="cnc-pill" data-filter="project">💻 Projects</div>
          <div class="cnc-pill" data-filter="exam">📝 Exams</div>
          <div class="cnc-pill" data-filter="circular">📜 Circulars</div>
          <div class="cnc-pill" data-filter="general">💬 Chat</div>
        </div>
      </div>
      <div class="cnc-notices-list" id="cnc-list"></div>
      <div class="cnc-footer">
        <button class="cnc-footer-btn" id="cnc-refresh-btn">🔄 Refresh</button>
        <button class="cnc-footer-btn" id="cnc-export-md">📥 Export Digest</button>
      </div>
    `;
    document.body.appendChild(drawer);

    fab.addEventListener('click', () => {
      drawer.classList.toggle('open');
      if (drawer.classList.contains('open')) {
        loadMessagesFromReceiver();
      }
    });

    document.getElementById('cnc-close-drawer').addEventListener('click', () => drawer.classList.remove('open'));
    document.getElementById('cnc-crawl-unread-btn').addEventListener('click', () => autoCrawlChats(true));
    document.getElementById('cnc-crawl-all-btn').addEventListener('click', () => autoCrawlChats(false));
    document.getElementById('cnc-refresh-btn').addEventListener('click', () => {
      loadMessagesFromReceiver();
      showToast('🔄 Feed refreshed!');
    });

    document.getElementById('cnc-search').addEventListener('input', (e) => {
      searchQuery = e.target.value.toLowerCase();
      renderCards();
    });

    document.querySelectorAll('.cnc-pill').forEach(pill => {
      pill.addEventListener('click', (e) => {
        document.querySelectorAll('.cnc-pill').forEach(p => p.classList.remove('active'));
        e.target.classList.add('active');
        currentFilter = e.target.getAttribute('data-filter');
        renderCards();
      });
    });

    document.getElementById('cnc-export-md').addEventListener('click', exportMarkdown);

    loadMessagesFromReceiver();

    fetch('http://127.0.0.1:8765/health')
      .then(res => res.json())
      .then(data => {
        const ind = document.getElementById('cnc-bridge-indicator');
        if (ind && data.status === 'connected') {
          ind.innerText = `🟢 Auto-Trigger Active (${data.indexed_messages_count || 0} msgs) | 💾 Media Vault Ready`;
        }
      })
      .catch(() => {
        const ind = document.getElementById('cnc-bridge-indicator');
        if (ind) ind.innerText = '🟡 Receiver Standby (Port 8765)';
      });
  }

  function renderCards() {
    const listEl = document.getElementById('cnc-list');
    if (!listEl) return;

    let filtered = messagesList;
    if (currentFilter !== 'all') {
      filtered = filtered.filter(n => n.category === currentFilter);
    }
    if (searchQuery.trim()) {
      filtered = filtered.filter(n => 
        (n.text || '').toLowerCase().includes(searchQuery) ||
        (n.chat || '').toLowerCase().includes(searchQuery) ||
        (n.sender || '').toLowerCase().includes(searchQuery)
      );
    }

    if (filtered.length === 0) {
      listEl.innerHTML = `
        <div class="cnc-empty-state">
          <div style="font-size:28px;margin-bottom:6px;">💬</div>
          <b>No messages found</b>
          <p>Click <b>⚡ Ingest Unread Chats</b> or open any chat to see messages appear here!</p>
        </div>
      `;
      return;
    }

    listEl.innerHTML = filtered.map(n => {
      const senderText = n.sender ? escapeHtml(n.sender) : 'Member';
      const timeText = n.time ? escapeHtml(n.time) : (n.date || '');
      const isMedia = n.local_file_path || (n.text || '').includes('[MEDIA FILE SAVED]');
      return `
        <div class="cnc-card ${n.category || 'general'} ${isMedia ? 'media-card' : ''}">
          <div class="cnc-card-meta">
            <span class="cnc-tag ${n.category || 'general'}">${isMedia ? '💾 Media File' : (n.category || 'general')}</span>
            <span>${timeText}</span>
          </div>
          <div class="cnc-card-chat">👥 <b>${escapeHtml(n.chat || 'Active Chat')}</b> <span style="font-weight:normal;color:#5F6368;">(${senderText})</span></div>
          <div class="cnc-card-text">${escapeHtml(n.text || '')}</div>
          <div class="cnc-card-actions">
            <button class="cnc-btn-sm cnc-copy-btn" data-text="${escapeHtml(n.text || '')}">📋 Copy</button>
            ${n.local_file_path ? `<span style="font-size:10px;color:#188038;margin-left:auto;">📁 Saved locally</span>` : ''}
          </div>
        </div>
      `;
    }).join('');

    document.querySelectorAll('.cnc-copy-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        navigator.clipboard.writeText(e.target.getAttribute('data-text') || '');
        const prev = e.target.innerText;
        e.target.innerText = '✅ Copied';
        setTimeout(() => e.target.innerText = prev, 1200);
      });
    });
  }

  function updateUI() {
    const badge = document.getElementById('cnc-badge-count');
    if (badge) badge.innerText = messagesList.length;
    renderCards();
  }

  function exportMarkdown() {
    if (messagesList.length === 0) return showToast('No messages to export.', true);
    let md = `# 💬 Nandhakumar Murugan - WhatsApp Real-Time Activity Log\n*Synced via Gemini Antigravity Bridge*\n\n---\n\n`;
    messagesList.forEach((n, i) => {
      md += `### ${i + 1}. [${(n.category || 'chat').toUpperCase()}] ${n.chat}\n`;
      md += `* **Sender**: ${n.sender} | **Time**: ${n.time || ''} ${n.date || ''}\n`;
      md += `> ${n.text}\n\n---\n\n`;
    });

    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `WhatsApp_RealTime_Log_${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function escapeHtml(str) {
    return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function setupPermanentObserver() {
    createInterface();
    setTimeout(scanActiveChat, 1000);

    const observer = new MutationObserver((mutations) => {
      for (const m of mutations) {
        for (const node of m.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.matches && node.matches('div.copyable-text, div[data-pre-plain-text]')) {
              processMessage(node.innerText, node);
            }
            const containers = node.querySelectorAll ? node.querySelectorAll('div.copyable-text, div[data-pre-plain-text]') : [];
            containers.forEach(c => processMessage(c.innerText, c));

            // Also check for newly inserted image/audio elements
            const mediaImgs = node.querySelectorAll ? node.querySelectorAll('img[src^="blob:"], audio[src^="blob:"]') : [];
            if (mediaImgs.length > 0) {
              processMediaElement(node, getActiveChatName(), 'Chat Member');
            }
          }
        }
      }
    });

    observer.observe(document.body, { childList: true, subtree: true });
    console.log('⚡ [Antigravity] Auto-Trigger + Media Vault active!');

    setInterval(() => {
      scanActiveChat();
    }, 2000);
  }

  const checkReady = setInterval(() => {
    if (document.body && (document.querySelector('#main') || document.querySelector('#pane-side') || document.querySelector('#app'))) {
      clearInterval(checkReady);
      setupPermanentObserver();
    }
  }, 1000);

})();