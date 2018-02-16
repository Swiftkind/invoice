
  $(document).ready(function() {

    // 
    $("a.create-invoice").on('click', function(e) {
      e.preventDefault();
      $("div.invoice-box").empty();
      $("div.invoice-box-form").show();
    });

    // Total amount calculation
    $('.field-quantity').on('keydown keyup keypress focusout focus', function() {
        var rate = $(this).parent().children('.field-rate').children().val();
        var quantity = $(this).children().val();
        var total = parseInt(rate) + parseInt(quantity);
        $(this).parent().children('.field-amount').children().val(total)
    });
    $('.field-rate').on('keydown keyup keypress focusout focus', function() {
        var rate = $(this).children().val();
        var quantity = $(this).parent().children('.field-quantity').children().val();
        var total = parseInt(rate) + parseInt(quantity);
        $(this).parent().children('.field-amount').children().val(total)
    });


    // Ajax view invoice
    $("div.invoice-data").on('click', function(e) {
      e.preventDefault();
      var id = $(this).attr('id').toString();
      $.ajax({
       method: 'GET',
       url: "/invoice/ajax/view/"+id+"",
       context: $(this),
     })
      .done(function(response){
        var obj = JSON.parse(response.invoice);

        for (var data in obj) {
          $("div.invoice-box-form").hide()
          $("div.invoice-box").empty()
          $("div.invoice-box").append(
            '<div class="col-md-12">'
            +'<br>'
            +'<div class="col-md-8"><label>Invoice Info</label></div>'
            +'<div class="col-md-4">          '
            +'<a href="#" class="btn">Edit</a>'
            +'<a href="#">Delete</a>'
            +'<a href="#" target="_blank">|Generate PDF|</a>'
            +' <a href="#">Send</a>'
            +'</div>'
            +'<br>'
            +'<hr>'
            +'</div>'
            +'<div class="col-md-12">'
            +'<div class="col-md-3">'
            +' <label >Invoice #:</label>'
            +' </div>'
            +' <div class="col-md-9">'
            +obj[data].fields.invoice_number
            +' </div>'
            +' </div>'
            +'<div class="col-md-12">'
            +'<div class="col-md-3">'
            +' <label >Client:</label>'
            +' </div>'
            +' <div class="col-md-9">'
            +obj[data].fields.client
            +' </div>'
            +' </div>'
            +'<div class="col-md-12">'
            +'<div class="col-md-3">'
            +' <label >Item/s :</label>'
            +' </div>'
            +' <div class="col-md-9">'
            +obj[data].fields.item
            +' </div>'
            +' </div>'
            +'<div class="col-md-12">'
            +'<div class="col-md-3">'
            +' <label >Invoice date:</label>'
            +' </div>'
            +' <div class="col-md-9">'
            +obj[data].fields.invoice_date
            +' </div>'
            +' </div>'
            +'<div class="col-md-12">'
            +'<div class="col-md-3">'
            +' <label >Due date:</label>'
            +' </div>'
            +' <div class="col-md-9">'
            +obj[data].fields.due_date
            +' </div>'
            +' </div>'
            +'<div class="col-md-12">'
            +'<div class="col-md-3">'
            +' <label >Remarks :</label>'
            +' </div>'
            +' <div class="col-md-9">'
            +obj[data].fields.remarks
            +' </div>'
            +' </div>'
            )
        }
      });
    });
  });
