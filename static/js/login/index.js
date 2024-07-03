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

const postLogin = () => {
  const userId = idInput.value;
  const userPwd = passwordInput.value;
  $.ajax({
    type: "POST",
    url: "/loginJWT",
    contentType: "application/json",
    data: JSON.stringify({ id: userId, pwd: userPwd }),
    success: function (response) {
      console.log(response);
      let access_token = response["token"];
      console.log(access_token);
      if (response["result"] == "success") {
        localStorage.setItem("token", access_token);
        window.location.href = "/homepage";
      } else {
        alert(response["msg"]);
      }
    },
  });
};
