<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link type="text/css" rel="stylesheet" href="/static/style.css">
    <title>{{listname}}</title>
</head>
<body>
  <div class="list_box">
    <div class="list_action_box">
    <table class="list_table">

    <tr class="list_row">
        <th class="list_col_h">Item</th>
        <th class="list_col_h">Elo</th>
        <th class="list_col_h">Actions</th>
    </tr>

    </table>
    </div>
    
    <div class="list_add_box">
    <table class="list_table">

    <tr class="list_row">
        <td class="list_col">
        <form action="/list/{{listname}}" method="post">
        <table class="list_table">
            
            <tr class="list_row">
                <td class="list_col"> 
                <input type="text" class="list_input" id="item" name="item" placeholder="Item"> 
                </td>
                <td class="list_col"> 
                </td>
                <td class="list_col"> 
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
                <tr>
                <td class="list_col"> <p class="item_label">{{item}}</p> </td>
                <td class="list_col"> <p class="item_label">{{data[item]}}</p> </td>
                <td class="list_col"> 
                <button type="submit" class="list_del_button" name="action" value="DEL_{{item}}">Delete</button>
                </td>
                </tr>

        </table>
        </form>
        </td>
      </tr>
      % end
      
    </table>
    </div>

  <div class="list_bottom_box">
    <form action="/list/{{listname}}/clear" method="post">
      <button type="submit" class="list_del_button" name="action" value="CLR">Delete List</button>
    </form>
    <form action="{{listname}}/rank" method="post">
      <button type="submit" class="list_add_button" name="action" value="RNK">Rank Items</button>
    </form>
  </div>

  </div>

</body>
</html>
