$(document).ready(function() {
	$('#div_id_brand').hide();
	$('#div_id_model').hide();

	    // AJAX GET CATEGORY
        $.ajax({
            type: "GET",
            url: "https://api.mercadolibre.com/categories/MCO1743",
            sync: false,
            contentType: "application/json",
            dataType: "jsonp",
            success: function(data) {
            	console.log(data[2]);
            	main_category=data[2]["children_categories"];
            	$('#id_main_category').append('<option value="MCO1743">Selecciona una categoria</option>');
	            for(i = 0; i < main_category.length; i++){
	                $('#id_main_category').append('<option value="'+main_category[i]["id"]+'">'+main_category[i]["name"]+'</option>');
	            }
	            
        	}
        });




    // AJAX GET BRANDS
    $('#id_main_category').change(function(){


    	category=$('select[id=id_main_category]').val();
    	
        $.ajax({
            type: "GET",
            url: "https://api.mercadolibre.com/categories/"+category+"",
            sync: false,
            contentType: "application/json",
            dataType: "jsonp",
            success: function(data) {
            	$('#div_id_main_category').hide();
		    	$('#div_id_brand').show();
            	console.log(data[2]);
            	marcas=data[2]["children_categories"];
            	$('#id_brand').append('<option value="">Todos las marcas</option>');
	            for(i = 0; i < marcas.length; i++){
	                $('#id_brand').append('<option value="'+marcas[i]["id"]+'">'+marcas[i]["name"]+'</option>');
	            }
        	}
        });

    });

    // AJAX GET MODEL
    $('#id_brand').change(function(){
    	brand=$('select[id=id_brand]').val();

        $.ajax({
            type: "GET",
            url: "https://api.mercadolibre.com/categories/"+brand+"",
            sync: false,
            contentType: "application/json",
            dataType: "jsonp",
            success: function(data) {
            	$('#div_id_brand').hide();
    			$('#div_id_model').show();
            	console.log(data[2]);
            	model=data[2]["children_categories"];
            	$('#id_model').append('<option value="">Todos las lineas</option>');
	            for(i = 0; i < model.length; i++){
	                $('#id_model').append('<option value="'+model[i]["id"]+'">'+model[i]["name"]+'</option>');
	            }
        	}
        });

    });

    // AJAX GET LOCATION
        $.ajax({
            type: "GET",
            url: "https://api.mercadolibre.com/countries/CO",
            sync: false,
            contentType: "application/json",
            dataType: "jsonp",
            success: function(data) {
            	console.log(data[2]);
            	states=data[2]["states"];
            	$('#id_location').append('<option value="CO">Selecciona un departamento</option>');
	            for(i = 0; i < states.length; i++){
	                $('#id_location').append('<option value="'+states[i]["id"]+'">'+states[i]["name"]+'</option>');
	            }
        	}
        });



    // AJAX POST
    $('.add-todo').click(function(){
      console.log('am i called');

        $.ajax({
            type: "POST",
            url: "/ajax/add/",
            dataType: "json",
            data: { "item": $(".todo-item").val() },
            success: function(data) {
                alert(data.message);
            }
        });

    });



    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }); 


});