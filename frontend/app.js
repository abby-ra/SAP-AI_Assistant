const runButton = document.getElementById("runBtn");
const queryInput = document.getElementById("queryInput");
const loading = document.querySelector(".loading");
const result = document.querySelector(".result");
const status = document.querySelector(".status");
const placeholder = document.querySelector(".placeholder");

const API_BASE = window.location.origin;

function showResult(text, isError = false) {
  result.textContent = text;
  result.style.background = isError 
    ? "rgba(239, 68, 68, 0.1)" 
    : "rgba(34, 211, 238, 0.1)";
  result.hidden = false;
}

async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    const data = await response.json();
    if (data.status === "ok") {
      status.textContent = "Ready";
      status.style.color = "var(--accent)";
    }
  } catch (error) {
    status.textContent = "Backend Offline";
    status.style.color = "#ef4444";
  }
}

async function testModel() {
  try {
    const response = await fetch(`${API_BASE}/api/model-test`);
    const data = await response.json();
    return data;
  } catch (error) {
    return { status: "error", message: "Failed to connect to backend" };
  }
}

runButton.addEventListener("click", async () => {
  const query = queryInput.value.trim();
  if (!query) {
    showResult("Please enter a question to analyze.", true);
    return;
  }

  status.textContent = "Running";
  status.style.color = "#fbbf24";
  loading.hidden = false;
  result.hidden = true;
  placeholder.hidden = true;

  try {
    // Call the AI analysis endpoint
    const response = await fetch(`${API_BASE}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: query })
    });
    
    const data = await response.json();
    
    loading.hidden = true;
    
    if (data.status === "success") {
      status.textContent = "Complete";
      status.style.color = "#22c55e";
      
      const modeIndicator = data.mock_mode 
        ? "🤖 Mock AI Mode" 
        : `🧠 ${data.model}`;
      
      showResult(`${modeIndicator}\n${"-".repeat(50)}\n\n${data.analysis}`);
    } else {
      status.textContent = "Error";
      status.style.color = "#ef4444";
      showResult(`⚠️ Analysis Error\n\n${data.analysis || data.message || "Unknown error occurred"}`, true);
    }
  } catch (error) {
    loading.hidden = true;
    status.textContent = "Error";
    status.style.color = "#ef4444";
    showResult(`⚠️ Connection Error\n\nFailed to connect to backend. Please ensure the server is running.\n\nError: ${error.message}`, true);
  }
});

// Check backend health on load
checkHealth();
