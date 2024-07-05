const submitButton = document.getElementById('submitButton');
const messageIcon = document.querySelector('.notification');
const iconChat = document.querySelector('.iconChat');
const idInput = document.getElementById('input-box');

submitButton.addEventListener('click', function () {
    const selectedUserId = idInput.value;
    localStorage.setItem('selectedUserId', selectedUserId);
    window.location.href = '/question';
});
messageIcon.addEventListener('click', (e) => {
    window.location.href = '/inbox';
});

iconChat.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = '/chat';
});

const outBtn = document.getElementById('outBtn');
outBtn.addEventListener('click', function () {
    window.location.href = '/';
});


