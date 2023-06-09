<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="/static/comparison.css">
  <title>{{pair[0]}} vs {{pair[1]}}</title>
</head>

<body>
  <h1><a href="/index">Home</a> | <a href="/list">Lists</a> | <a href="/logout">Logout</a></h1>
  <div class="comparison_box">
    <h1>Pick which you prefer more:</h1>
    <form action="/list/{{listname}}/rank" method="post">
      <div class="comparison_box_side">
        <h2>{{pair[0]}}</h2>
        <button type="submit" class="comparison_button" name="action" value="NXT_1">This</button>
      </div>
      <div class="comparison_box_side">
        <h2>{{pair[1]}}</h2>
        <button type="submit" class="comparison_button" name="action" value="NXT_0">This</button>
      </div>
    </form>
  </div>
</body>

</html>
