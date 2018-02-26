'use strict';

let formset = formsetJS();
formset.reIndex();

function invoiceJS() {
  function invoiceForm() {
    // Invoice Form
    displayAddForm();
  }

  function displayAddForm() {
    // Display add form
    $('#id_form-TOTAL_FORMS').val(1);

    let invForm = $('#invForm');
    let invView = $('#invView');

    if (invForm.hasClass('hidden')) {
       invForm.removeClass('hidden');
       invView.addClass('hidden');

    } else {
       invForm.removeClass('hidden');
       invView.addClass('hidden');
    }

    let invNum = $('#id_invoice_number');
    let invDesc = $('#id_description');
    let invClient = $('#id_client');
    let invDate = $('#id_invoice_date');
    let invDueDate = $('#id_due_date');
    let invRemarks = $('#id_remarks');
    let error = $('.error');
    let totalForm = $('#id_form-TOTAL_FORMS').val();
    invNum.val('');
    invDesc.val('');
    invClient.val('');
    invDate.val('');
    invDueDate.val('');
    invRemarks.val('');
    error.text('');

    // formset
    let description = $('.field-description');
    let quantity = $('.field-quantity');
    let rate = $('.field-rate');
    let amount = $('.field-amount');
    let del = $('.field-delete');
    let subtotal = $('#id-sub-total');
    let inpSubtotal = $('#id_subtotal');

    description.children().val('');
    quantity.children().val('');
    rate.children().val('');
    amount.children('span').text(0);
    amount.children('input').val('');
    amount.children('input').attr('type', 'hidden');
    del.children().val('');
    subtotal.text('');
    inpSubtotal.val('')

    // Remove other form except with 0 id
    $('.form-row').each(function(counter) {
      let idFormRow = $(this).attr('id');
      if (idFormRow != 0) {
        $(this).remove();
      }
      $('#id_form-TOTAL_FORMS').val(1);
    });
  }

   return {
    invoiceForm: invoiceForm,
    main: function() {}
   }
}


function invoiceView(id) {
  // Invoice details
  $.ajax({
    method: 'GET',
    url: "/invoice/ajax/view/" + id + "",
    dataType: 'json',
    context: $(this),
    success: function(resp) {

      createInvoice();

      let invData = JSON.parse(resp.invoice);
      let invItems = JSON.parse(resp.items);
      let invNum = $('#invNum');
      let invDesc = $('#invDesc');
      let invClient = $('#invClient');
      let invPayStat = $('#invPayStat');
      let invDueDate = $('#invDueDate');
      let invDate = $('#invDate');
      let invRem = $('#invRem');
      let invSubTotal = $('#invSubTotal');
      let invTotal = $('#invTotal');
      let invURLEdit = $('a[name="invoiceURLEdit"]');
      let totalForm = $('#id_form-TOTAL_FORMS');
      let itemsTbody = $('#itemsTbody');
      let itemsRow = $('#itemsRow');
      let invForm = $('#invForm');
      let invView = $('#invView');

      if (invData.length) {
        invData = invData[0];
      }

      // Display view content
      if (invView.hasClass('hidden')) {
        invView.removeClass('hidden');
        invForm.addClass('hidden');
      } else {
        invView.removeClass('hidden');
        invForm.addClass('hidden');
      }

      let paymentStat = '';
      if (invData.fields.payment_status == false) {
          paymentStat = 'unpaid';
      } else if (invData.fields.payment_status == true) {
          paymentStat = 'paid';
      }

      let invDueDateData = new Date(invData.fields.due_date);
      let invDateData = new Date(invData.fields.invoice_date);
      let arrInvDate = [];
      let arrDueDate = [];
      let invoiceDate = '';
      let invoiceDueDate = '';

      // Display data
      arrInvDate = String(invDateData).split(' ');
      arrDueDate = String(invDueDateData).split(' ');
      invoiceDate = arrInvDate[1] + ' ' + arrInvDate[2] + ', ' + arrInvDate[3];
      invoiceDueDate = arrDueDate[1] + ' ' + arrDueDate[2] + ', ' + arrDueDate[3];

      invNum.text(resp.prefix.toUpperCase() + ': ' + resp.invoice_number);
      invDesc.text(invData.fields.description.charAt(0).toUpperCase() +
                   invData.fields.description.slice(1).toLowerCase()
              );
      invClient.text(resp.client.toLowerCase()
          .replace(/\b[a-z]/g, function(letter) {
              return letter.toUpperCase();
          })
      );
      invPayStat.text(paymentStat.charAt(0).toUpperCase() + paymentStat.slice(1).toLowerCase());
      invDueDate.text(invoiceDueDate);
      invDate.text(invoiceDate);
      invRem.text(invData.fields.remarks.charAt(0).toUpperCase() +
          invData.fields.remarks.slice(1).toLowerCase()
      );
      invSubTotal.text(invData.fields.subtotal);
      invTotal.text(invData.fields.subtotal);

      invURLEdit.attr({
          'href': '/invoice/edit/' + invData.pk + '/' + invItems.length + '/',
          'id': invData.pk,
      });

      if (invItems.length) {
          itemsTbody.html('');
          for (var i = 0; i <= invItems.length - 1; i++) {
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
}

function createInvoice(id) {
  // Create invoice
  let invoice = invoiceJS();
  invoice.invoiceForm();
}

function addOrder() {
  // Add order
  formset.addFormSet();
  formset.reIndex();
  formset.displayRemove();
}

function deleteRowOrder(id) {
  // Delete row order form
  $('a#' + id).parent().parent().remove();
  $('#id_form-TOTAL_FORMS').val(formset.totalForm() - 1);
  //removeForm.remove();
  formset.reIndex();
  formset.computationSubtotal();
}

function qtyCompute(id) {
  // Compute amount when qty is change
  $('.field-quantity').on('keyup', function(event) {
    let rate = $(this).parent().children('.field-rate').children().val();
    let quantity = $(this).children().val();
    let total = parseInt(rate) * parseInt(quantity);

    if (!isNaN(total)) {
      $(this).parent().children('.field-amount').children('span').text(total);
      $(this).parent().children('.field-amount').children('input').val(total);
    } else {
      $(this).parent().children('.field-amount').children('span').text(0);
      $(this).parent().children('.field-amount').children('input').val(0);
    }
    formset.computationSubtotal();
  });
}

function rateCompute(id) {
  // Compute amount when rate is change
  $('.field-rate').on('keyup', function(event) {
    let rate = $(this).children().val();
    let quantity = $(this).parent().children('.field-quantity').children().val();
    let total = parseInt(rate) * parseInt(quantity);

    if (!isNaN(total)) {
      $(this).parent().children('.field-amount').children('span').text(total);
      $(this).parent().children('.field-amount').children('input').val(total);
    } else {
      $(this).parent().children('.field-amount').children('span').text(0);
      $(this).parent().children('.field-amount').children('input').val(0);
    }
    formset.computationSubtotal();
  });
}
