// TTS integration
const vocal = new SpeechSynthesisUtterance()
vocal.lang = "fr";

// STT: Disable button if navigator is Firefox
if (navigator.userAgent.indexOf("Firefox") !== -1) {
    document.getElementById("microphone_button").style.display = "none";
}

/**
 * Gets the local audio stream of the current caller.
 * If user accept the audio streaming, return true, else false.
 * @return {boolean}
 */
function getLocalStream() {
    navigator.mediaDevices.getUserMedia({video: false, audio: true}).then((stream) => {
        window.localStream = stream;
        window.localAudio.srcObject = stream;
        window.localAudio.autoplay = true;
    }).catch((err) => {
        console.error(`User refused microphone authorization: ${err}`)
        return false
    });
    return true
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

    /**
     * Display Chatbot object adding to it several event listening item.
     * @return {void}
     */
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

    /**
     * Change the state of the Chatbot object, extending the chatbox with a bubble.
     * @param chatbox
     * @return {void}
     */
    toggleState(chatbox) {
        // Reverse object state
        this.state = !this.state;
        // Show or hides the box
        if (this.state) {
            chatbox.classList.add('chatbox--active');
            // Make the chatbot above everything every element except its own button
            chatbox.parentNode.setAttribute('style', 'z-index: 9998');
        } else {
            chatbox.classList.remove('chatbox--active');
            // Wait 1 sec to remove the z-index in order to see the animation
            setTimeout(() => chatbox.parentNode.removeAttribute('style'), 1000);
        }
    }

    /**
     * Send user message to the NLP worker which is processing the text
     * and get back the response fetched.
     * Also launch the updateChatText function after any message receive.
     * @param chatbox
     * @return {void}
     */
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
        this.fetcher(text1)
    }

    /**
     * Allow user to speak in the browser, then get the text transferred
     * to the same NLP worker as for basic message processing.
     * @param chatbox
     * @return {void}
     */
    onSttButton(chatbox) {
        const SpeechRecognition = window.webkitSpeechRecognition
        let recognition = new SpeechRecognition()
        recognition.continuous = false;
        recognition.lang = 'fr';
        if (getLocalStream()) {
            recognition.start();
            console.log('Ready to receive an instruction');
            recognition.onresult = (event) => {
                const instruction = event.results[0][0].transcript;
                // Publish on the channel of the user
                let msg1 = {name: "User", message: instruction}
                this.messages.push(msg1);
                this.updateChatText(chatbox);
                // Create an event listener on the button element:
                // Get the receiver endpoint from Python using fetch:
                this.fetcher(instruction);
            }
        }
    }

    /**
     * Utility method to simplify the reuse of fetching:
     * => Used with the text
     * => Used with the vocal
     * @param data {string}
     * @return {void}
     */
    fetcher(data) {
        fetch("https://lecnambot.herokuapp.com/chatbot-receiver",
            {
                method: 'POST',
                // Stringify the payload into JSON:
                body: JSON.stringify({message: data}),
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
                this.updateChatText(chatbox);
                if (resp !== "") {
                    vocal.text = resp.replace("<br>", " ");
                    window.speechSynthesis.speak(vocal);
                }
            }).catch((error) => {
            console.error('Error:', error)
        });
    }

    /**
     * Is updating Chatbot conversation by adding html div
     * in the message__item section.
     * @return {void}
     */
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
