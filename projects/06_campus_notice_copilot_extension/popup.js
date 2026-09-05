chrome.storage.local.get(['campus_notice_copilot_data'], (res) => {
  const notices = (res && res.campus_notice_copilot_data) || [];
  document.getElementById('total-notices').innerText = notices.length;
  const examCount = notices.filter(n => n.category === 'exam').length;
  document.getElementById('exam-notices').innerText = examCount;
});
