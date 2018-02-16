

  $(document).ready(function() {
    $('input#id_first_name').keyup(function(){
      var f = $(this).val();
      var l = $('input#id_last_name').val()
      $('input#id_display_name').val(f+' '+l);
    });

    $('input#id_last_name').keyup(function(){
      var l = $(this).val();
      var f = $('input#id_first_name').val()
      $('input#id_display_name').val(f+' '+l);
    });

    if ($( "select#id_item_type").val() == 'fixed'){
      $('input#id_amount').removeAttr("disabled")
    }else if($( "select#id_item_type").val() == 'quantity'){
      $('input#id_quantity').removeAttr("disabled")
      $('input#id_rate').removeAttr("disabled")
    }

    $( "select#items").click(function(){
      var selected = $(this).val();
      $('div#item-pick').append('<span>'+selected+'</span>')
    });
  });