$(document).ready(()=>{
let sorting_state="latest";
    $("input[type=radio]").on('click',(e)=>{
        setFilters();
    })
    $("input[name=coin_name]").on('keyup',(e)=>{
        setFilters();
    })

    function  setFilters() {
        let filter1 = $("input[name=mode]").filter(":checked").val();
        let filter2 = $("input[name=status]").filter(":checked").val();
        let filter3 = $("input[name=type]").filter(":checked").val();
        let filtered=$("tr").filter("."+filter1).filter("."+filter2).filter("."+filter3);

        let filter4 = $("input[name=coin_name]").val();

        let arr = filter4.split(" ");

        arr.forEach((filter)=>{
            if(filter.length>0 && filter!=" ")
            {
                filter=filter.toUpperCase();
                filtered=filtered.filter("."+filter);                
            }
        })

        $(".all").hide();        

        filtered.show();
    }
})