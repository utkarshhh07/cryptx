let portfolio=JSON.parse(document.getElementById('portfolio').textContent);
let api_key = '97345c0932caf03b68d9c0b6b74dcb79dd5462c903ccd9dfb1784081d07cd539';

let pl = new Map();

$(document).ready(function(){
    setInterval(() => {
        changeAllPrices();
    },2000);
});

function changeAllPrices()
{
    
    portfolio.forEach(holding => {
        changeEachCoinPrice(holding);
    });

    let overall_pl=0;
    pl.forEach((value, key) => {
        overall_pl+=value;
    })
    overall_pl=overall_pl.toFixed(2);
    $("#total_pl").html(overall_pl);
    if(overall_pl<0)
    $("#total_pl").css('color','red');
    else if(overall_pl>0)
    $("#total_pl").css('color','green');
}

async function changeEachCoinPrice(holding) {
    
    let coin_name = holding.name;
    let coin_symbol = holding.symbol;
    let currency_name = "USD";

    let real_time_url = `https://min-api.cryptocompare.com/data/price?fsym=${coin_symbol}&tsyms=${currency_name}&api_key=${api_key}`;
    const response = await fetch(real_time_url);
    var data = await response.json();
    let current_price = data.USD;
    // console.log(current_price)
    let quantity = holding.quantity
    let avg_price = holding.avg_price
    let total_pl = (current_price*quantity-avg_price*quantity).toFixed(2)
    let pl_id = "id_p&l_"+coin_symbol;
    let pl_container = document.getElementById(pl_id);
   

    if(total_pl>0)
    {
        pl_container.innerHTML="+"+ total_pl+'<span style="font-size:20px; font-weight:900;">&#8593;</span>';
        pl_container.style.color="green";
       
    }
    else if(total_pl<0)
    {
        pl_container.innerHTML=total_pl+'<span style="font-size:20px; font-weight:900;">&#8595;</span>';
        pl_container.style.color="red";
    }

    total_pl=parseFloat(total_pl);
    total_pl=total_pl
    pl.set(coin_symbol,total_pl);

}

