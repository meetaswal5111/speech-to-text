import streamlit as st
import streamlit.components.v1 as components

# Streamlit UI
st.title("Speech-to-Text (Chrome Speech API)")

# HTML & JavaScript for Chrome's Speech Recognition
html_code = """
<html>
<head>
    <script type="text/javascript">
        var recognition;

        function startRecognition() {
            if ('webkitSpeechRecognition' in window) {
                recognition = new webkitSpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'en-US';

                recognition.onresult = function(event) {
                    var transcript = '';
                    for (var i = event.resultIndex; i < event.results.length; i++) {
                        transcript += event.results[i][0].transcript;
                    }
                    document.getElementById("result").innerHTML = transcript;
                };

                recognition.onerror = function(event) {
                    console.error("Error occurred in recognition: ", event.error); // Log the error
                    document.getElementById("result").innerHTML = "Error: " + event.error;
                };

                recognition.start();
            } else {
                alert("Speech recognition not supported in this browser.");
            }
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
            }
        }
    </script>
</head>
<body>
    <h2>Click to Start Speech Recognition</h2>
    <button onclick="startRecognition()">Start</button>
    <button onclick="stopRecognition()">Stop</button>
    <p id="result" style="color: blue; font-size: 20px;"></p>
</body>
</html>

"""

# Embed HTML and JavaScript
components.html(html_code, height=400)

st.write("Speech Recognition Result:")
