
let modal_drag_area ;
let px,py;
let added = false;
ACTIVE_MODAL = true;
$(document).ready(()=>{
    // console.log("draggable_js_start")

    buy_btn = document.getElementById('buy_btn_btn')
    sell_btn = document.getElementById('sell_btn_btn')
    // console.log(buy_btn)
    buy_btn.addEventListener('click',onBuyClick)
    sell_btn.addEventListener('click',onSellClick)
    window.addEventListener('mouseup',removeMouseDrag)
    console.log("draggable_js_end")
}
);
function ModalChange(){
    modal_drag_area =getDraggableArea();
    modal = getModal();
    modal_drag_area.addEventListener('mousedown',addMouseDrag)
     offsety = modal.getBoundingClientRect().top;
     offsetx = modal.getBoundingClientRect().left;
    modal_drag_area.style.cursor="grab"
    modal.style.userSelect  = "None";
    // modal_drag_area.style.color = "red"
}
function onBuyClick(){
    // console.log('buy clicked')
    ACTIVE_MODAL = true;
    ModalChange()
}
function onSellClick(){
    // console.log('sell clicked')
    ACTIVE_MODAL = false
    ModalChange()
}
function getModal(){
    modal_grp = document.getElementsByClassName('draggable-modal');
    if(ACTIVE_MODAL){
        return modal_grp[0]
    }else{
        return modal_grp[1];
    }
}
function getDraggableArea(){
    modal_grp = document.getElementsByClassName('modal-drag-area');
    if(ACTIVE_MODAL){
        return modal_grp[0]
    }else{
        return modal_grp[1];
    }
}
function addMouseDrag(){
    // console.log('Mouse down')
    if(!added){
       
    modal.addEventListener('mousemove',dragModal)
    added=true;
    
}

}
function removeMouseDrag(){
    if(added){
    // console.log(' mouse up')
    modal.removeEventListener('mousemove',dragModal)
    added=false;
    

}
}
function dragModal(e){
    
    mousey = e.movementY;
    // mousey = mousey<0?-5:(mousey==0)?0:5;
    mousex = e.movementX;
    // mousex = mousex<0?-5:(mousex==0)?0:5;
    // console.log(modal.style.left,    offsetx,mousex        )
    // calcx = offsetx + mousex/
    
    offsetx+= mousex;
    offsety+= mousey;
    modal.style.left =offsetx +"px";
    modal.style.top = offsety +"px";
    // modal.style.user-select = 
}