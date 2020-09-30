let x = {'x_poli': 6, 'x_fasil' : 6};
let size_li = $("#poliklinik li").length;
let size_li_fasilitas = $("#fasilitas li").length;

$(document).ready(function () {
    show_hide('#poliklinik', '#showmore', size_li, x['x_poli'])
    show_hide('#fasilitas', '#show_more', size_li_fasilitas, x['x_fasil'])
})

function show_hide(id1, id2, size_li, x){
    $(id1+' li:lt('+size_li+')').hide();
    $(id1+' li:lt('+x+')').show();

    if(size_li <= x){
        $(id2).hide()
    }
}

function showmore(id1, id2, size_li, x_params){
    x[x_params] = (x[x_params]+5 <= size_li) ? size_li : x[x_params]+5;
    $(id1+' li:lt('+x[x_params]+')').show();
    $(id2).html('show less')
}

function showless(id1,id2, x_params){
    x[x_params] = (x[x_params]-5<0) ? x[x_params]-5 : 6;
    $(id1+' li').not(':lt('+x[x_params]+')').hide();
    $(id2).html('show more')
}

$('#showmore').on('click', function () {
    if(x['x_poli'] < size_li){
        showmore('#poliklinik', this, size_li, 'x_poli')
    }else{
        showless('#poliklinik', this, 'x_poli')
    }
})

$('#show_more').on('click', function () {
    if(x['x_fasil'] < size_li_fasilitas){
        showmore('#fasilitas', this, size_li_fasilitas, 'x_fasil')
    }else{
        showless('#fasilitas', this, 'x_fasil')
    }
})