document.addEventListener('DOMContentLoaded', function () {
    const socket = io('http://3.35.140.49:5001');
    const sendBtn = document.getElementById('sendbutton');
    const msgInput = document.getElementById('myMessage');
    const messageList = document.getElementById('messages');

    socket.on('connect', function () {
        socket.emit('my event', { data: "I'm connected!" });
    });

    socket.on('message', function (msg) {
        const senderId = msg.senderId;
        const myId = socket.id;
        const message = msg.message;
        console.log('msg', msg);
        console.log('메세지', message);
        const li = document.createElement('p');
        li.textContent = msg.message;
        li.classList.add('inputLabel');
        const nameTage = document.createElement('p');
        if (senderId === myId) {
            console.log('내꺼');
            li.classList.add('my');
            nameTage.innerHTML = '나';
            nameTage.classList.add('myname');
        } else {
            console.log('남의꺼');
            nameTage.innerHTML = '익명';
            nameTage.classList.add('othername');
            li.classList.add('other');
        }
        messageList.appendChild(nameTage);
        messageList.appendChild(li);
        // 메시지 리스트의 스크롤을 최신 메시지로 이동
        messageList.scrollTop = messageList.scrollHeight;
        console.log('socket id 내꺼', socket.id);
    });

    function sendMessage() {
        const message = msgInput.value;
        if (message !== '') {
            socket.send(message);
            msgInput.value = '';
        }
    }

    sendBtn.addEventListener('click', sendMessage);

    msgInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
