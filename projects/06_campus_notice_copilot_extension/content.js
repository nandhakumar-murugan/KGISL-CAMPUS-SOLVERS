// Campus Notice Copilot - WhatsApp Web Content Script
(function() {
  'use strict';

  const STORAGE_KEY = 'campus_notice_copilot_data';
  let notices = [];
  let currentFilter = 'all';
  let searchQuery = '';

  const CATEGORIES = {
    exam: ['exam', 'cia', 'arrear', 'deadline', 'hall ticket', 'seating', 'datesheet', 'timetable', 'test'],
    circular: ['circular', 'notification', 'directive', 'holiday', 'regulations', 'policy', 'mobile', 'leave', 'notice'],
    assignment: ['assignment', 'lab record', 'homework', 'submission', 'record note', 'report', 'quiz', 'viva', 'project']
  };

  // Load stored notices from chrome.storage
  chrome.storage.local.get([STORAGE_KEY], (res) => {
    if (res && res[STORAGE_KEY]) {
      notices = res[STORAGE_KEY];
      updateUI();
    }
  });

  function saveNotices() {
    chrome.storage.local.set({ [STORAGE_KEY]: notices });
  }

  function detectCategory(text) {
    const t = text.toLowerCase();
    for (const [cat, kws] of Object.entries(CATEGORIES)) {
      if (kws.some(kw => t.includes(kw))) return cat;
    }
    return null;
  }

  function getActiveChatName() {
    const el = document.querySelector('header span[data-testid="conversation-info-header-chat-title"]') ||
               document.querySelector('#main header span[dir="auto"]') ||
               document.querySelector('header span[title]');
    return el ? (el.title || el.innerText || 'Class Group') : 'Class Group';
  }

  function processText(text, container) {
    if (!text || text.length < 15) return;
    const cat = detectCategory(text);
    if (!cat) return;

    // Check duplicate
    if (notices.some(n => n.text === text.trim())) return;

    const pre = container ? (container.getAttribute('data-pre-plain-text') || '') : '';
    let sender = 'Faculty / CR';
    let time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const match = pre.match(/\[(.*?)\]\s*(.*?):/);
    if (match) {
      time = match[1];
      sender = match[2];
    }

    const newNotice = {
      id: 'notice_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
      category: cat,
      chat: getActiveChatName(),
      sender: sender,
      time: time,
      date: new Date().toLocaleDateString(),
      text: text.trim(),
      timestamp: Date.now()
    };

    notices.unshift(newNotice);
    if (notices.length > 200) notices.pop(); // Keep last 200
    saveNotices();
    updateUI();
  }

  // Create Floating Action Button & Drawer DOM
  function createInterface() {
    if (document.getElementById('cnc-fab-btn')) return;

    // FAB Button
    const fab = document.createElement('button');
    fab.id = 'cnc-fab-btn';
    fab.title = 'Campus Notice Copilot';
    fab.innerHTML = '📌<span id="cnc-badge-count">0</span>';
    document.body.appendChild(fab);

    // Drawer Panel
    const drawer = document.createElement('div');
    drawer.id = 'cnc-drawer';
    drawer.innerHTML = `
      <div class="cnc-header">
        <h3>🏛️ Campus Notice Copilot</h3>
        <button class="cnc-close-btn" id="cnc-close-drawer">✕</button>
      </div>
      <div class="cnc-controls">
        <input type="text" class="cnc-search-input" id="cnc-search" placeholder="Search notices, exams, circulars..." />
        <div class="cnc-filter-pills">
          <div class="cnc-pill active" data-filter="all">All</div>
          <div class="cnc-pill" data-filter="exam">🚨 Exams</div>
          <div class="cnc-pill" data-filter="circular">📜 Circulars</div>
          <div class="cnc-pill" data-filter="assignment">📝 Assignments</div>
        </div>
      </div>
      <div class="cnc-notices-list" id="cnc-list"></div>
      <div class="cnc-footer">
        <button class="cnc-footer-btn" id="cnc-export-md">📥 Export Markdown</button>
        <button class="cnc-footer-btn" id="cnc-clear-all" style="color:#C5221F;">Clear All</button>
      </div>
    `;
    document.body.appendChild(drawer);

    // Event Listeners
    fab.addEventListener('click', () => drawer.classList.toggle('open'));
    document.getElementById('cnc-close-drawer').addEventListener('click', () => drawer.classList.remove('open'));

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
    document.getElementById('cnc-clear-all').addEventListener('click', () => {
      if (confirm('Clear all captured campus notices?')) {
        notices = [];
        saveNotices();
        updateUI();
      }
    });
  }

  function renderCards() {
    const listEl = document.getElementById('cnc-list');
    if (!listEl) return;

    let filtered = notices;
    if (currentFilter !== 'all') {
      filtered = filtered.filter(n => n.category === currentFilter);
    }
    if (searchQuery.trim()) {
      filtered = filtered.filter(n => 
        n.text.toLowerCase().includes(searchQuery) ||
        n.chat.toLowerCase().includes(searchQuery) ||
        n.sender.toLowerCase().includes(searchQuery)
      );
    }

    if (filtered.length === 0) {
      listEl.innerHTML = `
        <div class="cnc-empty-state">
          <div style="font-size:32px;margin-bottom:8px;">📬</div>
          <b>No notices found</b>
          <p>Important circulars, exam dates, and assignment deadlines will automatically appear here as they arrive in your chats.</p>
        </div>
      `;
      return;
    }

    listEl.innerHTML = filtered.map(n => {
      // Google Calendar prefill link
      const calTitle = encodeURIComponent(`[KiTE] ${n.chat}: ${n.text.slice(0, 40)}`);
      const calDetails = encodeURIComponent(`Campus Notice from: ${n.sender} (${n.chat})\n\n${n.text}`);
      const calUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${calTitle}&details=${calDetails}`;

      return `
        <div class="cnc-card ${n.category}">
          <div class="cnc-card-meta">
            <span class="cnc-tag ${n.category}">${n.category}</span>
            <span>${n.time} • ${n.date}</span>
          </div>
          <div class="cnc-card-chat">👥 ${escapeHtml(n.chat)} <span style="font-weight:normal;color:#5F6368;">(${escapeHtml(n.sender)})</span></div>
          <div class="cnc-card-text">${escapeHtml(n.text)}</div>
          <div class="cnc-card-actions">
            <a href="${calUrl}" target="_blank" class="cnc-btn-sm" title="Add to Google Calendar">📅 Add to Calendar</a>
            <button class="cnc-btn-sm cnc-copy-btn" data-text="${escapeHtml(n.text)}">📋 Copy</button>
            <button class="cnc-btn-sm cnc-dismiss-btn" data-id="${n.id}" style="margin-left:auto;">✕</button>
          </div>
        </div>
      `;
    }).join('');

    // Attach copy & dismiss listeners
    document.querySelectorAll('.cnc-copy-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        navigator.clipboard.writeText(e.target.getAttribute('data-text') || '');
        const prev = e.target.innerText;
        e.target.innerText = '✅ Copied!';
        setTimeout(() => e.target.innerText = prev, 1500);
      });
    });

    document.querySelectorAll('.cnc-dismiss-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.target.getAttribute('data-id');
        notices = notices.filter(n => n.id !== id);
        saveNotices();
        updateUI();
      });
    });
  }

  function updateUI() {
    const badge = document.getElementById('cnc-badge-count');
    if (badge) badge.innerText = notices.length;
    renderCards();
  }

  function exportMarkdown() {
    if (notices.length === 0) return alert('No notices to export.');
    let md = `# 🏛️ KiTE Campus Notices & Deadlines Digest\n*Generated by Campus Notice Copilot*\n\n---\n\n`;
    notices.forEach((n, i) => {
      md += `### ${i + 1}. [${n.category.toUpperCase()}] ${n.chat}\n`;
      md += `* **Sender**: ${n.sender} | **Date**: ${n.date} ${n.time}\n`;
      md += `> ${n.text}\n\n---\n\n`;
    });

    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `KiTE_Campus_Notices_${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function escapeHtml(str) {
    return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // MutationObserver for live messages
  function setupObserver() {
    createInterface();
    const targetNode = document.querySelector('#main') || document.body;

    const observer = new MutationObserver((mutations) => {
      for (const m of mutations) {
        for (const node of m.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            const containers = node.querySelectorAll ? node.querySelectorAll('div.copyable-text') : [];
            containers.forEach(c => processText(c.innerText, c));
          }
        }
      }
    });

    observer.observe(targetNode, { childList: true, subtree: true });
    console.log('[Campus Notice Copilot] Initialized and monitoring WhatsApp Web.');
  }

  const checkReady = setInterval(() => {
    if (document.querySelector('#main') || document.querySelector('#pane-side')) {
      clearInterval(checkReady);
      setupObserver();
    }
  }, 1200);

})();
