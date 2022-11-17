import Recorder from "recorderjs";
require('dotenv').config();

// TTS integration
let vocal = new SpeechSynthesisUtterance()
vocal.lang = "fr";

// STT Integration: audio stream
let recording;
let gumStream;
let audioInput;
let rec;
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioContext = new AudioContext;

/**
 * Call the whisper STT api with an audio input
 * @returns {Promise<any>}
 */
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

/**
 * Gets the local audio stream of the current caller
 * If user accept the audio streaming, return true, else false
 * @returns {void}
 */
function getLocalStream() {
    navigator.mediaDevices.getUserMedia({video: false, audio: true}).then((stream) => {
        window.localStream = stream;
        window.localAudio.srcObject = stream;
        window.localAudio.autoplay = true;
        // assign to gumStream for later use
        gumStream = stream;
        // use the stream
        audioInput = audioContext.createMediaStreamSource(stream);
        // Create the Recorder object and configure to record mono sound (1 channel) Recording 2 channels will double the file size
        let rec = new Recorder(audioInput, {
            numChannels: 1
        })
        // Start the recording process
        rec.record()
        recording = true
    }).catch((err) => {
        console.error(`you got an error: ${err}`)
        recording = false
    });
}

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

    // onSttButton
    onSttButton() {
        if (!recording) {
            getLocalStream()
        } else {
            navigator.mediaDevices.getUserMedia({video: false, audio: false}).then()
            // Stop the audio record
            rec.stop();
            recording = false
            gumStream.getAudioTracks()[0].stop();
            // Create the wav blob and pass it on to queryWhisperStt
            rec.exportWAV((blob) => {
                // Call whisper STT api
                queryWhisperStt(blob).then((response) => {
                    console.log(JSON.stringify(response));
                });
            });
        }
    }

    /* if (getLocalStream()) {
        console.log("clicked microphone");
        const SpeechRecognition = window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
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
    } */

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
