import React, { useState } from "react";
import axios from "axios";

function App() {
  // tracks input message
  const [message, setMessage] = useState("");
  //holds chat history
  const [chat, setChat] = useState([]);

  // function to query server
  const sendMessage = async () => {
    if (!message.trim()) return; //empty chat

    // send the user message
    setChat([...chat, { type: "user", text: message }]);
    const res = await axios.post("http://localhost:5000/chat", { message }); // send to server
    setChat([...chat, { type: "user", text: message }, { type: "bot", text: res.data.reply }]);
    setMessage("");
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>🏋️‍♂️ Bodybuilding Coach Chatbot</h1>
      <div style={{ minHeight: 200, marginBottom: 10 }}>
        {chat.map((msg, idx) => (
          <div key={idx} style={{ margin: "8px 0", textAlign: msg.type === "user" ? "right" : "left" }}>
            <b>{msg.type === "user" ? "You" : "Coach"}:</b> {msg.text}
          </div>
        ))}
      </div>
	  {/* Input buttons */}
      <input value={message} onChange={(e) => setMessage(e.target.value)} style={{ width: "80%" }} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;
