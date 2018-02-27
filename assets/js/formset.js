'use strict';

function formsetJS() {

  function clone(getLastForm) {
    // Clone a form
    let cloneForm = getLastForm.clone();
    cloneForm.find('.field-description').children('input').val('');
    cloneForm.find('.field-quantity').children('input').val('');
    cloneForm.find('.field-rate').children('input').val('');
    cloneForm.find('.field-amount').children('input').val('');
    cloneForm.find('.field-quantity').children('input').attr('placeholder', '0');
    cloneForm.find('.field-rate').children().attr('placeholder', '0');
    cloneForm.find('.field-amount').children('span').text('0');
    cloneForm.find('.field-amount').children('input').attr('placeholder', '0');
    return cloneForm
  }

  function totalForm() {
    // Get latest total form
    return Number($('#id_form-TOTAL_FORMS').val())
  }

  function insert(lastForm, newForm) {
    // Insert a form
    newForm.insertAfter(lastForm);
  }

  function getLastForm() {
    // Get the last form
    return $('.form-row:last');
  }

  function addFormSet() {
    // Add order form
    let cloneForm = clone(getLastForm());
    $('#id_form-TOTAL_FORMS').val(totalForm() + 1);
    insert(getLastForm(), cloneForm);
  }

  function computationSubtotal() {
      // Sub-t0tal computation
    let arr = [];
    let subTotal = 0
    let totalForm = Number($('#id_form-TOTAL_FORMS').val());
    $('.field-amount').each(function(counter) {
      arr[counter] = Number($(this).children('input').val());
    });
    
    for (let counter = 0; counter < totalForm; counter++) {
      subTotal += arr[counter];
    }
    $('#id-sub-total').text(subTotal);
    $('input#id_subtotal').val(subTotal);
  }

  function reIndex() {
    // Re index order form id and name
    $('.form-row').each(function(counter) {

      let description = $(this).find('.field-description');
      let quantity = $(this).find('.field-quantity');
      let rate = $(this).find('.field-rate');
      let amount = $(this).find('.field-amount');
      let del = $(this).find('.field-delete');

      $(this).attr('id', counter);
      $(this).children('input').attr({
          'id': 'id_form-' + counter + '-id',
          'name': 'form-' + counter + '-id'
      });

      description.children().attr({
          'id': 'id_form-' + counter + '-description',
          'name': 'form-' + counter + '-description'
      });
      quantity.children().attr({
          'id': 'id_form-' + counter + '-quantity',
          'name': 'form-' + counter + '-quantity'
      });
      rate.children().attr({
          'id': 'id_form-' + counter + '-rate',
          'name': 'form-' + counter + '-rate'
      });
      amount.children('span').attr({
          'id': 'id_form-' + counter + '-amount',
          'name': 'form-' + counter + '-amount'
      });
      amount.children('input').attr({
          'id': 'id_form-' + counter + '-amount',
          'name': 'form-' + counter + '-amount'
      });
      del.children().attr({
          'id': 'id_form-' + counter + '-delete',
          'name': 'form-' + counter + '-delete'
      });

      let qty = Number(quantity.children().val());
      let rte = Number(rate.children().val());
      amount.children('span').text(qty * rte);
      amount.children('input').val(qty * rte);

      displayRemove();
      computationSubtotal() ;
    });
  }

  function displayRemove() {
    // Display remove link
    let del = $('.field-delete');
    del.each(function() {
      if ($(this).children('a').attr('id') != 'id_form-0-delete') {
          $(this).children('a').text('remove');
      }
    });
  }

  return {
    totalForm: totalForm,
    addFormSet: addFormSet,
    clone: clone,
    computationSubtotal: computationSubtotal,
    reIndex: reIndex,
    displayRemove: displayRemove,
    main: function() {}
  }
}