function quantityMinusPlus(info) {
    const type = info.getAttribute("data-type");
    const slug = info.getAttribute("slug");
    const csrf_token = info.getAttribute("csrf-token");
    const data_field = info.getAttribute("data-field");
    let url;
    if (type == 'minus') {
        url = window.location.origin.concat("/", "quantity-minus-from-cart");
    } else if (type == 'plus') {
        url = window.location.origin.concat("/", "quantity-plus-from-cart");
    }
    $.ajax({
        url: url,
        type: "POST",
        data: {
            'slug': slug,
            'csrfmiddlewaretoken':  csrf_token,
        },
        success: function (data) {
            if (data.quantity) {
                if($('#quantity').length) {
                    $('#quantity'.concat(data_field)).val(data.quantity);
                    $('#total-item-price'.concat(data_field)).html("$".concat(data.total_item_price.toFixed(2)));
                    $('#sub-total').text("$".concat(data.sub_total.toFixed(2)));
                    $('#total-amount-saved').text("$".concat(data.total_amount_saved.toFixed(2)));
                    $('#total').text("$".concat(data.total.toFixed(2)));
                } else if ($('#cart-item-count').length) {
                    $('#cart-item-count').html("<span class='icon-shopping_cart'></span>[".concat(data.cart_item_count, "]"));
                }
            }

            console.log(type);

            if (Boolean(data.remove) == true) {
                $('#order-item'.concat(data_field)).remove();
                $('#sub-total').text("$".concat(data.sub_total.toFixed(2)));
                $('#total-amount-saved').text("$".concat(data.total_amount_saved.toFixed(2)));
                $('#total').text("$".concat(data.total.toFixed(2)));
                console.log('remove: ' + slug);
            }
            
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    })
}
