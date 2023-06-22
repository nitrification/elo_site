<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{user}}'s lists</title>
</head>
<body>
    <h1>{{signupplz}}</h1>
    %if listz != None: 
        %for i in listz:
    <div class="card">
    <form method="post" action="/list">
        <input type="submit" id="{{i}}" name="list" value="{{i}}">
        <input type="submit" id="remove_{{i}}" name="remove_list" value="Remove">
    </form>
    </div>
        %end
    %end
    <div class="card">
    <form method="post" action="/list">
        <input type="submit" id="add_list" name="add_list" value="Add a list">
    </form>
    </div>
</body>
</html>