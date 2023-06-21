<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>login</title>
</head>
<body>
    <h1>Login:</h1>
    <form method="POST" action="/login">
        <label for="username">Username:</label>
        <input type="text" name="username" id="username" placeholder="Username">
        <br>
        <label for="password">Password:</label>
        <input type="password" name="password" id="password" placeholder="Password">
        <br>
        <input type="submit" name="submit_all" value="submit">
     </form>
</body>
</html>