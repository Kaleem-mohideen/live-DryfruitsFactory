// jQuery(function($){
//     $(document).ready(function(){
//         $("#id_product").change(function(){
//             // console.log(obj.currentTarget.value);
//             $.ajax({
//                 url:"/get_phases/",
//                 type:"POST",
//                 data:{ product: $(this).val(),},
//                 success: function(result) {
//                     console.log(result);
//                     console.log("here")
//                     // cols = document.getElementById("id_phase_select");
//                     // cols.options.length = 0;
//                     // for(var k in result){
//                     //     cols.options.add(new Option(k, result[k]));
//                     // }
//                 },
//                 error: function(e){
//                     console.error(JSON.stringify(e));
//                 },
//             });
//         });
//     }); 
// });



jQuery(function($){
    $(document).ready(function(){

        // console.log(document.getElementById("id_productType"))
        if (document.getElementById("id_productType") != null){
            var clone = document.getElementById("id_productType").cloneNode(true);
            update_productType($("#id_product").val(), clone)
        }
        $("#id_product").change(function(){
            update_productType($(this).val(), clone)
        });
        
    });

    function update_productType(product, clone) {
        $.ajax({
            url:"/get_phases/",
            type:"POST",
            data:{product: product,},
            success: function(result) {
                var cols = document.getElementById("id_productType");
                cols.innerHTML = clone.innerHTML
                Array.from(cols.options).forEach(function(option_element) {
                    console.log(option_element)
                    console.log('result',eval(result))
                    console.log('result',eval(result['includeQuery']))
                    var res = eval(result['includeQuery'])
                    var existing = false;
                    for (var i in res) {
                        // console.log('k', res[k]['pk'])
                        if (option_element.value == res[i]['pk'] || option_element.value == $('#id_productType option:selected').val()) {
                            console.log("True")
                            existing = true
                        }
                    }
                    if (existing == false) {
                        console.log("False")
                        $("#id_productType option[value='"+option_element.value+"']").remove();
                    }
                })
            },
            error: function(e){
                console.error(JSON.stringify(e));
            },
        });
    }
});