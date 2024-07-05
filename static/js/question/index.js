const submitButton = document.getElementById('submitButton');
const messageInput = document.getElementById('message-input');
const messageIcon = document.querySelector('.notification');
const iconChat = document.querySelector('.iconChat');
const outBtn = document.getElementById('outBtn');

submitButton.addEventListener('click', function (e) {
    e.preventDefault();
    const userId = localStorage.getItem('selectedUserId');
    const userMessage = messageInput.value;
    postUserQuestion(userId, userMessage);
});

const postUserQuestion = async (userId, userMessage) => {
    try {
        const response = await fetch('/question/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: userId, msg: userMessage }),
        });
        if (response.ok) {
            window.location.href = '/authChk';
        }
    } catch (e) {
        alert(e);
    }
};

messageIcon.addEventListener('click', (e) => {
    window.location.href = '/inbox';
});

iconChat.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = '/chat';
});

outBtn.addEventListener('click', function () {
    window.location.href = '/';
});
