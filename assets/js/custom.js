$(document).ready(function(){

	/*client*/


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


	if ($( "select#id_invoice_type").val() == 'fixed'){
		$('input#id_amount').removeAttr("disabled")
	}else if($( "select#id_invoice_type").val() == 'hourly'){
		$('input#id_hours').removeAttr("disabled")
		$('input#id_start_time').removeAttr("disabled")
		$('input#id_end_time').removeAttr("disabled")
		$('input#id_rate').removeAttr("disabled")

	}


	

	$( "select#id_invoice_type").click(function(){
		var selected = $(this).val();

		if (selected == 'hourly'){
			
			$('input#id_hours').removeAttr("disabled")
			$('input#id_start_time').removeAttr("disabled")
			$('input#id_end_time').removeAttr("disabled")
			$('input#id_rate').removeAttr("disabled")
			$('input#id_amount').attr("disabled", "true")

		}
		if(selected == 'fixed'){

			$('input#id_hours').attr("disabled", "true")
			$('input#id_start_time').attr("disabled", "true")
			$('input#id_end_time').attr("disabled", "true")
			$('input#id_rate').attr("disabled", "true")
			$('input#id_amount').removeAttr("disabled")



		}


	}); 








});
