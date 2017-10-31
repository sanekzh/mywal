jQuery(document).ready(function ($) {
    init();

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

function init() {
    console.log('table')
    var productTable = $('#table_of_products').DataTable({
    "bServerSide": true,
    "sAjaxSource": 'list_of_products',
    "bProcessing": true,
    "bLengthChange": true,
    // "bSearching": true,
    "bFilter": true,
    'sDom': 'rtpli',
    "bSortable": false,  // change
    "autoWidth": true,
    "ordering": false,
    "bInfo": true,
    "lengthMenu": [[10, 25, 50, 100], [10, 25, 50, 100]],
    "iDisplayLength": 10
    // "aoColumnDefs": [
    //     {
    //     "mRender": function (data, type, row) {
    //         row.status_filter = '<a class="data_number" href="#">' + row[0] + '</a>';
    //         return row.status_filter;
    //     },
    //     "aTargets": [0]
    //     }
    // ]

    });
    productTable.ajax.reload();
}
// $(document).ready(function () {
//     var form = $('#upc_request');
//     console.log(form);
//
//     form.on('submit', function (event) {
//         event.preventDefault();
//         console.log('123');
//         // var nmb = $('#number').val();
//         // console.log(nmb);
//         // var submit_btn = $('#submit_btn');
//         // var product_id = submit_btn.data('product_id');
//         // var name = submit_btn.data('name');
//         // var product_price = submit_btn.data('product_price');
//         // console.log(product_id);
//         // console.log(name);
// //         // basketUpdaiting(product_id, nmb, is_delete=false);
// //     });
// // });
//
// $(document).ready(function () {
//
//     var form = $('#upc_request');
//     console.log(form);
//     form.on('submit', function (event) {
//         event.preventDefault();
//         console.log('123');
//         var button = document.querySelector("button");
//         button.addEventListener("click", function () {
//         console.log("Кнопка нажата.");
//         });
//     });
// });