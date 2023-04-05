// var updateBtns = document.getElementsByClassName("update-cart");

// for (i = 0; i < updateBtns.length; i++) {
//     updateBtns[i].addEventListener('click', function(){
//         var productId = this.dataset.product
//         var action = this.dataset.action
//         console.log('productId:', productId, 'Action:', action)
//         console.log('USER:', user)

//         if (user == 'AnonymousUser'){
//             addCookieItem(productId, action)
//         }else{
//             updateUserOrder(productId, action)
//         }

//     })

// }
$(document).ready(function(){
$('body').on('click','.update-cart',function(){

        var x3 = true;
        var productId = $(this).data('product');
        var action = $(this).data('action');
        var wholesale = $(this).data('wholesale');


        if(location.pathname == "/cart/" || location.pathname.startsWith("/productsingle/") ){
            var $button = $(this);
            const min = $button.closest('.quantity').find("input.quantity-count").attr('min');
            const max = $button.closest('.quantity').find("input.quantity-count").attr('max');
            const value = $button.closest('.quantity').find("input.quantity-count").val();

            if(location.pathname == "/cart/"){

            if( (parseInt(value) > parseInt(max) && action == "add") || parseInt(value) < parseInt(min) ){
                // $(this).closest('.quantity').find("input.quantity-count").val(value-1);
                x3 = false;



            }
        }else if(location.pathname.startsWith("/productsingle/")){

            if( (parseInt(value) > parseInt(max) && action == "add") || parseInt(value) < parseInt(min) ){

                x3 = false;
        }

        }

        }
        if (user == 'AnonymousUser' && x3){
            console.log("AnonymousUser")
            addCookieItem(productId, action, wholesale)
        }else if(x3) {
            updateUserOrder(productId, action, wholesale)
        }

});




function updateUserOrder(productId, action, wholesale){

    if(location.pathname.startsWith("/productsingle/")){

                var weight = document.getElementById('selectedweight' +productId);
                var strweight = weight.options[weight.selectedIndex].value;


            }

        if (typeof strweight === "undefined"){
            var strweight = 0;
        }



        var url = "/update_item/";
        $('.loading-spinner').show();
        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'productId':productId, 'action':action, 'wholesale': wholesale, 'strweight': strweight})

        })
        .then((response) => {
           return response.json();
        })
        .then((data) => {
            console.log(data)
            var quantityCount = $('#quantity-count'+data["subproduct_id"]).val();
            $('.loading-spinner').hide();
            if(quantityCount == 0 || action == 'delete'){
                $('.cart-productlist'+data["subproduct_id"]).html('');
            }else{
                $('.offer-price'+data["subproduct_id"]).html(data[data["subproduct_id"]]);
                $('.actual-price'+data["subproduct_id"]).html(data[data["subproduct_id"]+"actual_price"]);

            }

            // if(location.pathname == "/cart/"){
            //     update_CartProducts(data)
            // }


            $('.cart-count').html(data.cartItems);
            $('.sub_total').html(data['get_cart_total']);
            $('.actual_sub_total').html(data['get_cart_actual_total']);
            $('.total_savings').html(data['get_cartSavingsfrom_actual_total']);
            $('.total').html(data['get_cart_total_with_deliverycharge']);
            $('.deliveryCharge').html(data['deliverycharge']);
            $('.GST').html(data['gstcharge']);
            var cartCount = $('.cart-count').text();
            if (cartCount != 0) {
                $('.cart-count').css('transform', 'scale(1)');
            }

        });


}

function update_CartProducts(data) {
    //         $('.cart-section').html('').load(
    //             "/cart/"
    // );
      }

function addCookieItem(productId, action, wholesale){

    console.log("wholesale",wholesale);
    console.log(typeof(wholesale));

    $('.loading-spinner').show();


    if(location.pathname.startsWith("/productsingle/")){

                var weight = document.getElementById('selectedweight' +productId);
                var strweight = weight.options[weight.selectedIndex].value;
            }
    if(location.pathname == "/cart/"){
        var previousQuantity = cart[productId][wholesale]['quantity']
    }
    if (typeof strweight === "undefined"){
            var strweight = 0;
        }

    if (action == 'add'){

        if (cart[productId] == undefined){
            console.log(wholesale);
            cart[productId] = {};
            cart[productId][wholesale] = {'quantity':1}

        }else{
            if (cart[productId][wholesale] == undefined){
                cart[productId][wholesale] = {'quantity':1}
            }else{
                cart[productId][wholesale]['quantity'] += 1
            }

        }
        $('.cart-count').html(function (i, val) {
                        return val * 1 + 1;
                    });
    } else if(action == 'remove'){
        cart[productId][wholesale]['quantity'] -= 1

        if (cart[productId][wholesale]['quantity'] <= 0){

            delete cart[productId][wholesale];
        }
        $('.cart-count').html(function (i, val) {
                        return val * 1 - 1;
                    });
    } else if(action == 'delete'){
            delete cart[productId][wholesale];

    }
    var cartCount = $('.cart-count').text();
            if (cartCount != 0) {
                $('.cart-count').css('transform', 'scale(1)');
            }

    if (location.pathname != "/cart/" && productId in cart && wholesale in cart[productId] && 'quantity' in cart[productId][wholesale] ){
        if (cart[productId][wholesale]['quantity'] >0){
        cart[productId][wholesale]['selectedweight'] = strweight
        }
    }

    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

    // location.reload()
    $('.loading-spinner').hide();
    if(location.pathname == "/cart/"){

        $('.loading-spinner').show();


        function quantitysum(){
            var totalquantity = 0;
            for (var productId in cart){
                for (var wholesale in cart[productId]){
                    console.log( productId, cart[productId][wholesale]['quantity'] );
                    totalquantity += cart[productId][wholesale]['quantity']
                }

            }
            console.log(totalquantity)
            return totalquantity;
        }
        $('.items').html(quantitysum());


        var url = "/process_order/";
        $.ajax({

        url: url,
        headers:{
                'Content-Type':'application/json; charset=utf-8',
                'X-CSRFToken':csrftoken,
            },

        type: 'POST',
        data: JSON.stringify({'productId':productId, 'action':action, 'wholesale':wholesale}),
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        success: function (res, status) {

            if(action == 'delete'){

                $('.cart-productlist'+res['subprodId']).html('');
            }

        // console.log(typeof res)
        console.log(res)
        console.log(eval(res['items']))

            var quantityCount = $('#quantity-count'+res['subprodId']).val();
            var oldPrice = $('.offer-price'+res['subprodId']).text();
            var oldPrice1 = $('.actual-price'+res['subprodId']).text();
            console.log("quan",quantityCount);
            console.log("oldprice",oldPrice);
            // var updatedPriceold = $('.actual-price').text();
            var newPrice = (oldPrice/ previousQuantity) * parseFloat(quantityCount);
            var newPrice1 = (oldPrice1/ previousQuantity) * parseFloat(quantityCount);
            $('.loading-spinner').hide();
            if(quantityCount == 0){
                $('.cart-productlist'+res['subprodId']).html('');
            }else{
            $('.offer-price'+res['subprodId']).html(newPrice);
            $('.actual-price'+res['subprodId']).html(newPrice1);
            }


        // $('.loading-spinner').hide();
        $('.sub_total').html(res['order']['get_cart_total']);
        $('.actual_sub_total').html(res['order']['get_cart_actual_total']);
        $('.total_savings').html(res['order']['get_cartSavingsfrom_actual_total']);
        $('.total').html(res['order']['get_cart_total_with_deliverycharge']);
        $('.deliveryCharge').html(res['order']['deliverycharge']);
        $('.GST').html(res['order']['gstcharge']);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(textStatus);
            alert(XMLHttpRequest.status);
            alert(errorThrown)
        }
      });

    }



}
});
