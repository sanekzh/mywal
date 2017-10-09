// $(document).ready(function () {
//     var form = $('#upc_id');
//     console.log(form);
//     form.click('submit', function (event) {
//         event.preventDefault();
//         console.log('123');
//         var upc_id = $('#input_upc').val();
//         console.log(upc_id);
//     });
//
//
// });
//
// jQuery(document).ready(function () {
//     var form = $('#upc_id');
//     console.log('jQuery working!');
//     form.on('submit', function (event) {
//         event.preventDefault();
//         console.log('123');
//
//
//     });
//
// });
jQuery(document).ready(function ($) {
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
            // data: {
            //     // data1: data1,
            //     "param": '123',
            //     "csrfmiddlewaretoken": $('#profile_form input[name=csrfmiddlewaretoken]').val()
            // },
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