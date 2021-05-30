function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

/**
 * Checks whether the current page is the Login page.
 * @returns True if the page is either the Login page
 */
function isAgentPage() {
  return document.getElementById('agent-page') != undefined;
}

window.onload = () => {
  // if we are in the login page, do not do a check. they have to login first.
  if (isAgentPage()) return;
  const status = getCookie('isLoggedIn');
  if (status === "") {
    alert("You are not logged in to the Agent Portal.");
    window.location.href = '/';
  }
}

/**
 * Checks the credentials input and redirects to the Agent portal on 
 * successful credentials.
 * @returns Redirects to the agent page on a successful match
 */
function login() {
  if (!isAgentPage()) return;
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  if (username.toLowerCase() !== 'specialagentoso' || password.toLowerCase() !== 'dora123') {
    alert("Your username/password is incorrect");
    return;
  }
  document.cookie = `isLoggedIn=true; expires=${new Date().getTime() + (5 * 60 * 1000)}`;
  window.location.href = '/agent';
}
