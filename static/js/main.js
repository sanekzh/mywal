$(document).ready(function(){
  $("#button_modal_add_product").click(function() {
    $("#myModal").modal('show');
  });
});

$(document).ready(function(){
  $("#export_in_csv").click(function() {
    $("#myModal_export_in_csv").modal('show');
  });
});

$(document).ready(function(){
  $("#import_from_csv").click(function() {
    $("#myModal_import_from_csv").modal('show');
  });
});

function ViewCheck(){
        $('#add_product_ok').removeClass('hidden');
    }
function ViewCheck_remove(){
        $('#add_product_ok').addClass('hidden');
    }
function ViewError(){
    $('#add_product_error').removeClass('hidden');
}
function ViewError_remove(){
    $('#add_product_error').addClass('hidden');
}
jQuery(document).ready(function ($) {
    $('#table_of_products').DataTable({
        'processing': false,
        'serverSide': true,
        'scrollX': true,
        'searching': false,
        'lengthChange': false,
        'ajax': {
            'url': '/list_of_products/',
            'type': 'GET',
            'dataSrc': ''
        },
        'columns': [
            { 'data': 'fields.owner'},
            { 'data': 'fields.upc' },
            { 'data': 'fields.image_product'},
            { 'data': 'fields.title' },
            { 'data': 'fields.brand_name' },
            { 'data': 'fields.model'},
            { 'data': 'fields.price' },
            { 'data': 'fields.quantity' },
            { 'data': 'fields.in_stock' },
            { 'data': 'fields.free_shipping'},
            { 'data': 'fields.created' },
            // { 'data': 'fields.update' },
            { 'data': 'pk' }
         ],
         'columnDefs': [
            {
                'targets': 2,
                'data': 'fields.image_product',
                'render': function (data, type, full, meta) {
                    return '<img src="' + data + '">';
                }
            },
            {
                'targets': 6,
                'data': 'fields.price',
                'render': function (data, type, full, meta) {
                    return '<label>$' + data + '</label>';
                }
            },
            {
                'targets': 8,
                'data': 'fields.in_stock',
                'render': function (data, type, full, meta) {
                    if (data != true) {
                        return '<i class="fa fa-check-circle-o" aria-hidden="true"></i>';
                    }
                    else return '<i class="fa fa-times-circle-o" aria-hidden="true"></i>';
                }
            },
            {
                'targets': 9,
                'data': 'fields.free_shipping',
                'render': function (data, type, full, meta) {
                    if (data != true) {
                        return '<i class="fa fa-check-circle-o" aria-hidden="true"></i>';
                    }
                    else return '<i class="fa fa-times-circle-o" aria-hidden="true"></i>';
                }
            },
            {
                'targets': 10,
                'data': 'fields.free_shipping',
                'render': function (data, type, full, meta) {
                    var datatime = data.substring(0, 10) + ' ' + data.substring(11, 16);
                    return '<label style="font-weight: normal">' + datatime + '</label>';

                }
            },
            {
                'targets': 11,
                'data': 'pk',
                'render': function (data, type, full, meta) {
                    var pid = data;
                    var prod = 'product/';
                    return '<a href="' + prod + pid + '" id="delete_product_link">' +
                                '<i class="fa fa-trash-o" aria-hidden="true"></i></a>';
                }
            }
        ]
        } );

    //************** REQUEST ADD PRODUCT IN TABLE FOR UPC **************
    $('#upc_id').submit(function(event){
        event.preventDefault();
        var form = $('#upc_id');
        var data = {};
        data.upc = $('#input_upc').val();
        var csrf_token = $('#upc_id input[name="csrfmiddlewaretoken"]').val();
        data['csrfmiddlewaretoken'] = csrf_token;
        var url = form.attr("action");
        console.log(url);
        console.log(csrf_token);
        $.ajax({
            type: "POST",
            url: url,
            dataType:"html",
            data: data,
            cache: true,
            success: function(data){
                data = JSON.parse(data);
                console.log('success context = ', data.description);
                if (data.description == 'yes'){
                    ViewError_remove();
                    ViewCheck();
                }
                else if(data.description == 'no') {
                    ViewCheck_remove();
                    ViewError();
                }
            },
            error: function(){
                console.log('error ajax request');
            }
       });
    });
});
