<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Table</title>
</head>
<body>
    <H1>Enter your items below!</H1>
    <form action="/table" method="POST">
        <input type="text" name="item" placeholder="item">
        <input type="submit">
    </form>
    <ul>
        % for item in item_list:
            <li>{{ item }}</li>
        % end
        </ul>
</body>
</html>