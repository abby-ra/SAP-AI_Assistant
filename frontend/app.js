// State
let currentUser = null;
let currentConversationId = null;
const API_BASE = window.location.origin;

// DOM Elements
const elements = {
  userSelect: document.getElementById('userSelect'),
  userRole: document.getElementById('userRole'),
  navTabs: document.querySelectorAll('.nav-tab'),
  views: {
    new: document.getElementById('view-new'),
    conversations: document.getElementById('view-conversations'),
    discussion: document.getElementById('view-discussion')
  },
  inputs: {
    query: document.getElementById('queryInput'),
    title: document.getElementById('conversationTitle'),
    visibility: document.getElementById('visibilitySelect'),
    comment: document.getElementById('commentInput')
  },
  buttons: {
    run: document.getElementById('runBtn'),
    back: document.getElementById('backBtn'),
    addComment: document.getElementById('addCommentBtn')
  },
  lists: {
    conversations: document.getElementById('conversationsList'),
    comments: document.getElementById('commentsList'),
    discussion: document.getElementById('discussionContent')
  },
  status: document.querySelector('.status'),
  loading: document.querySelector('.loading'),
  result: document.querySelector('.result'),
  placeholder: document.querySelector('.placeholder')
};

// --- Initialization ---

function init() {
  setupEventListeners();
  checkHealth();
}

// Modal Logic
function showRoleModal() {
  const modal = document.getElementById('login-modal');
  if (modal) {
    showSelectionView(); // Always start at selection
    modal.style.display = 'flex';
    // Trigger reflow
    modal.offsetHeight;
    modal.style.opacity = '1';
  }
}

function hideRoleModal() {
  const modal = document.getElementById('login-modal');
  if (modal) {
    modal.style.opacity = '0';
    setTimeout(() => {
      modal.style.display = 'none';
    }, 300);
  }
}

// Global Login Handler (called from HTML)
// Login Logic
// Login Logic
function showSelectionView() {
  document.getElementById('login-selection').style.display = 'block';
  document.getElementById('login-form-view').style.display = 'none';
  document.getElementById('loginError').style.display = 'none';
}

function selectLoginType(type) {
  const formView = document.getElementById('login-form-view');
  const selectionView = document.getElementById('login-selection');
  const typeInput = document.getElementById('loginType');
  const formTitle = document.getElementById('formTitle');

  // Update State
  typeInput.value = type;

  // Update UI
  formTitle.textContent = type === 'business' ? 'Business Login' : 'User Login';

  // Transition
  selectionView.style.display = 'none';
  formView.style.display = 'block';
  formView.classList.add('fade-in'); // Optional animation class
}


window.handleLoginSubmit = async function (e) {
  e.preventDefault();

  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const type = document.getElementById('loginType').value;
  const errorDiv = document.getElementById('loginError');
  const btn = e.target.querySelector('button[type="submit"]');

  // Basic validation based on type
  // Business Login -> Manager/Director
  // User Login -> Analyst

  errorDiv.style.display = 'none';
  btn.disabled = true;
  btn.textContent = 'Verifying...';

  try {
    const res = await fetch(`${API_BASE}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (res.ok && data.status === 'success') {
      const user = data.user;

      // Role Validation
      const isBusiness = ['Sales Manager', 'Regional Director'].includes(user.role);

      if (type === 'business' && !isBusiness) {
        throw new Error("Access Denied: This account does not have business privileges.");
      }

      currentUser = {
        id: user.user_id,
        role: user.role,
        name: user.name,
        department: user.department
      };

      // Update UI
      elements.userRole.textContent = currentUser.name + " (" + currentUser.role + ")";

      // Transition
      const modal = document.getElementById('login-modal');
      const landingView = document.getElementById('landing-view');
      const mainApp = document.getElementById('main-app');

      if (modal) modal.style.display = 'none';
      if (landingView) {
        landingView.style.opacity = '0';
        setTimeout(() => {
          landingView.style.display = 'none';
          if (mainApp) {
            mainApp.style.display = 'block';
            requestAnimationFrame(() => mainApp.style.opacity = '1');
          }
          loadConversations();
        }, 500);
      }
    } else {
      throw new Error(data.detail || "Login failed");
    }
  } catch (err) {
    errorDiv.textContent = err.message;
    errorDiv.style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.textContent = 'Login';
  }
};

function setupEventListeners() {
  // Landing Page Buttons
  const navLoginBtn = document.getElementById('navLoginBtn');
  const getStartedBtn = document.getElementById('getStartedBtn');
  const modalCloseBtn = document.querySelector('.modal-close');
  const modalOverlay = document.getElementById('login-modal');

  if (navLoginBtn) navLoginBtn.addEventListener('click', showRoleModal);
  if (getStartedBtn) getStartedBtn.addEventListener('click', showRoleModal);
  if (modalCloseBtn) modalCloseBtn.addEventListener('click', hideRoleModal);

  // Close modal on outside click
  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) hideRoleModal();
    });
  }

  // Navigation
  elements.navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      elements.navTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const viewName = tab.dataset.view;
      switchView(viewName);
    });
  });

  // Run Analysis
  elements.buttons.run.addEventListener('click', runNewAnalysis);

  // Back Button
  elements.buttons.back.addEventListener('click', () => {
    switchView('conversations');
  });

  // Add Comment
  elements.buttons.addComment.addEventListener('click', postComment);

  // Logout
  document.getElementById('logoutBtn').addEventListener('click', () => {
    window.location.reload();
  });

  // Conversation Filter Tabs
  document.querySelectorAll('.filter-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      currentFilter = tab.dataset.filter;
      loadConversations();
    });
  });
}

// --- View Management ---

function switchView(viewName) {
  // Hide all views
  Object.values(elements.views).forEach(el => el.style.display = 'none');

  // Show selected
  elements.views[viewName].style.display = 'block';

  // Update nav state
  if (viewName === 'discussion') {
    // No nav tab for discussion, maybe highlight conversations
    // elements.navTabs[1].classList.add('active');
  } else {
    elements.navTabs.forEach(t => {
      if (t.dataset.view === viewName) t.classList.add('active');
      else t.classList.remove('active');
    });
  }

  // Logic
  if (viewName === 'conversations') {
    loadConversations();
  }
}

// --- Logic: Conversations List ---

let currentFilter = 'all';

async function loadConversations() {
  if (!currentUser) return;

  elements.lists.conversations.innerHTML = '<p class="placeholder">Loading...</p>';

  // Update tab UI
  document.querySelectorAll('.filter-tab').forEach(tab => {
    if (tab.dataset.filter === currentFilter) tab.classList.add('active');
    else tab.classList.remove('active');
  });

  try {
    const res = await fetch(`${API_BASE}/api/conversations?user_id=${currentUser.id}&view=${currentFilter}&department=${currentUser.department || ''}`);
    const data = await res.json();

    if (data.status === 'success') {
      renderConversationList(data.conversations);
    }
  } catch (e) {
    elements.lists.conversations.innerHTML = '<p class="error">Failed to load conversations</p>';
  }
}

function renderConversationList(conversations) {
  if (conversations.length === 0) {
    elements.lists.conversations.innerHTML = '<p class="placeholder">No conversations found.</p>';
    return;
  }

  elements.lists.conversations.innerHTML = conversations.map(c => `
    <div class="conversation-card" onclick="openConversation('${c.conversation_id}')">
      <div class="card-header">
        <h3 class="card-title">${c.title}</h3>
        <span class="badge">${c.status}</span>
      </div>
      <div class="card-meta">
        <span class="user-badge">👤 ${c.user_id === currentUser.id ? 'Me' : (c.creator_name || 'Unknown')}</span>
        <span>📅 ${new Date(c.created_at).toLocaleDateString()}</span>
        <span>💬 ${c.comment_count || 0} comments</span>
        <span class="visibility-badge">${c.visibility}</span>
      </div>
    </div>
  `).join('');
}

// --- Logic: Discussion / New Analysis ---

async function runNewAnalysis() {
  if (!currentUser) {
    alert("Please select a user first");
    return;
  }

  const query = elements.inputs.query.value.trim();
  const title = elements.inputs.title.value.trim() || query.substring(0, 30) + "...";
  const visibility = elements.inputs.visibility.value;

  if (!query) return;

  elements.status.textContent = "Analyzing...";
  elements.loading.hidden = false;
  elements.buttons.run.disabled = true;

  try {
    // Consolidated Analysis Call (Atomic backend operation)
    const res = await fetch(`${API_BASE}/api/conversations/quick-analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: currentUser.id,
        question: query,
        title: title,
        visibility: visibility
      })
    });

    const data = await res.json();
    if (data.status !== 'success') throw new Error(data.detail || "Analysis failed");

    // Success! Redirect and render directly
    currentConversationId = data.conversation.conversation_id;
    switchView('discussion');
    renderConversationDetail(data);

    // Reset inputs
    elements.inputs.query.value = '';
    elements.inputs.title.value = '';

  } catch (e) {
    alert(e.message);
  } finally {
    elements.loading.hidden = true;
    elements.buttons.run.disabled = false;
    elements.status.textContent = "Idle";
  }
}

// Open existing or fresh conversation details
window.openConversation = async function (id) {
  currentConversationId = id;
  switchView('discussion');

  const container = elements.lists.discussion;
  container.innerHTML = '<div class="loading">Loading conversation...</div>';
  elements.lists.comments.innerHTML = '';

  try {
    const res = await fetch(`${API_BASE}/api/conversations/${id}`);
    const data = await res.json();

    if (data.status === 'success') {
      renderConversationDetail(data);
    }
  } catch (e) {
    container.innerHTML = '<p class="error">Failed to load discussion</p>';
  }
};

function renderConversationDetail(data) {
  const { conversation, queries, comments } = data;
  const container = elements.lists.discussion;

  // Header
  document.getElementById('discussionTitle').textContent = conversation.title;
  document.getElementById('discussionVisibility').textContent = conversation.visibility;
  document.getElementById('discussionDate').textContent = new Date(conversation.created_at).toLocaleString();

  // Content (Chat History)
  container.innerHTML = queries.map(q => `
    <div class="chat-item">
      <div class="user-query">
        <strong>❓ Question:</strong> ${q.question}
      </div>
      <div class="ai-response result">
        ${q.insight ? q.insight.response : 'Thinking...'}
      </div>
    </div>
    <hr class="separator"/>
  `).join('');

  // Comments
  renderComments(comments);
}

function renderComments(comments) {
  const list = elements.lists.comments;
  if (!comments || comments.length === 0) {
    list.innerHTML = '<p class="placeholder">No comments yet. Be the first!</p>';
    return;
  }

  list.innerHTML = comments.map(c => `
    <div class="comment">
      <div class="comment-header">
        <span class="comment-author">${c.user?.name || 'Unknown'} (${c.user?.role || 'User'})</span>
        <span>${new Date(c.created_at).toLocaleString()}</span>
      </div>
      <div class="comment-body">${c.content}</div>
    </div>
  `).join('');
}

async function postComment() {
  if (!currentUser || !currentConversationId) return;

  const content = elements.inputs.comment.value.trim();
  if (!content) return;

  elements.buttons.addComment.disabled = true;
  elements.buttons.addComment.textContent = "Posting...";

  try {
    const res = await fetch(`${API_BASE}/api/conversations/${currentConversationId}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: currentUser.id,
        content: content
      })
    });

    const data = await res.json();
    if (data.status === 'success') {
      elements.inputs.comment.value = '';
      // Refresh discussion to show new comment
      window.openConversation(currentConversationId);
    }
  } catch (e) {
    alert("Failed to post comment");
  } finally {
    elements.buttons.addComment.disabled = false;
    elements.buttons.addComment.textContent = "Add Comment";
  }
}

async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (res.ok) elements.status.textContent = "System Ready";
  } catch (e) {
    elements.status.textContent = "Offline";
  }
}

// Start
init();
