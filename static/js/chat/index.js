document.addEventListener('DOMContentLoaded', function () {
    const socket = io('http://localhost:5001');
    const sendBtn = document.getElementById('sendbutton');
    const msgInput = document.getElementById('myMessage');
    const messageList = document.getElementById('messages');
    const homeBtn = document.getElementById('outBtn');

    socket.on('connect', function () {
        socket.emit('my event', { data: "I'm connected!" });
    });

    socket.on('message', function (msg) {
        const senderId = msg.senderId;
        const myId = socket.id;
        const message = msg.message;
        const li = document.createElement('p');
        li.textContent = msg.message;
        li.classList.add('inputLabel');
        const nameTage = document.createElement('p');
        if (senderId === myId) {
            li.classList.add('my');
            nameTage.innerHTML = '나';
            nameTage.classList.add('myname');
        } else {
            nameTage.innerHTML = '익명';
            nameTage.classList.add('othername');
            li.classList.add('other');
        }
        messageList.appendChild(nameTage);
        messageList.appendChild(li);
        messageList.scrollTop = messageList.scrollHeight;
    });

    function sendMessage() {
        const message = msgInput.value;
        if (message !== '') {
            socket.send(message);
            msgInput.value = '';
        }
    }

    msgInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    homeBtn.addEventListener('click', function () {
        window.location.href = '/home';
    });
});
