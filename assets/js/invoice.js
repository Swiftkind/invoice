'use strict';
$(function() {

    // Display invoice form
    $("a.create-invoice").on('click', function(e) {
      e.preventDefault();
      $("div.invoice-box").empty();
      $("div.invoice-box-form").show();
    });

    // Ajax view invoice
    $("div.invoice-data").on('click', function(e) {
      e.preventDefault();
      let id = $(this).attr('id').toString();

      $.ajax({
       method: 'GET',
       url: "/invoice/ajax/view/"+id+"",
       context: $(this),
      })
      .done(function(response){
        let obj = JSON.parse(response.invoice);

        // Create invoice details template
        for (let data in obj) {
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
