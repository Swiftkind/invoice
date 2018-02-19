'use strict';

let formset = function() {

  let totalForm = Number( $('#id_form-TOTAL_FORMS').val() );
  let totalFormCounter;
  let arr = []
    

  let amountComputation = function(){
    // Total amount calculation
    $('.field-quantity').on('keydown keyup keypress focusout focus', function() {
        let rate = $(this).parent().children('.field-rate').children().val();
        let quantity = $(this).children().val();
        let total = parseInt(rate) * parseInt(quantity);

        if (!isNaN(total)){
          $(this).parent().children('.field-amount').text(total);
        }
    });
    $('.field-rate').on('keydown keyup keypress focusout focus', function() {
        let rate = $(this).children().val();
        let quantity = $(this).parent().children('.field-quantity').children().val();
        let total = parseInt(rate) * parseInt(quantity);

        if (!isNaN(total)){
          $(this).parent().children('.field-amount').text(total);
        }
    });
  }

  // Display created elements
  for(let counter=0; counter < totalForm; counter++){
    let rowForm = $('.row-item').find('input[name="form-'+counter+'-description"]').parent().parent().attr('id',counter);
    let del =  $('.form-row#'+counter).find('.field-delete').children().attr('id','id_form-'+counter+'-delete');

    // Add remove text
    if ( del.attr('id') != 'id_form-0-delete'){
      del.text('remove');
    }

    let rate =  $('.form-row#'+counter).find('.field-rate').children().val();
    let quantity =  $('.form-row#'+counter).find('.field-quantity').children().val();
    let total = parseInt(rate) * parseInt(quantity);

    if (!isNaN(total)){
      $('.form-row#'+counter).find('.field-amount').text(total);
    }

   // Delete order form
    $('a#id_form-'+counter+'-delete').on('click', function(){
      let totalForm = Number( $('#id_form-TOTAL_FORMS').val() );
      let newTotalForm = $('#id_form-TOTAL_FORMS').val(totalForm-1) ;
      if ( $(this).attr('id') != 'id_form-0-delete' ) {
        let removeForm = $(this).parent().parent();
        removeForm.remove();
      }
     });

    amountComputation();

    // Sub-t0tal computation
     $('.field-amount').each(function(counter){
       arr[counter] = Number( $(this).text() )
      });
     let subTotal = 0
     for(let counter=0; counter<totalForm; counter++){
       subTotal += arr[counter];
     }
     $('.sub-total').text(subTotal)
  }

  // Add order form
  $('a.add-order').on('click', function(){
    let totalForm = Number( $('#id_form-TOTAL_FORMS').val() );
    let newTotalForm = $('#id_form-TOTAL_FORMS').val(totalForm+1) ;
    totalFormCounter = newTotalForm

    for(let counter=totalForm; counter < newTotalForm.val(); counter++){
      let lastForm = $('.row-item').find('.form-row:last');
      let newForm = lastForm.clone().attr('id', totalForm);
      let prevNo = totalForm-1

      newForm.find('input[name="form-'+prevNo+'-description"]')
             .attr({name: 'form-'+totalForm+'-description', 
                    id:'id_form-'+totalForm+'-description',
              });

      newForm.find('input[name="form-'+prevNo+'-quantity"]')
             .attr({name: 'form-'+totalForm+'-quantity', 
                    id:'id_form-'+totalForm+'-quantity',
              });

      newForm.find('input[name="form-'+prevNo+'-rate"]')
             .attr({name: 'form-'+totalForm+'-rate', 
                    id:'id_form-'+totalForm+'-rate',
              });

      newForm.find('[name="form-'+prevNo+'-amount"]')
             .attr({name: 'form-'+totalForm+'-amount', 
                    id:'id_form-'+totalForm+'-amount',
              });

      newForm.find('a[id="id_form-'+prevNo+'-delete"]')
             .attr({id:'id_form-'+totalForm+'-delete',})
             .text('remove');

      newForm.find('input').val('');
      newForm.find('div.field-amount').text('');
      newForm.insertAfter($('.form-row:last'));

      // Delete order form
      $('a#id_form-'+totalForm+'-delete').on('click', function(){
        let totalForm = Number( $('#id_form-TOTAL_FORMS').val() );
        let newTotalForm = $('#id_form-TOTAL_FORMS').val(totalForm-1) ;
        if ( $(this).attr('id') != 'id_form-0-delete' ) {
          let removeForm = $(this).parent().parent();
          removeForm.remove();
          let maxHitTotalForm = Number(totalFormCounter.val() )+1;
          $('.form-row').each(function (counter) {
            $(this).attr('id', counter) ;
          });
        }
       // Sub-t0tal computation
       $('.field-amount').each(function(counter){
         arr[counter] = Number( $(this).text() )
        });
       let subTotal = 0
       for(let counter=0; counter<totalForm; counter++){
         subTotal += arr[counter];
       }
       $('.sub-total').text(subTotal)
       });

      amountComputation();

      // Sub-t0tal computation
       $('.field-amount').each(function(counter){
         arr[counter] = Number( $(this).text() )
        });
       let subTotal = 0
       for(let counter=0; counter<totalForm; counter++){
         subTotal += arr[counter];
       }
       $('.sub-total').text(subTotal)
      
    }
  });
};

