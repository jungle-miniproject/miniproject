const signupBtn = document.getElementById('signupBtn');
const password = document.getElementById('userPwd');
const confirmPassword = document.getElementById('confirmPassword');
const passwordError = document.getElementById('passwordError');
const userIdInput = document.getElementById('userId');
const userNameInput = document.getElementById('userName');

signupBtn.addEventListener('click', (e) => {
    e.preventDefault();
    postSignUp();
});

function validateForm() {
    let inputPassword = password.value;
    let inputConfirmPassword = confirmPassword.value;
    if (inputPassword !== inputConfirmPassword) {
        passwordError.textContent = 'Passwords do not match';
        return false;
    } else {
        passwordError.textContent = '';
        return true;
    }
}

const postSignUp = async () => {
    const userId = userIdInput.value;
    const userName = userNameInput.value;
    const userPwd = confirmPassword.value;
    const isValid = validateForm();
    if (!isValidInputLength(userId) || !isValidInputLength(userName) || !isValidInputLength(userPwd)) {
        alert('빈 입력값이 존재합니다!');
        return;
    }
    if (isValid) {
        try {
            const response = await fetch('/signup/api', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: userId, pwd: userPwd, name: userName }),
            });
            const data = await response.json();
            console.log('Response:', data);
            window.location.href = '/login';
        } catch (error) {
            console.error('Error:', error);
        }
    }
};

const isValidInputLength = (text) => {
    return text.length > 0;
};
