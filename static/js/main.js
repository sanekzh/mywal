jQuery(document).ready(function ($) {
    $('#table_of_products').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": '/list_of_products/',
            // "type": "GET"
            'dataSrc': ''
        },
        "columns": [
             // 'columns': [
        //     {'data': 'fields.id', 'orderable': false},
        //     {'data': 'fields.upc', 'orderable': false},
        //     {'data': 'fields.image_product', 'orderable': true},
        //     {'data': 'fields.title', 'orderable': false},
        //     {'data': 'fields.brand_name', 'orderable': false},
        //     {'data': 'fields.in_stock', 'orderable': false},
        //     {'data': 'fields.price', 'orderable': true},
        //     {'data': 'fields.free_shipping', 'orderable': false},
        //     {'data': 'fields.created', 'orderable': true}
        // ]
            // { "data": "id" },
            { "data": "fields.owner"},
            { "data": "fields.upc" },
            { "data": "fields.image_product"},
            { "data": "fields.title" },
            { "data": "fields.brand_name" },
            { "data": "fields.model"},
            { "data": "fields.price" },
            // { "data": "fields.quantity" },
            // { "data": "fields.in_stock" },
            // { "data": "fields.price" },
            // { "data": "fields.free_shipping"},
            // { "data": "fields.is_active" },
            // { "data": "fields.created" },
            // { "data": "fields.update" }
         ],
         'columnDefs': [
            {
                'targets': 2,
                'data': 'fields.image_product',
                'render': function (data, type, full, meta) {
                    return '<img src="' + data + '">';
                }
            }
        ]
        } );

    $('#upc_id').submit(function(event){
        event.preventDefault();
        // var data = $(this).serialize();
        //
        var data = {};
        data.upc = $('#input_upc').val();
        console.log(data.upc);
        var csrf_token = $('#upc_id input[name="csrfmiddlewaretoken"]').val();
        data['csrfmiddlewaretoken'] = csrf_token;
        console.log(csrf_token);
        $.ajax({
            type: "POST",
            url: "/home/",
            dataType:"html",
            data: data,
            cache: false,
            success: function(data){
                if (data == 'ok'){
                   // location.reload();
                }
                else{
                   // $('#error-login').html(data);
                }
            }
       });
    });
});
