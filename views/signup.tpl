<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>Sign up</title>
</head>
<body>
    <h1>Sign Up:</h1>
    <form method="POST" action="/signup">
        <label for="username">Username:</label>
        <input type="text" name="username" id="username" placeholder="Username">
        <br>
        <label for="password">Password:</label>
        <input type="password" name="password" id="password" placeholder="Password">
        <br>
        <label for="cpassword">Confirm Password:</label> 
        <input type="password" name="cpassword" id="cpassword" placeholder="Confirm Password"> 
        <input type="submit" name="submit_all" value="submit">
     </form>
</body>
</html>