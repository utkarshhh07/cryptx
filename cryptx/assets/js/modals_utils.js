$(document).ready(() => {
    let isBuy = true
    console.log($("input[name=order_type]"))
    $('#buy_btn_btn').on('click', (e) => {
        console.log('Buy Clicked')
        isBuy = true
    })
    $('#sell_btn_btn').on('click', (e) => {
        console.log('Sell Clicked')
        isBuy = false
    })
    $("input[name=order_type]").on('click', (e) => {
        
        let type = e.target.value;
        if(isBuy){
        if (type == "MARKET") {
            order_type="MARKET"
            $("#buy_price").attr('disabled', true);
            document.getElementById('buy_price').value = current_price;
        }
        else {
            order_type="LIMIT"
            $("#buy_price").removeAttr('disabled');
        }
    }
    else{
        if (type == "MARKET") {
            $("#sell_price").attr('disabled', true);
            document.getElementById('sell_price').value = current_price;
        }
        else {
            $("#sell_price").removeAttr('disabled');
        }
    }
    })

   

})