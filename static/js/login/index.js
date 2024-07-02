const idInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginButton = document.getElementById('loginBtn');
const signupBtn = document.getElementById('signup');

loginButton.addEventListener('click', (e) => {
    e.preventDefault();
    postLogin();
    window.location.href = '/homepage';
});

signupBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = '/signup';
});

const postLogin = async () => {
    try {
        fetch('https://jsonplaceholder.typicode.com/todos/1')
            .then((response) => response.json())
            .then((res) => console.log(res));
        window.location.href = '/homepage';
    } catch (e) {
        alert('잘못된 유저입니다!');
        return;
    }
};
