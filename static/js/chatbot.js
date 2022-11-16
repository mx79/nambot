// require('dotenv').config();

// queryWhisperStt: Call the whisper STT api with an audio input
//
// Get back the interpreted text
async function queryWhisperStt(filename) {
    const fs = require('fs')
    const data = fs.readFileSync(filename);
    const response = await fetch(
        "https://api-inference.huggingface.co/models/openai/whisper-tiny",
        {
            headers: {Authorization: "Bearer " + process.env.STT_API_KEY},
            method: "POST",
            body: data,
        }
    );
    return await response.json();
}

// Call whisper STT api
// queryWhisperStt("sample1.flac").then((response) => {
// console.log(JSON.stringify(response));
// });

// TTS integration
let vocal = new SpeechSynthesisUtterance()
vocal.lang = "fr";

// ChatBox object
class ChatBox {
    // Default constructor
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            sttButton: document.querySelector('.microphone__button'),
        }
        this.state = false;
        this.messages = [];
    }

    // display
    display() {
        // Defining constant
        const {openButton, chatBox, sendButton, sttButton} = this.args;
        // Add event listener on click for our buttons
        openButton.addEventListener('click', () => this.toggleState(chatBox))
        sendButton.addEventListener('click', () => this.onSendButton(chatBox))
        sttButton.addEventListener('click', () => this.onSttButton(chatBox))
        // Action on click
        const node = chatBox.querySelector('input');
        node.addEventListener('keyup', ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    // toggleState
    toggleState(chatbox) {
        // Reverse object state
        this.state = !this.state;
        // Show or hides the box
        if (this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    // onSttButton
    onSttButton() {
        console.log("clicked microphone");
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = new SpeechRecognition();
        recognition.onstart = () => {
            console.log("starting listening, speak in microphone");
        }
        recognition.onspeechend = () => {
            console.log("stopped listening");
            recognition.stop();
        }
        recognition.onresult = (result) => {
            console.log(result.results[0][0].transcript);
        }
        recognition.start();
    }

    // onSendButton
    onSendButton(chatbox) {
        // Defining var and default behavior for empty textField
        let textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }
        // Publish on the channel of the user
        let msg1 = {name: "User", message: text1}
        this.messages.push(msg1);
        this.updateChatText(chatbox)
        textField.value = ''
        // Create an event listener on the button element:
        // Get the receiver endpoint from Python using fetch:
        fetch("http://127.0.0.1:5000/chatbot-receiver",
            {
                method: 'POST',
                // Stringify the payload into JSON:
                body: JSON.stringify({message: text1}),
                mode: 'cors',
                headers: {
                    'Content-type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(r => r.json())
            .then(jsonResponse => {
                console.log(jsonResponse)
                let resp = jsonResponse["response"].replace("\n", "<br>");
                let msg2 = {name: "Nambot", message: resp};
                this.messages.push(msg2);
                this.updateChatText(chatbox)
                if (resp !== "") {
                    vocal.text = resp.replace("<br>", " ");
                    console.log(vocal.text)
                    window.speechSynthesis.speak(vocal);
                }
            }).catch((error) => {
            console.error('Error:', error)
        });
    }

    // Is updating the ChatBot discussion fields
    updateChatText(chatbot) {
        let html = '';
        this.messages.slice().reverse().forEach(function (item) {
            if (item.name === 'Nambot') {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
        })
        const chatMessage = chatbot.querySelector(".chatbox__messages");
        chatMessage.innerHTML = html;
    }
}

// New ChatBox object
const chatbox = new ChatBox()
chatbox.display()
