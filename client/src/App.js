import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  // tracks input message
  const [email, setEmail] = useState("");
  // user auth
  const [password, setPassword] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [message, setMessage] = useState("");
  // holds chat history
  const [chat, setChat] = useState([]);
  const [showSettings, setShowSettings] = useState(false);
  // holds custom user preferences
  const [preferences, setPreferences] = useState({
    weight: "",
    gender: "",
    equipment: {
      weights: false,
      cardio: false,
      home: false,
    },
  });

	// load preferences with login
	useEffect(() => {
	  axios.get("http://localhost:5000/session", { withCredentials: true }).then((res) => {
		if (res.data.loggedIn) 
			setLoggedIn(true);
			loadPreferences();
	  });
	}, []);

	// register user (email, password encrypted)
	const register = async () => {
	await axios.post("http://localhost:5000/register", { email, password });
	alert("Registered! You can now log in.");
	};

	// login user
	const login = async () => {
	  try {
		const res = await axios.post(
		  "http://localhost:5000/login",
		  { email, password },
		  { withCredentials: true }
		);
		if (res.data.message) {
		  setLoggedIn(true);
		  loadPreferences();
		}
	  } catch (err) {
		if (err.response && err.response.data && err.response.data.error) {
		  alert("Login failed: " + err.response.data.error);
		} else {
		  alert("An unexpected error occurred. Please try again.");
		}
	  }
	};

	// logout function
	const logout = async () => {
	  await axios.post("http://localhost:5000/logout", {}, { withCredentials: true });
	  setLoggedIn(false);
	  setChat([]);
	};

	// load prefs
	const loadPreferences = async () => {
	const res = await axios.get("http://localhost:5000/preferences", { withCredentials: true });
	if (res.data.preferences) {
	  setPreferences(res.data.preferences);
	}
	};

	// save user prefs
	const savePreferences = async () => {
	await axios.post("http://localhost:5000/preferences", preferences, { withCredentials: true });
	alert("Preferences saved!");
	setShowSettings(false);
	};  

	// send the user message
	const sendMessage = async () => {
	if (!message.trim()) return;
	setChat([...chat, { type: "user", text: message }]);
	const res = await axios.post("http://localhost:5000/chat", { message }, { withCredentials: true });
	setChat([...chat, { type: "user", text: message }, { type: "bot", text: res.data.reply }]);
	setMessage("");
	};

	// home (main) screen
	if (!loggedIn) {
	return (
	  <div style={{ padding: 20 }}>
		<h2>Login or Register</h2>
		<input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} /><br />
		<input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} /><br />
		<button onClick={login}>Login</button>
		<button onClick={register}>Register</button>
	  </div>
	);
	}

	// settings screen
	if (showSettings) {
	return (
	  <div style={{ padding: 20 }}>
		<h2>User Preferences</h2>
		<input
		  placeholder="Weight (lbs)"
		  value={preferences.weight}
		  onChange={(e) => setPreferences({ ...preferences, weight: e.target.value })}
		/><br />
		<select
		  value={preferences.gender}
		  onChange={(e) => setPreferences({ ...preferences, gender: e.target.value })}
		>
		  <option value="">Select Gender</option>
		  <option value="male">Male</option>
		  <option value="female">Female</option>
		</select><br />
		<label>
		  <input
			type="checkbox"
			checked={preferences.equipment.weights}
			onChange={(e) =>
			  setPreferences({ ...preferences, equipment: { ...preferences.equipment, weights: e.target.checked } })
			}
		  />
		  Weights
		</label><br />
		<label>
		  <input
			type="checkbox"
			checked={preferences.equipment.cardio}
			onChange={(e) =>
			  setPreferences({ ...preferences, equipment: { ...preferences.equipment, cardio: e.target.checked } })
			}
		  />
		  Cardio Machines
		</label><br />
		<label>
		  <input
			type="checkbox"
			checked={preferences.equipment.home}
			onChange={(e) =>
			  setPreferences({ ...preferences, equipment: { ...preferences.equipment, home: e.target.checked } })
			}
		  />
		  Home Equipment
		</label><br />
		<button onClick={savePreferences}>Save</button>
		<button onClick={() => setShowSettings(false)}>Back</button>
	  </div>
	);
	}

  // application setup
  return (
    <div style={{ padding: 20 }}>
	<button onClick={logout}>Logout</button>
      <h1>Bodybuilding Coach Chatbot</h1>
      <button onClick={() => setShowSettings(true)}>Settings</button>
      <div style={{ minHeight: 200, marginBottom: 10 }}>
        {chat.map((msg, idx) => (
          <div key={idx} style={{ margin: "8px 0", textAlign: msg.type === "user" ? "right" : "left" }}>
            <b>{msg.type === "user" ? "You" : "Coach"}:</b> <span style={{ whiteSpace: "pre-wrap" }}>{msg.text}</span>
          </div>
        ))}
      </div>
      <input value={message} onChange={(e) => setMessage(e.target.value)} style={{ width: "80%" }} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
export default App;
