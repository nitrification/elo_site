<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8" />
    <title>Sign up</title>
    <link type="text/css" rel="stylesheet" href="/static/loginsignup.css">
</head>
<body>
    <div class="loginbox">
    <h1>Sign Up:</h1>
    <form method="post" action="/signup">
        <input type="text" class="logincredentials" name="username" id="username" placeholder="Username">
        <br>
        <input type="password" class="logincredentials" name="password" id="password" placeholder="Password">
        <br>
        <input type="password" class="logincredentials" name="cpassword" id="cpassword" placeholder="Confirm Password"> 
        <input type="submit" class="submitbutton" name="submit_all" value="submit">
        <br>
        <p></p>
     </form>
     <h2><a href="/index">return home</a></h2>
    </div>
</body>
</html>
