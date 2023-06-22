<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title>login</title>
    <link type="text/css" rel="stylesheet" href="/static/loginsignup.css">
</head>
<body>
    <div class="loginbox">
      <h1>Login:</h1>
      <form method="post" action="/login">
          <input type="text"  class="logincredentials" name="username" id="username" placeholder="username">
          </br>
          <input type="password" class="logincredentials" name="password" id="password" placeholder="password">
          </br>
          <input type="submit" class="submitbutton" name="submit_all" value="submit">
          <p></p>
      </form>
      <h2><a href="/index">return home</a> | <a href="/signup">sign up</a></h2>
     </div>
</body>
</html>
