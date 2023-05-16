
let socket;
const MARKET=1,LIMIT=2;
let toast_id=1;
let order_type = "MARKET"
let limit_price_holder = $('#buy_price')
function show_toast(msg) {
    // document.getElementById("toast_header").innerHTML = x;
    $(".toast-container").prepend(`<div class="toast toast_${toast_id}"  role="alert" aria-live="assertive" aria-atomic="true">
                                        <div id="toast_header" class="toast-header">
                                            ${msg}
                                        </div>
                                        <div class="toast-body">
                                            <button onclick="dispose_toast(${toast_id})" class="btn btn-danger">Close</button>
                                        </div>
                                    </div>`
    )
    $(`.toast_${toast_id}`).toast('show');
    toast_id+=1;
}

function dispose_toast(id) {
    $(`.toast_${id}`).toast('dispose');
}


$(document).ready(()=>{ 
    
    let data = {email:email};
    socket=io("http://localhost:5000",{data});
 
    socket.on('connect',()=>{ 
        socket.emit('storeInfo', data);
    });

    socket.on('new-user',(data)=>{
        console.log(data.msg);
    })

    socket.on("alert",(data)=>{
        console.log(data);
        show_toast(data.msg);
        notify_on_desktop(data.msg);
    })

    $("#scheduler").on('click',()=>{
        let coin=$("#coin").val();
        let price=$("#price").val();
        let data={coin,price};
        socket.emit("schedule_limit_order",data);
      })
  
      $("#remove").on('click',()=>{
        socket.emit("remove_task");
      })
  
      socket.on("executed",(data)=>{
          let order_id=data.order_id;
          let msg=`Order executed with id : ${order_id}`;
          let url = "/orders/handle_limit_orders/";
          let sent = {
              'order_id' : order_id,
              'price' : data.price,
          } 
          console.log(data);
        $.ajax({
            type: 'GET',
            url: url,
            data: sent,
            success: function (data) {
                notify_on_desktop(msg);
            },
            error: function (data) {
                show_toast('An error occurred.');
            },
        });
        //   show_toast(msg);
      })


    $("#buy_quantity").on('keyup',(e)=>{

        let qty = document.getElementById("buy_quantity").value;
        qty=parseFloat(qty);
        
        let total_price = (current_price*qty).toFixed(3);
        margin_required = document.getElementById("margin_required") 
        if(order_type=="MARKET"){
        margin_required.innerHTML=total_price;
        }
        if(order_type=="LIMIT"){
            limit_price = parseFloat(limit_price_holder.value)
            margin_required.innerHTML =  (limit_price*qty).toFixed(3);
        }
    
    })
    $('#buy_price').on('keyup',(e)=>{
        let qty = document.getElementById("buy_quantity").value;
        qty=parseFloat(qty);
        margin_required = document.getElementById("margin_required") 
        if(order_type=="LIMIT"){
            limit_price = parseFloat(e.target.value)
            
            let margin_price = (limit_price*qty).toFixed(3)
            console.log(limit_price,qty)
            if(isNaN(margin_price)){
                margin_price=0
            }
            margin_required.innerHTML =  margin_price;
        }
    })

    $("#sell_quantity").on('keyup',(e)=>{

        let qty = document.getElementById("sell_quantity").value;
        qty=parseFloat(qty);
        
        let total_price = (current_price*qty).toFixed(3);
    
    })


    $("#buy_form").on('submit',(e)=>{
        e.preventDefault();

        let form = $("#buy_form");
        let url = "/orders/handle_buy/";
        
        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function (data) {

                let order = data.order;
                if(order.order_type==MARKET || data.success==0)
                {
                    let x = data.msg;
                    show_toast(x);
                    notify_on_desktop(x);
                    return;
                }
                show_toast(data.msg);
                notify_on_desktop(data.msg);
                socket.emit('schedule_limit_order',{order,email});                
            },
            error: function (data) {
                show_toast("An error occured.");
            },
        });
    })

    $("#sell_form").on('submit',(e)=>{
        e.preventDefault();

        let form = $("#sell_form");
        let url = "/orders/handle_sell/";

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function (data) {

                let order = data.order;
                if(order.order_type==MARKET || data.success==0)
                {
                    let x = data.msg;
                    show_toast(x);
                    notify_on_desktop(x);
                    return;
                }
                show_toast(data.msg);
                notify_on_desktop(data.msg);
                socket.emit('schedule_limit_order',{order,email});              
            },
            error: function (data) {
                show_toast("An error occured.");
            },
        });
    })


    // for price alerts
    $("#set_alert_btn").on('click',()=>{
          let price=$("#price_alert").val();
          let data={price,coin_symbol,email};
          socket.emit('set_price_alert',data);
    })


    // positions handler
    $(".cancel-btn").on('click',(e)=>{
        let id=e.target.id;
        
        let conf = confirm("Are you sure u want to cancel this order..?");
        if(conf==false)
        return;

        // stop job running from nodejs server
        let data={'id':id};
        socket.emit('remove-order',data);

        // make order status cancelled
        let url='/orders/handle_cancel_order/';
        $.ajax({
            url: url,
            data: data,
            success: function (res) {
                $("#row_"+id).remove();
                show_toast("Order successfully cancelled");
                notify_on_desktop("Order successfully cancelled");
            },
            error: function (res) {
                show_toast("An error occured.");
            },
        });

    })

})