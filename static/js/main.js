jQuery(document).ready(function ($) {
    // $("#button_modal_add_product").click(function (e) {
    //  e.preventDefault();
    //     var modal = $("#modal_add_product");  //  Show modal window
    //     modal.style.display = "block";
    //      //  Clear input fields
    // });

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
            { 'data': 'fields.update' }
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
                'data': 'fields.free_shipping',
                'render': function (data, type, full, meta) {
                    var datatime = data.substring(0, 10) + ' ' + data.substring(11, 16);
                    return '<label style="font-weight: normal">' + datatime + '</label>';

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



//     var modal = document.getElementById('modal_add_product');
//
// // Get the button that opens the modal
// var btn = document.getElementById("button_modal_add_product");
//
// // Get the <span> element that closes the modal
// var span = document.getElementsByClassName("close")[0];
//
// // When the user clicks on the button, open the modal
// btn.onclick = function(e) {
//     e.preventDefault()
//     modal.style.display = "block";
// };
//
// // When the user clicks on <span> (x), close the modal
// span.onclick = function() {
//     modal.style.display = "none";
// };
//
// // When the user clicks anywhere outside of the modal, close it
// window.onclick = function(event) {
//     if (event.target == modal) {
//         modal.style.display = "none";
//     }
// };
