'use strict';
$(function() {

    // Display invoice form
    $("a.create-invoice").on('click', function(e) {
      e.preventDefault();
      $("#invView").addClass('hidden');;
      $("#invForm").removeClass('hidden');
    });

    // Ajax view invoice
    $("div.invoice-data").on('click', function(e) {
      e.preventDefault();
      let id = $(this).attr('id').toString();

      $.ajax({
        method: 'GET',
        url: "/invoice/ajax/view/"+id+"",
        dataType: 'json',
        context: $(this),
        success: function (resp) {
          let invData = JSON.parse(resp.invoice);
          let invItems = JSON.parse(resp.items);

          if (invData.length) {
            invData = invData[0];
          }

          let wrapperDiv = $('#invView');
          let invForm = $('#invForm');
          let invNum = $('#invNum');
          let invDesc = $('#invDesc');
          let invClient = $('#invClient');
          let invPayStat = $('#invPayStat');
          let invDueDate = $('#invDueDate');
          let invDate = $('#invDate');
          let invRem = $('#invRem');
          let invSubTotal = $('#invSubTotal');
          let invTotal = $('#invTotal');

          let itemsTbody = $('#itemsTbody');
          let itemsRow = $('#itemsRow');

          wrapperDiv.removeClass('hidden');
          invForm.addClass('hidden');

          let paymentStat = '';
          if (invData.fields.payment_status == false){
            paymentStat = 'unpaid';
          } else if (invData.fields.payment_status == true){
            paymentStat = 'paid';
          }

          let invDueDateData = new Date(invData.fields.due_date);
          let invDateData = new Date(invData.fields.invoice_date);

          let arrInvDate = [];
          let arrDueDate = [];
          let invoiceDate = '';
          let invoiceDueDate = '';
          arrInvDate = String(invDateData).split(' ');
          arrDueDate = String(invDueDateData).split(' ');
          invoiceDate = arrInvDate[1]+' '+arrInvDate[2]+', '+arrInvDate[3];
          invoiceDueDate = arrDueDate[1]+' '+arrDueDate[2]+', '+arrDueDate[3];

          invNum.text(resp.prefix.toUpperCase()+': '+resp.invoice_number);
          invDesc.text(invData.fields.description.charAt(0).toUpperCase()
                       + invData.fields.description.slice(1).toLowerCase()
                      );
          invClient.text(resp.client.toLowerCase()
                                    .replace(/\b[a-z]/g, function(letter) {
                                      return letter.toUpperCase();
                                     }) 
                         );
          invPayStat.text(paymentStat.charAt(0).toUpperCase()+ paymentStat.slice(1).toLowerCase());
          invDueDate.text(invoiceDueDate);
          invDate.text(invoiceDate);
          invRem.text(invData.fields.remarks.charAt(0).toUpperCase()
                      + invData.fields.remarks.slice(1).toLowerCase() 
                     );
          invSubTotal.text(invData.fields.subtotal);
          invTotal.text(invData.fields.subtotal);

          if (invItems.length) {
            itemsTbody.html('');
            for (var i = invItems.length - 1; i >= 0; i--) {
              let newRow = itemsRow.clone();
              newRow.removeClass('hidden');
              newRow.children('.itemDesc').html(invItems[i].fields.description);
              newRow.children('.itemQty').html(invItems[i].fields.quantity);
              newRow.children('.itemRate').html(invItems[i].fields.rate);
              newRow.children('.itemAmount').html(invItems[i].fields.amount);
              itemsTbody.append(newRow);
            }
          }
        },
      })
    });
  });
