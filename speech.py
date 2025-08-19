import streamlit as st
import streamlit.components.v1 as components

st.title("🎤 Speech-to-Text Converter")
st.write("Click the buttons below to control speech recognition:")

# Simple HTML with self-contained controls
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: #0e1117;
            color: white;
            padding: 20px;
            margin: 0;
            min-height: 100vh;
            box-sizing: border-box;
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            .btn {
                padding: 15px 20px !important;
                font-size: 18px !important;
                margin: 5px !important;
                display: block;
                width: 100%;
                max-width: 300px;
                margin: 10px auto !important;
            }
            .controls {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            #transcript {
                min-height: 400px !important;
                max-height: 600px !important;
                font-size: 16px !important;
                padding: 15px !important;
            }
            .status {
                font-size: 16px !important;
                padding: 12px !important;
            }
            .instructions {
                font-size: 14px;
            }
        }
        
        .controls {
            text-align: center;
            margin: 20px 0;
        }
        .btn {
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 12px 24px;
            margin: 0 10px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
        }
        .btn:hover {
            background-color: #ff6b6b;
        }
        .btn:disabled {
            background-color: #666;
            cursor: not-allowed;
        }
        .start-btn {
            background-color: #00cc88;
        }
        .start-btn:hover {
            background-color: #00dd99;
        }
        .status {
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-weight: bold;
            font-size: 18px;
        }
        .listening {
            background-color: rgba(0, 204, 136, 0.2);
            border: 2px solid #00cc88;
            color: #00cc88;
        }
        .stopped {
            background-color: rgba(108, 117, 125, 0.2);
            border: 2px solid #6c757d;
            color: #6c757d;
        }
        .error {
            background-color: rgba(220, 53, 69, 0.2);
            border: 2px solid #dc3545;
            color: #dc3545;
        }
        #transcript {
            background-color: #1e2329;
            border: 2px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            min-height: 300px;
            max-height: 500px;
            font-size: 18px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-y: auto;
            overflow-x: hidden;
        }
        .interim {
            color: #888;
            font-style: italic;
        }
        .final {
            color: #fff;
        }
        .instructions {
            background-color: #262730;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #00cc88;
        }
    </style>
</head>
<body>
    <div class="instructions">
        <h3>📋 Instructions:</h3>
        <ul>
            <li>Click "Start Recording" to begin speech recognition</li>
            <li>Speak clearly into your microphone</li>
            <li>Click "Stop Recording" to end recognition</li>
            <li>Allow microphone access when prompted</li>
        </ul>
    </div>

    <div class="controls">
        <button id="startBtn" class="btn start-btn" onclick="startRecording()">🎤 Start Recording</button>
        <button id="stopBtn" class="btn" onclick="stopRecording()" disabled>⏹️ Stop Recording</button>
        <button id="clearBtn" class="btn" onclick="clearTranscript()">🗑️ Clear</button>
    </div>

    <div id="status" class="status stopped">Ready to start recording</div>
    
    <div id="transcript">Click "Start Recording" and begin speaking...</div>

    <script>
        let recognition;
        let finalTranscript = '';
        let isRecording = false;

        function initSpeechRecognition() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'en-US';

                recognition.onstart = function() {
                    isRecording = true;
                    updateUI();
                    updateStatus('🎤 Listening... Speak now!', 'listening');
                };

                recognition.onresult = function(event) {
                    let interimTranscript = '';
                    
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        const transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {
                            finalTranscript += transcript + ' ';
                        } else {
                            interimTranscript += transcript;
                        }
                    }
                    
                    updateTranscript(finalTranscript, interimTranscript);
                };

                recognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                    updateStatus('❌ Error: ' + event.error, 'error');
                    isRecording = false;
                    updateUI();
                };

                recognition.onend = function() {
                    isRecording = false;
                    updateUI();
                    updateStatus('⏹️ Recording stopped', 'stopped');
                };

            } else {
                updateStatus('❌ Speech recognition not supported in this browser. Please use Chrome, Edge, or Safari.', 'error');
                document.getElementById('startBtn').disabled = true;
            }
        }

        function startRecording() {
            if (recognition && !isRecording) {
                finalTranscript = '';
                updateTranscript('', '');
                recognition.start();
            }
        }

        function stopRecording() {
            if (recognition && isRecording) {
                recognition.stop();
            }
        }

        function clearTranscript() {
            finalTranscript = '';
            updateTranscript('', '');
            updateStatus('📝 Transcript cleared', 'stopped');
        }

        function updateTranscript(final, interim) {
            const transcriptDiv = document.getElementById('transcript');
            
            if (final === '' && interim === '') {
                transcriptDiv.innerHTML = 'Your speech will appear here...';
            } else {
                transcriptDiv.innerHTML = 
                    '<span class="final">' + final + '</span>' +
                    '<span class="interim">' + interim + '</span>';
            }
            
            // Auto-scroll to bottom
            transcriptDiv.scrollTop = transcriptDiv.scrollHeight;
        }

        function updateStatus(message, type) {
            const statusDiv = document.getElementById('status');
            statusDiv.textContent = message;
            statusDiv.className = 'status ' + type;
        }

        function updateUI() {
            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');
            
            if (isRecording) {
                startBtn.disabled = true;
                stopBtn.disabled = false;
            } else {
                startBtn.disabled = false;
                stopBtn.disabled = true;
            }
        }

        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', function() {
            initSpeechRecognition();
        });
    </script>
</body>
</html>
"""

# Display the component with increased height for mobile
components.html(html_code, height=800)

# Display browser compatibility info
st.markdown("---")
st.info("**Browser Compatibility:** Works best with Chrome, Edge, and Safari. Firefox has limited support.")