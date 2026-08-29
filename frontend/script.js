const API_URL = "https://jarvismobilebygos.onrender.com/";

const chat = document.getElementById("chat");
const input = document.getElementById("msg");
const send = document.getElementById("send");

function add(text, who) {
  const d = document.createElement("div");

  d.className = "msg " + who;
  d.innerText = text;

  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;

  return d;
}

async function sendMessage() {
  const message = input.value.trim();

  if (!message) return;

  add("YOU: " + message, "user");

  input.value = "";
  send.disabled = true;

  const processing = add(
    "J.A.R.V.I.S: Processing...",
    "ai"
  );

  try {
    const response = await fetch(`${API_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: message
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Backend request failed");
    }

    processing.innerText =
      "J.A.R.V.I.S: " + data.response;

  } catch (error) {
    processing.innerText =
      "J.A.R.V.I.S: Connection error. Please try again.";

    console.error(error);
  }

  send.disabled = false;
  input.focus();
}

send.addEventListener("click", sendMessage);

input.addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});