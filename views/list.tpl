<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link type="text/css" rel="stylesheet" href="/static/displaylist.css">
    <title>{{listname}}</title>
</head>
<body>
  <div class="list_box">
  <h1>{{listname}}</h1>
    <div class="list_action_box">
        <div class="fake_box" style="width:58%"> <h2>Item</h2> </div>
        <div class="fake_box" style="width:19%"> <h2>Elo</h2> </div>
        <div class="fake_box" style="width:19%"> <h2>Action</h2> </div>
    </div>

    <div class="list_add_box">
    <table class="list_table">

    <tr class="list_row">
        <td class="list_col">
        <form action="/list/{{listname}}" method="post">
        <table class="list_table">
            
            <tr class="list_row">
                <td class="list_td_input" style="width:80%"> 
                <input type="text" class="list_input" id="item" name="item" placeholder="Item"> 
                </td>
                <td class="list_col" style="width:20%"> 
                <button type="submit" class="list_add_button" name="action" value="ADD">Add Item</button>
                </td>
            </tr>
            
        </table>
        </form>
        </td>
    </tr>

    </table>
    </div>
      
    <div class="list_item_box">
    <table class="list_table">

      % for item in data.keys():
      <tr class="list_row">
        <td class="list_col">
        <form action="/list/{{listname}}" method="post">

        <table class="list_table">
                <td class="list_col" style="width:60%"> 
                <div class="fake_button"> <p class="item_label">{{item}}</p> </div> </td>
                <td class="list_col" style="width:20%"> 
                <div class="fake_button"> <p class="item_label">{{data[item]}}</p> </td>
                <td class="list_col" style="width:20%"> 
                <button type="submit" class="list_del_button" name="action" value="DEL_{{item}}">Delete</button>
                </td>

        </table>
        </form>
        </td>
      </tr>
      % end
      
    </table>
    </div>

  <div class="list_bottom_box">
    <form action="{{listname}}/rank" method="post">
      <button type="submit" class="list_b_action_button" name="action" value="RNK">Rank Items</button>
    </form>
  </div>

</div>
</body>
</html>
