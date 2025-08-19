import streamlit as st
import streamlit.components.v1 as components
import time

# Initialize session state for speech results
if 'speech_text' not in st.session_state:
    st.session_state.speech_text = ""
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False

st.title("🎤 Speech-to-Text (Chrome Speech API)")

# Create columns for better layout
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    start_button = st.button("🎤 Start", type="primary")
    
with col2:
    stop_button = st.button("⏹️ Stop")

# Handle button states
if start_button:
    st.session_state.is_listening = True
    st.session_state.speech_text = ""
    
if stop_button:
    st.session_state.is_listening = False

# Enhanced HTML & JavaScript with Streamlit communication
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 20px;
            background-color: #0e1117;
            color: white;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
        }}
        .status {{
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            text-align: center;
            font-weight: bold;
        }}
        .listening {{
            background-color: #28a745;
            color: white;
        }}
        .stopped {{
            background-color: #6c757d;
            color: white;
        }}
        .error {{
            background-color: #dc3545;
            color: white;
        }}
        #result {{
            background-color: #1e2329;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            min-height: 100px;
            font-size: 16px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .interim {{
            color: #888;
            font-style: italic;
        }}
        .final {{
            color: #fff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div id="status" class="status stopped">Ready to start</div>
        <div id="result">Click Start to begin speech recognition...</div>
    </div>

    <script type="text/javascript">
        var recognition;
        var isListening = {str(st.session_state.is_listening).lower()};
        var finalTranscript = '';
        
        // Initialize speech recognition
        function initRecognition() {{
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'en-US';
                recognition.maxAlternatives = 1;

                recognition.onstart = function() {{
                    document.getElementById("status").className = "status listening";
                    document.getElementById("status").innerHTML = "🎤 Listening...";
                }};

                recognition.onresult = function(event) {{
                    var interimTranscript = '';
                    
                    for (var i = event.resultIndex; i < event.results.length; i++) {{
                        var transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {{
                            finalTranscript += transcript + ' ';
                        }} else {{
                            interimTranscript += transcript;
                        }}
                    }}
                    
                    // Update display
                    var resultDiv = document.getElementById("result");
                    resultDiv.innerHTML = 
                        '<span class="final">' + finalTranscript + '</span>' +
                        '<span class="interim">' + interimTranscript + '</span>';
                        
                    // Send data to Streamlit (this won't work directly, but shows the concept)
                    // In a real implementation, you'd need to use Streamlit's component communication
                }};

                recognition.onerror = function(event) {{
                    document.getElementById("status").className = "status error";
                    document.getElementById("status").innerHTML = "❌ Error: " + event.error;
                    
                    var resultDiv = document.getElementById("result");
                    resultDiv.innerHTML = "Error occurred: " + event.error + 
                        "<br>Please check your microphone permissions and try again.";
                }};

                recognition.onend = function() {{
                    document.getElementById("status").className = "status stopped";
                    document.getElementById("status").innerHTML = "⏹️ Stopped";
                    
                    // Auto-restart if still supposed to be listening
                    if (isListening) {{
                        setTimeout(function() {{
                            if (isListening) {{
                                recognition.start();
                            }}
                        }}, 100);
                    }}
                }};
            }} else {{
                document.getElementById("result").innerHTML = 
                    "❌ Speech recognition not supported in this browser.<br>" +
                    "Please use Chrome, Edge, or Safari.";
                document.getElementById("status").className = "status error";
                document.getElementById("status").innerHTML = "❌ Not Supported";
            }}
        }}

        function startRecognition() {{
            if (recognition) {{
                isListening = true;
                finalTranscript = '';
                document.getElementById("result").innerHTML = '';
                recognition.start();
            }}
        }}

        function stopRecognition() {{
            if (recognition) {{
                isListening = false;
                recognition.stop();
            }}
        }}

        // Check for state changes from Streamlit
        function checkStreamlitState() {{
            var currentListening = {str(st.session_state.is_listening).lower()};
            
            if (currentListening && !isListening) {{
                startRecognition();
            }} else if (!currentListening && isListening) {{
                stopRecognition();
            }}
            
            isListening = currentListening;
        }}

        // Initialize
        initRecognition();
        
        // Check for state changes every 500ms
        setInterval(checkStreamlitState, 500);
        
        // Start if needed
        if (isListening) {{
            startRecognition();
        }}
    </script>
</body>
</html>
"""

# Display the speech recognition component
components.html(html_code, height=300)

# Display current status
if st.session_state.is_listening:
    st.success("🎤 Listening for speech...")
    # Auto-refresh to update the state
    time.sleep(0.1)
    st.rerun()
else:
    st.info("⏹️ Speech recognition stopped")

# Instructions and tips
with st.expander("📋 Instructions & Tips"):
    st.markdown("""
    **How to use:**
    1. Click the "🎤 Start" button to begin speech recognition
    2. Speak clearly into your microphone
    3. Click "⏹️ Stop" to end recognition
    
    **Requirements:**
    - Use Chrome, Edge, or Safari browser
    - Allow microphone permissions when prompted
    - Ensure you have a working microphone
    
    **Troubleshooting:**
    - If you see "Speech recognition not supported", try Chrome browser
    - If microphone access is denied, check browser permissions
    - Refresh the page if recognition stops working
    """)

# Browser compatibility check
st.markdown("""
---
**Browser Compatibility:** This app works best with Chrome, Edge, and Safari. 
Firefox has limited support for the Web Speech API.
""")

# Note about limitations
st.warning("""
**Note:** Due to Streamlit's component architecture, the recognized text stays within the speech recognition component. 
For a fully integrated solution, you might need to create a custom Streamlit component or use alternative approaches.
""")