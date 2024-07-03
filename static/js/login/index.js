const idInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const loginButton = document.getElementById("loginBtn");
const signupBtn = document.getElementById("signup");

loginButton.addEventListener("click", (e) => {
  e.preventDefault();
  postLogin();
});

signupBtn.addEventListener("click", (e) => {
  e.preventDefault();
  window.location.href = "/signup";
});

const postLogin = async () => {
  const userId = idInput.value;
  const userPwd = passwordInput.value;
  const response = await fetch("/loginJWT", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: userId, pwd: userPwd }),
  });
  if (response.ok) {
    let token = response["token"];
    console.log(token);
    console.log("response", response);
    window.location.href = "/homepage";
  } else {
    alert("아이디 또는 비밀번호가 틀렸습니다.");
  }
};
