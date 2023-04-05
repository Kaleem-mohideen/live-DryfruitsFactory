$(document).ready(function(){
	$('.loading-spinner').hide();
	new WOW().init();
	$(document).on('hidden.bs.modal', function () {
		if ($('.modal.show').length) {
			$('body').addClass('modal-open');
		}
	});
	var $easyzoom = $('.easyzoom').easyZoom();

                // Setup thumbnails example
                var productImage = $easyzoom.filter('.easyzoom--with-thumbnails').data('easyZoom');

                $('.thumbnails').on('click', 'a', function (e) {
                    var $this = $(this);

                    e.preventDefault();

                    // Use EasyZoom's `swap` method
                    productImage.swap($this.data('standard'), $this.attr('href'));
                });
    //              jQuery('<div class="quantity-nav"><div class="quantity-button quantity-up"><img src="{% static 'shop/img/plus.png' %}" class="img-fluid"></div><div class="quantity-button quantity-down"><img src="{% static 'shop/img/minus.png' %}" class="img-fluid"></div></div>').insertAfter('.quantity input');
                jQuery('.quantity').each(function () {
                    var spinner = jQuery(this),
                            input = spinner.find('input[type="number"]'),
                            btnUp = spinner.find('.quantity-up'),
                            btnDown = spinner.find('.quantity-down'),
                            min = input.attr('min'),
                            max = input.attr('max');

                    btnUp.click(function () {
                        btnDown.removeAttr("disabled");
                        var oldValue = parseFloat(input.val());
                        if (oldValue > max) {
                            var newVal = oldValue;
                        } else {
                            var newVal = oldValue + 1;
                            if (oldValue == max){
                                btnUp.attr("disabled", "disabled");
                            }
                        }
                        if (newVal == 1){
                            $(".productSingleAddCart").html('Added');
                            $(".productSingleAddCart").attr('disabled', 'disabled');
                        }
                        spinner.find("input").val(newVal);
                        spinner.find("input").trigger("change");

                        var quantityCount = $('.quantity-count').val();
                        var updatedPriceold = $('.actual-price').text();
                        var updatedPricenew = $('.offer-price').text();

                        if (parseFloat(quantityCount) == 1 || parseFloat(quantityCount) > parseFloat(max)) {
                            // $(this).attr('disabled', true);
                            var newPrice = updatedPricenew;
                            var oldPrice = updatedPriceold;

                        } else{
                            var newPrice = (updatedPricenew/ (parseFloat(quantityCount)-1)) * parseFloat(quantityCount);
                            var oldPrice = (updatedPriceold/ (parseFloat(quantityCount)-1)) * parseFloat(quantityCount);
                        }
                        //
                        // if (quantityCount == 2 && !$(".offer-price").data("price")) {
                        //     $('.offer-price').data("price", updatedPricenew);
                        // } else {
                        //     updatedPricenew = $('.offer-price').data("price");
                        // }
                        // if (quantityCount == 2 && !$(".actual-price").data("price")) {
                        //     $('.actual-price').data("price", updatedPriceold);
                        // } else {
                        //     updatedPriceold = $('.actual-price').data("price");
                        // }



                        $('.offer-price').html(newPrice);
                        $('.actual-price').html(oldPrice);

                    });

                    btnDown.click(function () {
                        btnUp.removeAttr("disabled");
                        var oldValue = parseFloat(input.val());
                        if (oldValue>max){
                            var oldValue = oldValue - 1;
                        }
                        if (oldValue == min){
                                btnDown.attr("disabled", "disabled");
                            }
                        if (oldValue <= min) {
                            var newVal = oldValue;
                        } else {
                            var newVal = oldValue - 1;
                        }
                        if (newVal == 0){
                            $(".productSingleAddCart").html('Add to cart');
                            $(".productSingleAddCart").prop('disabled', false);
                        }
                        spinner.find("input").val(newVal);
                        spinner.find("input").trigger("change");
                        var quantityCount = $('.quantity-count').val();
                        var updatedPriceold = $('.actual-price').text();
                        var updatedPricenew = $('.offer-price').text();

                        if (parseFloat(quantityCount) == 0 || parseFloat(quantityCount) <= min) {
                            var newPrice = updatedPricenew;
                            var oldPrice = updatedPriceold;
                        } else{
                        var newPrice = (updatedPricenew/ (parseFloat(quantityCount)+1)) * parseFloat(quantityCount);
                        var oldPrice = (updatedPriceold/ (parseFloat(quantityCount)+1)) * parseFloat(quantityCount);
                        }
                        // if (quantityCount == 2 && !$(".offer-price").data("price")) {
                        //     $('.offer-price').data("price", updatedPricenew);
                        // } else {
                        //     updatedPricenew = $('.offer-price').data("price");
                        // }
                        // if (quantityCount == 2 && !$(".actual-price").data("price")) {
                        //     $('.actual-price').data("price", updatedPriceold);
                        // } else {
                        //     updatedPriceold = $('.actual-price').data("price");
                        // }




                        $('.offer-price').html(newPrice);  //parseFloat().toFixed(2) ->to convert to float of 2 decimals
                        $('.actual-price').html(oldPrice);
                    });
                });
                $('body').on('click', '.productSingleAddCart', function () {
                    $(this).html('Added');
                    var productName = $(this).closest('.product-singledetails').find('.product-singlename').text();
                    $('.cart-count').css('transform', 'scale(1)');
                    $(this).attr('disabled', 'disabled');
                    messageDisplay(productName + " added to cart", 1500, "success");
                    $(".quantity input.quantity-count").val(1);
                    $(".quantity input.quantity-count").trigger("change");
                });
                $('body').on('click', '#clearSubcategoryfilters', function () {
                    let subcatFilter = $('#clearSubcategoryfilters').closest('.filter-box').find("input:checked");
                    if (subcatFilter.length > 0) {
                        $(subcatFilter).prop('checked', false);
                        messageDisplay("Category filters are cleared", 1500, "success");
                    } else {
                        messageDisplay("Category filters are applied", 1500, "error");
                    }
                });

	$(window).on('scroll', function () {
		if ($(this).scrollTop() > 600) {
			let navbarHeight = Math.ceil($('.navbar-fluid').height());
			$('.navbar-fluid').addClass('nav-fixed');
			$('.main-content').css('padding-top', navbarHeight);
			$('#productFilter').addClass('sticky');
		} else {
			$('.navbar-fluid').removeClass('nav-fixed');
			$('.main-content').css('padding-top', '');
			$('#productFilter').removeClass('sticky');
		}
	
		if ($(this).scrollTop() > 300) {
			$('.navbar-fluid').addClass('translate-top');
		} else {
			$('.navbar-fluid').removeClass('translate-top');
		}
	
		if ($(this).scrollTop() > 600) {
			$('.scroll-top').fadeIn(600);
		} else {
			$('.scroll-top').fadeOut(600);
		}
	});
	
	$('body').on('click', '.scroll-top', function () {
		$("html,body").animate({scrollTop: 0}, 500);
		return false;
	}).on('click', '.navbar-toggler', function () {
		$('.c-hamburger').toggleClass('is-active');
	}).on('click', '.btn-addcart, .btn-addtocart, .product-addcart', function () {
        $(this).html('Added');
        $(this).attr('disabled', 'disabled');
        // $('.cart-count').html(function (i, val) {
        // return val * 1 + 1;
        // });
        // var cartCount = $('.cart-count').text();
        // if (cartCount != 0) {
        //     $('.cart-count').css('transform', 'scale(1)');
        // }
	}).on('click', '#signupModalbtn', function () {
		$('#loginModal').modal('hide');
	}).on('click', '#forgotPasswordModalbtn', function () {
		$('#loginModal').modal('hide');
		$('#forgotModal').modal('show');
	}).on('click', '#login-btn', function () {
		$('#signupModal').modal('hide');
	});

	/* cart count */
var cartCount = $('.cart-count').text();
if (cartCount != 0) {
    $('.cart-count').css('transform', 'scale(1)');
}
// if (localStorage.getItem('cart') == null){
//     var cart = {};
// }
// else{
// cart = JSON.parse(localStorage.getItem('cart'));
// for(var item in cart){
// document.getElementById('div'+item).innerHTML = 'added';
// }
// document.getElementById('cart-count').innerHTML = Object.keys(cart).length;
// }

// //$("#addCart").click(function(){
// //    });

//     $("#selectedField").on('click', '#remCF', function(){
//         $(this).parent().parent().remove();
//     });

////////


$('#login-btn').on('click', function(e) {
    e.preventDefault();
    var that = $(this);
    console.log("main");
    $.ajax({
        type: "POST",
        url: "/login/",
        data: {
            csrfmiddlewaretoken: csrftoken
        },
        success: function(response) {

            $(".modal-login").html(response);
            $("#signupModal").modal('hide');
            $("#loginModal").modal('show');
        },
        error: function() {
            alert('Error');
        }
    });
    return false;
});


$(document).on('submit','#login_form', function(e){

    e.preventDefault();
    var login_form = $('#login_form');
    var action = login_form.attr('action');
    var method = login_form.attr('method');
    var data_ = login_form.serialize();

    $.ajax({
        type: method,
        url: action,
        data: data_,
        success: function(data, status) {

            if ($(data).find('.is-invalid').length > 0 ||$(data).find('.alert-danger').length > 0) {

                $('.modal-login').html(data);
                // console.log(data)

            }else{


                $('#loginModal').modal('hide')
                location.reload(); //Reload the current document page on success

            }
        }
    });

    return false;
});

var restoreModalOnClose = function(){
    var error_fields = $('.has-error')
    var danger_pop = $('.alert-danger')

    danger_pop.parent().remove()

    $.each(error_fields, function(index, value){
        $(value).removeClass('has-error');
        // console.log(value)
    })

};


$('#loginModal').on('hidden.bs.modal', function (e){

    restoreModalOnClose()
});

$('#signupModalbtn').on('click', function(e) {
    e.preventDefault();
    var that = $(this);
    $.ajax({
        type: "POST",
        url: "/register/",
        data: {
            csrfmiddlewaretoken: csrftoken
        },
        success: function(response) {

            // $('#form-replace').html(response);
            $(".modal-signup").html(response);
            $('#loginModal').modal('hide');
            $("#signupModal").modal('show');


        },
        error: function() {
            alert('Error');
        }
    });
    return false;
});

$(document).on('submit','#signup_form', function(e){

    e.preventDefault();
    var signup_form = $('#signup_form');
    var action = signup_form.attr('action');
    var method = signup_form.attr('method');
    var data_ = signup_form.serialize();

    $.ajax({
        type: method,
        url: action,
        data: data_,

        success: function(data, status) {



            if ($(data).find('.is-invalid').length > 0 || $(data).find('.alert-danger').length > 0) {

                $('.modal-signup').html(data);
                // console.log(data)

            }else{
                console.log("here in success3");


                $('#signupModal').modal('hide')

                location.reload(); //Reload the current document page on success

            }
        }


    });

    return false;
});

$('#signupModal').on('hidden.bs.modal', function (e){

    restoreModalOnClose()
});

// $(function () {
//       // Log in button
//       $("#login-btn").modalForm({
//           formURL: "/login/",
//           modalID: "#loginModal",
//           csrfmiddlewaretoken :csrftoken,
//       });
//     });


        // Countries
        var country_arr = new Array("INDIA");

        $.each(country_arr, function (i, item) {
            $('#country').append($('<option>', {
                value: i,
                text : item,
            }, '</option>' ));
        });

        // States
        var s_a = new Array();


        s_a[0]="Andaman and Nicobar Islands|Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chandigarh|Chhattisgarh|Dadra and Nagar Haveli|Daman and Diu|Goa|Gujarat|Haryana|Himachal Pradesh|Jharkhand|Karnataka|Kashmir|Kerala|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|NCT|Nagaland|Odisha|Pondicherry|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal";


        // Cities
        var c_a = new Array();

        c_a['Andaman and Nicobar Islands']= "Port Blair";
        c_a['Andhra Pradesh']="Addanki|Adoni|Akividu|Akkarampalle|Amalapuram|Amudalavalasa|Anakapalle|Anantapur|Atmakur|Attili|Avanigadda|Badvel|Banganapalle|Bapatla|Betamcherla|Bhattiprolu|Bhimavaram|Bhimunipatnam|Bobbili|Challapalle|Chemmumiahpet|Chicacole|Chilakalurupet|Chinnachowk|Chipurupalle|Chirala|Chodavaram|Cuddapah|Cumbum|Dharmavaram|Dhone|Elamanchili|Ellore|Emmiganur|Erraguntla|Gajuwaka|Gannavaram|Giddalur|Gudivada|Gudur|Guntakal Junction|Guntur|Hindupur|Ichchapuram|Jaggayyapeta|Jammalamadugu|Kadiri|Kaikalur|Kakinada|Kalyandurg|Kandukur|Kanigiri|Kanuru|Kavali|Kondapalle|Kosigi|Kovur|Kovvur|Kuppam|Macherla|Machilipatnam|Madanapalle|Mandapeta|Mangalagiri|Markapur|Nagari|Nandigama|Nandikotkur|Nandyal|Narasannapeta|Narasapur|Narasaraopet|Narsipatnam|Nayudupeta|Nellore|Nidadavole|Nuzvid|Ongole|Pakala|Palakollu|Palasa|Palkonda|Palmaner|Parlakimidi|Parvatipuram|Pedana|Peddapuram|Penugonda|Penukonda|Phirangipuram|Pithapuram|Polavaram|Ponnur|Ponnuru|Proddatur|Pulivendla|Punganuru|Puttur|Rajahmundry|Rajampet|Ramachandrapuram|Ramanayyapeta|Ramapuram|Rampachodavaram|Rayachoti|Rayadrug|Razam|Renigunta|Repalle|Salur|Samalkot|Sattenapalle|Singarayakonda|Sompeta|Srisailain|Suluru|Tadepalle|Tadepallegudem|Tadpatri|Tanuku|Tekkali|Tirumala|Tirupati|Tuni|Uravakonda|Vadlapudi|Venkatagiri|Vepagunta|Vetapalem|Vijayawada|Vinukonda|Visakhapatnam|Vizianagaram|Vuyyuru|Yanam|Yanamalakuduru";
        c_a['Arunachal Pradesh']="Along|Itanagar|Margherita|Naharlagun|Pasighat";
        c_a['Assam']="Abhayapuri|Barpeta|Barpeta Road|Bilasipara|Bokajan|Bongaigaon|Chapar|Dhekiajuli|Dhing|Dhuburi|Dibrugarh|Digboi|Diphu|Duliagaon|Dum Duma|Gauripur|Goalpara|Golaghat|Guwahati|Haflong|Hailakandi|Hajo|Hojai|Howli|Jorhat|Karimganj|Kharupatia|Kokrajhar|Lumding Railway Colony|Makum|Mangaldai|Mariani|Marigaon|Nahorkatiya|Namrup|North Guwahati|North Lakhimpur|Rangapara|Rangia|Sibsagar|Silapathar|Silchar|Sonari|Tezpur|Tinsukia|Udalguri";
        c_a['Bihar']="Amarpur|Araria|Arrah|Aurangabad|Bagaha|Bahadurganj|Bairagnia|Bakhtiyarpur|Bangaon|Banka|Banmankhi|Bar Bigha|Barauli|Barh|Barhiya|Baruni|Begusarai|Belsand|Bettiah|Bhabhua|Bhagalpur|Bhawanipur|Bihar|Bihariganj|Bikramganj|Birpur|Buddh Gaya|Buxar|Chakia|Chapra|Chhatapur|Colgong|Dalsingh Sarai|Darbhanga|Daudnagar|Dehri|Dhaka|Dighwara|Dinapore|Dumra|Dumraon|Fatwa|Forbesganj|Gaya|Gopalganj|Hajipur|Hilsa|Hisua|Islampur|Jagdispur|Jahanabad|Jamalpur|Jamui|Jaynagar|Jha Jha|Jhanjharpur|Jogbani|Kasba|Katihar|Khagaria|Khagaul|Kharagpur|Kishanganj|Koath|Koelwar|Lalganj|Luckeesarai|Madhipura|Madhubani|Maharajgani|Mairwa|Maner|Manihari|Marhaura|Masaurhi Buzurg|Mokameh|Monghyr|Mothihari|Murliganj|Muzaffarpur|Nabinagar|Nasriganj|Naugachhia|Nawada|Nirmali|Patna|Piro|Pupri|Purnia|Rafiganj|Rajgir|Ramnagar|Raxaul|Revelganj|Rusera|Sagauli|Saharsa|Samastipur|Shahbazpur|Shahpur|Sheikhpura|Sheohar|Sherghati|Silao|Sitamarhi|Siwan|Supaul|Teghra|Tekari|Thakurganj|Waris Aliganj";
        c_a['Chandigarh']="Chandigarh";
        c_a['Chhattisgarh']="Akaltara|Ambikapur|Arang|Balod|Baloda Bazar|Bemetara|Bhanpuri|Bhatapara|Bhilai|Bilaspur|Champa|Dhamtari|Dongargarh|Durg|Gumla|Jagdalpur|Janjgir|Jashpurnagar|Junagarh|Kanker|Katghora|Kawardha|Khairagarh|Kharsia|Kirandul|Kondagaon|Korba|Kota|Kotaparh|Kumhari|Mahasamund|Mungeli|Pasan|Pathalgaon|Raigarh|Raipur|Raj-Nandgaon|Ratanpur|Sakti|Saraipali|Takhatpur|Umarkot";
        c_a['Dadra and Nagar Haveli']="Amli|Silvassa";
        c_a['Daman and Diu']="Daman|Diu";
        c_a['Goa']="Calangute|Cuncolim|Curchorem|Dicholi|Madgaon|Mapuca|Marmagao|Panaji|Ponda|Sancoale|Taleigao|Vasco Da Gama";
        c_a['Gujarat']="Ahmedabad|Amod|Amreli|Amroli|Anand|Anjar|Ankleshwar|Babra|Bagasra|Bantva|Bardoli|Bedi|Bhachau|Bhanvad|Bharuch|Bhavnagar|Bhayavadar|Bhuj|Bilimora|Borsad|Botad|Chaklasi|Chalala|Chanasma|Chhala|Chhota Udepur|Chotila|Dabhoi|Dahegam|Dakor|Damnagar|Devgadh Bariya|Dhandhuka|Dhanera|Dharampur|Dhari|Dholka|Dhoraji|Dhrangadhra|Dhrol|Disa|Dohad|Dwarka|Gadhada|Gandevi|Gandhidham|Gariadhar|Ghandinagar|Godhra|Gondal|Halol|Halvad|Harij|Himatnagar|Jalalpur|Jambusar|Jamnagar|Jasdan|Jetpur|Jodhpur|Jodiya Bandar|Junagadh|Kadi|Kadod|Kalavad|Kalol|Kandla|Kapadvanj|Karamsad|Kathor|Keshod|Khambhaliya|Khambhat|Khed Brahma|Kheda|Kheralu|Kodinar|Kosamba|Kundla|Kutiyana|Lalpur|Lathi|Limbdi|Lunavada|Mahemdavad|Mahudha|Manavadar|Mandvi|Mangrol|Mansa|Mendarda|Modasa|Morbi|Morwa|Mundra|Nadiad|Okha|Padra|Palanpur|Palitana|Pardi|Patan|Petlad|Porbandar|Radhanpur|Rajkot|Rajpipla|Rajula|Ranavav|Rapar|Salaya|Sanand|Sarkhej|Sayla|Siddhapur|Sihor|Sikka|Sojitra|Songadh|Surat|Surendranagar|Talaja|Than|Tharad|Thasra|Umreth|Un|Una|Unjha|Upleta|Vadnagar|Vadodara|Valabhipur|Vallabh Vidyanagar|Valsad|Vapi|Vasa|Vejalpur|Veraval|Vijapur|Visavadar|Visnagar|Vyara|Wankaner";
        c_a['Haryana']="Ambala|Asandh|Bahadurgarh|Bara Uchana|Barwala|Beri Khas|Bhiwani|Charkhi Dadri|Dabwali|Dharuhera|Ellenabad|Faridabad|Fatehabad|Firozpur Jhirka|Gharaunda|Gohana|Gorakhpur|Gurgaon|Hansi|Hisar|Hodal|Indri|Jagadhri|Jhajjar|Jind|Kaithal|Kalanaur|Kalanwali|Karnal|Kharkhauda|Ladwa|Maham|Mahendragarh|Narayangarh|Narnaul|Narnaund|Narwana|Nilokheri|Palwal|Panipat|Pataudi|Pehowa|Pinjaur|Punahana|Pundri|Rania|Ratia|Rewari|Rohtak|Safidon|Samalkha|Shahabad|Sirsa|Sohna|Sonipat|Taoru|Thanesar|Tohana|Yamunanagar";
        c_a['Himachal Pradesh']="Baddi|Chamba|Dharmsala|Hamirpur|Kalka|Kulu|Mandi|Nahan|Paonta Sahib|Shimla|Solan|Sundarnagar|Una";
        c_a['Jharkhand']="Barka Kana|Barki Saria|Bokaro|Bundu|Chaibasa|Chakradharpur|Chas|Chatra|Daltonganj|Dhanbad|Dugda|Dumka|Garhwa|Ghatsila|Giridih|Gobindpur|Godda|Gomoh|Gumia|Hazaribag|Husainabad|Jamadoba|Jamshedpur|Jamtara|Jasidih|Jharia|Jugsalai|Jumri Tilaiya|Kanke|Katras|Khunti|Kodarma|Kuju|Latehar|Lohardaga|Madhupur|Mushabani|Noamundi|Pakaur|Pathardih|Ramgarh|Ranchi|Sahibganj|Sijua|Simdega";
        c_a['Karnataka']="Afzalpur|Aland|Alnavar|Anekal|Annigeri|Arkalgud|Arsikere|Athni|Aurad|Badami|Bagalkot|Bagepalli|Bail-Hongal|Bangarapet|Bannur|Bantval|Basavakalyan|Basavana Bagevadi|Belgaum|Bellary|Belur|Bengaluru|Bhadravati|Bhalki|Bhatkal|Bidar|Bijapur|Bilgi|Birur|Byadgi|Byndoor|Challakere|Chamrajnagar|Channagiri|Channapatna|Channarayapatna|Chik Ballapur|Chikmagalur|Chiknayakanhalli|Chikodi|Chincholi|Chintamani|Chitapur|Chitradurga|Coondapoor|Dandeli|Devanhalli|Dod Ballapur|French Rocks|Gadag|Gajendragarh|Gangawati|Gangolli|Gokak|Gokarna|Goribidnur|Gubbi|Gulbarga|Guledagudda|Gundlupet|Gurmatkal|Hadagalli|Haliyal|Hangal|Harihar|Harpanahalli|Hassan|Haveri|Hirekerur|Hiriyur|Holalkere|Hole Narsipur|Homnabad|Honavar|Honnali|Hosdurga|Hoskote|Hospet|Hubli|Hukeri|Hungund|Hunsur|Ilkal|Indi|Jagalur|Jamkhandi|Jevargi|Kadur|Kalghatgi|Kampli|Kanakapura|Karkala|Karwar|Kerur|Khanapur|Kolar|Kollegal|Konnur|Koppal|Kotturu|Krishnarajpet|Kudachi|Kudligi|Kumta|Kundgol|Kunigal|Kushtagi|Lakshmeshwar|Lingsugur|Maddagiri|Maddur|Madikeri|Magadi|Mahalingpur|Malavalli|Malpe|Malur|Mandya|Mangalore|Manvi|Mudbidri|Muddebihal|Mudgal|Mudhol|Mulbagal|Mulgund|Mulki|Mundargi|Mundgod|Murudeshwara|Mysore|Nagamangala|Nanjangud|Naregal|Nargund|Navalgund|Nelamangala|Pavugada|Piriyapatna|Puttur|Rabkavi|Raichur|Ramanagaram|Ranibennur|Raybag|Robertsonpet|Ron|Sadalgi|Sagar|Sakleshpur|Sandur|Sankeshwar|Saundatti|Savanur|Seram|Shahabad|Shahpur|Shiggaon|Shikarpur|Shimoga|Shirhatti|Shorapur|Shrirangapattana|Sidlaghatta|Sindgi|Sindhnur|Sira|Sirsi|Siruguppa|Someshwar|Srinivaspur|Sulya|Talikota|Tarikere|Tekkalakote|Terdal|Tiptur|Tirthahalli|Tumkur|Udipi|Ullal|Vijayapura|Virarajendrapet|Wadi|Yadgir|Yelahanka|Yellapur";
        c_a['Kashmir']="Anantnag|Bandipura|Baramula|Bijbiara|Doda|Gandarbal|Jammu|Kathua|Kishtwar|Kulgam|Leh|Padam|Pulwama|Punch|Rajaori|Samba|Sopur|Soyibug|Srinagar|Udhampur";
        c_a['Kerala']="Adur|Alleppey|Aluva|Angamali|Aroor|Arukutti|Attingal|Badagara|Beypore|Cannanore|Changanacheri|Chavakkad|Chengannur|Cherpulassery|Cherthala|Chittur|Cochin|Dharmadam|Elur|Erattupetta|Ferokh|Guruvayur|Iringal|Irinjalakuda|Kadakkavoor|Kalamassery|Kalavoor|Kalpetta|Kannangad|Kasaragod|Kattanam|Kayankulam|Kizhake Chalakudi|Kodungallur|Kollam|Kotamangalam|Kottayam|Kozhikode|Kumbalam|Kunnamangalam|Kunnamkulam|Kutiatodu|Kuttampuzha|Mahe|Malappuram|Manjeri|Mannarakkat|Mattanur|Mavelikara|Mavoor|Muluppilagadu|Munnar|Muvattupula|Muvattupuzha|Nadapuram|Naduvannur|Nedumangad|Neyyattinkara|Nileshwar|Ottappalam|Palakkad|Panmana|Pappinissheri|Paravur|Pariyapuram|Pathanamthitta|Payyannur|Perumbavoor|Perumpavur|Piravam|Ponnani|Punalur|Shertallai|Shoranur|Talipparamba|Tellicherry|Thiruvananthapuram|Tirur|Tiruvalla|Trichur|Vaikam|Varkala|Vayalar|Vettur";
        c_a['Madhya Pradesh']="Agar|Alot|Amarpatan|Ambah|Amla|Anjad|Anuppur|Aron|Ashoknagar|Ashta|Babai|Badnawar|Baihar|Balaghat|Bamor Kalan|Banda|Bargi|Barwani|Basoda|Begamganj|Beohari|Berasia|Betul|Bhainsdehi|Bhander|Bhanpura|Bhawaniganj|Bhikangaon|Bhind|Bhitarwar|Bhopal|Biaora|Bijawar|Burhanpur|Burhar|Chanderi|Chhatarpur|Chhindwara|Daboh|Dabra|Damoh|Datia|Deori Khas|Depalpur|Dewas|Dhamnod|Dhar|Dindori|Etawa|Gadarwara|Garhakota|Gohadi|Guna|Gwalior|Harda Khas|Harpalpur|Harsud|Hatta|Hindoria|Hoshangabad|Indore|Itarsi|Jabalpur|Jamai|Jaora|Jatara|Jawad|Jhabua|Jora|Kailaras|Kaimori|Kannod|Kareli|Karera|Kasrawad|Katangi|Khachrod|Khajuraho|Khamaria|Khandwa|Khargone|Khategaon|Khilchipur|Khirkiyan|Khurai|Kolaras|Korwai|Kotma|Kukshi|Kumbhraj|Lahar|Lakhnadon|Leteri|Maheshwar|Mahgawan|Maihar|Maksi|Manasa|Manawar|Mandideep|Mandla|Mandsaur|Mandu|Mau|Mauganj|Mihona|Morar|Morena|Multai|Mungaoli|Murwara|Nagda|Nagod|Nainpur|Naraini|Narsimhapur|Narsinghgarh|Narwar|Nasrullahganj|Nepanagar|Palera|Pali|Panagar|Pandhurna|Panna|Parasia|Patharia|Pithampur|Porsa|Punasa|Raghogarh|Rahatgarh|Raisen|Rajgarh|Rajpur|Rampura|Ratlam|Rehli|Rewa|Sabalgarh|Sanawad|Sarangpur|Satna|Saugor|Sausar|Sehore|Sendhwa|Seondha|Seoni|Seoni Malwa|Shahdol|Shahpur|Shajapur|Shamgarh|Sheopur|Shivpuri|Shujalpur|Sidhi|Sihora|Singrauli|Sironj|Sohagpur|Tarana|Teonthar|Tikamgarh|Udaipura|Ujjain|Umaria|Unhel|Vidisha|Waraseoni";
        c_a['Maharashtra']="Achalpur|Ahmadnagar|Ahmadpur|Airoli|Ajra|Akalkot|Akola|Akot|Alandi|Alibag|Amalner|Amarnath|Ambad|Ambajogai|Amravati|Anjangaon|Anshing|Arangaon|Arvi|Ashta|Aurangabad|Ausa|Badlapur|Balapur|Ballalpur|Baramati|Barsi|Basmat|Bhandara|Bhayandar|Bhiwandi|Bhor|Bhudgaon|Bhum|Bhusaval|Boisar|Borivli|Buldana|Chakan|Chalisgaon|Chanda|Chandor|Chandur|Chandur Bazar|Chicholi|Chikhli|Chiplun|Chopda|Dahanu|Darwha|Daryapur|Dattapur|Daund|Deolali|Deoli|Deulgaon Raja|Dharangaon|Dharmabad|Dharur|Dhulia|Diglur|Digras|Dombivli|Dondaicha|Durgapur|Erandol|Faizpur|Gadhinglaj|Gangakher|Gangapur|Gevrai|Ghatanji|Ghoti Budrukh|Ghugus|Gondia|Hadgaon|Hinganghat|Hingoli|Ichalkaranji|Igatpuri|Indapur|Jaisingpur|Jalgaon|Jalgaon Jamod|Jalna|Jintur|Junnar|Kagal|Kalamb|Kalamnuri|Kalmeshwar|Kalyan|Kamthi|Kankauli|Kannad|Karad|Karanja|Karjat|Karmala|Katol|Khadki|Khamgaon|Khapa|Kharakvasla|Khetia|Khopoli|Khuldabad|Kinwat|Kodoli|Kolhapur|Kopargaon|Koregaon|Koynanagar|Kurandvad|Kurduvadi|Latur|Lonar|Lonavla|Mahad|Majalgaon|Malegaon|Malkapur|Malvan|Mangrul Pir|Manmad|Manwat|Mehekar|Mhasvad|Moram|Morsi|Mudkhed|Mukher|Mul|Mumbai|Murbad|Murtajapur|Nagpur|Naldurg|Nanded|Nandgaon|Nandura Buzurg|Nandurbar|Nashik|Navi Mumbai|Neral|Nilanga|Nipani|Osmanabad|Ozar|Pachora|Paithan|Palghar|Pandharpur|Panvel|Parbhani|Parli Vaijnath|Parola|Partur|Pathardi|Pathri|Patur|Pawni|Pen|Phaltan|Pimpri|Pipri|Powai|Pulgaon|Pune|Purna|Pusad|Rahimatpur|Rahuri|Rajgurunagar|Rajura|Ramtek|Ratnagiri|Raver|Risod|Roha|Sangamner|Sangli|Sangola|Saoner|Sasvad|Satana|Satara|Savantvadi|Savda|Selu|Shahada|Shegaon|Shiraguppi|Shirdi|Shirpur|Shivaji Nagar|Shrigonda|Sillod|Sinnar|Sirur|Solapur|Soygaon|Srivardhan|Talegaon Dabhade|Taloda|Tasgaon|Telhara|Thane|Tuljapur|Tumsar|Udgir|Ulhasnagar|Umarga|Umarkhed|Umred|Uran|Vada|Vaijapur|Varangaon|Vasind|Virar|Vite|Wai|Wani|Wardha|Warora|Warud|Washim|Yaval|Yavatmal|Yeola";
        c_a['Manipur']="Churachandpur|Imphal|Kakching|Mayang Imphal|Moirang|Phek|Thoubal";
        c_a['Meghalaya']="Mankachar|Nongstoin|Shillong|Tura";
        c_a['Mizoram']="Aizawl|Kolasib|Lunglei|Saiha|Serchhip";
        c_a['NCT']="Alipur|Bawana|Delhi|Karol Bagh|Nangloi Jat|New Delhi";
        c_a['Nagaland']="Dimapur|Kohima|Mokokchung|Mon|Tuensang|Wokha|Zunheboto";
        c_a['Odisha']="Angul|Asika|Athagarh|Bada Barabil|Balangir|Balasore|Balugaon|Banapur|Banki|Barbil|Bargarh|Barpali|Basudebpur|Bauda|Bhadrakh|Bhanjanagar|Bhawanipatna|Bhuban|Bhubaneshwar|Binka|Birmitrapur|Brahmapur|Brajarajnagar|Burla|Chatrapur|Cuttack|Deogarh|Dhenkanal|Gunupur|Hinjilikatu|Hirakud|Jagatsinghapur|Jajpur|Jaleshwar|Jatani|Jeypore|Jharsuguda|Kamakhyanagar|Kantabanji|Kendraparha|Kesinga|Khurda|Konarka|Koraput|Kuchaiburi|Malakanagiri|Nayagarh|Nilgiri|Nimaparha|Nowrangapur|Padampur|Paradip Garh|Patamundai|Patnagarh|Phulabani|Pipili|Polasara|Puri|Remuna|Sambalpur|Sonepur|Sorada|Soro|Sundargarh|Talcher|TitlagarhKaraikal|Puducherry";
        c_a['Pondicherry']="Karaikal|Puducherry";
        c_a['Punjab']="Abohar|Adampur|Ajnala|Amritsar|Anandpur|Bagha Purana|Balachor|Banga|Banur|Barnala|Basi|Batala|Bhadaur|Bhatinda|Bhawanigarh|Bhikhi|Bhogpur|Budhlada|Dasuya|Dhanaula|Dhariwal|Dhuri|Dinanagar|Doraha|Faridkot|Fatehgarh Churian|Fazilka|Ferozepore|Garhshankar|Giddarbaha|Guru Har Sahai|Jagraon|Jaito|Jalalabad|Jalandhar|Jandiala|Kapurthala|Kartarpur|Khanna|Kharar|Kotkapura|Laungowal|Ludhiana|Machhiwara|Malaut|Maler Kotla|Mansa|Maur|Moga|Mohali|Morinda|Mukerian|Muktsar|Nabha|Nakodar|Nangal Township|Nawashahr|Pathankot|Patiala|Patti|Phagwara|Phillaur|Qadian|Raikot|Rajpura|Rampura|Ropar|Samrala|Sanaur|Sangrur|Sardulgarh|Sirhind|Sultanpur|Sunam|Talwandi Bhai|Talwara|Tarn Taran|Zira";
        c_a['Rajasthan']="Abu|Abu Road|Ajmer|Aklera|Alwar|Amet|Anta|Anupgarh|Asind|Bagar|Bali|Balotra|Bandikui|Banswara|Baran|Bari|Bari Sadri|Barmer|Basi|Basni|Baswa|Bayana|Beawar|Begun|Behror|Bhadasar|Bhadra|Bharatpur|Bhasawar|Bhilwara|Bhindar|Bhinmal|Bhiwadi|Bikaner|Bilara|Bissau|Bundi|Chaksu|Chhabra|Chhapar|Chhoti Sadri|Chidawa|Chittaurgarh|Churu|Dausa|Deoli|Deshnoke|Devgarh|Dhaulpur|Didwana|Dig|Dungarpur|Fatehpur|Ganganagar|Gangapur|Gulabpura|Hanumangarh|Hindaun|Jahazpur|Jaipur|Jaisalmer|Jaitaran|Jalor|Jhalawar|Jhalrapatan|Jhunjhunun|Jodhpur|Kaman|Kapren|Karanpur|Karauli|Kekri|Keshorai Patan|Khandela|Khetri|Kishangarh|Kota|Kotputli|Kuchaman|Kuchera|Kumher|Lachhmangarh Sikar|Ladnun|Lakheri|Lalsot|Losal|Mahwah|Makrana|Malpura|Mandal|Mandalgarh|Mangrol|Manoharpur|Merta|Mundwa|Nadbai|Nagar|Nagaur|Nainwa|Napasar|Naraina|Nasirabad|Nathdwara|Nawa|Nawalgarh|Neem ka Thana|Nimaj|Nimbahera|Niwai|Nohar|Nokha|Padampur|Pali|Parvatsar|Phalodi|Phulera|Pilani|Pilibangan|Pindwara|Pipar|Pokaran|Pratapgarh|Pushkar|Raipur|Raisinghnagar|Rajakhera|Rajaldesar|Rajgarh|Rajsamand|Ramganj Mandi|Ramgarh|Ratangarh|Rawatbhata|Rawatsar|Ringas|Sadri|Salumbar|Sambhar|Samdari|Sanchor|Sangaria|Sangod|Sardarshahr|Sarwar|Sawai Madhopur|Shahpura|Sheoganj|Sikar|Sirohi|Siwana|Sojat|Sri Dungargarh|Sri Madhopur|Sujangarh|Suket|Sunel|Surajgarh|Suratgarh|Takhatgarh|Taranagar|Tijara|Todabhim|Todaraisingh|Tonk|Udaipur|Wer";
        c_a['Sikkim']="Gangtok";
        c_a['Tamil Nadu']="Adirampattinam|Alandur|Alangayam|Alangulam|Ambasamudram|Ambattur|Ambur|Anaimalai|Andippatti|Annur|Anthiyur|Arakkonam|Arani|Arantangi|Arcot|Ariyalur|Arumuganeri|Aruppukkottai|Attur|Avadi|Avinashi|Ayakudi|Bhavani|Bhuvanagiri|Bodinayakkanur|Chengalpattu|Chengam|Chennai|Chennimalai|Chetput|Chettipalaiyam|Cheyyar|Chidambaram|Chinna Salem|Chinnamanur|Coimbatore|Colachel|Cuddalore|Cumbum|Denkanikota|Devakottai|Dharapuram|Dharmapuri|Dindigul|Erode|Gingee|Gobichettipalayam|Gudalur|Gudiyatham|Guduvancheri|Gummidipundi|Harur|Hosur|Idappadi|Injambakkam|Irugur|Jayamkondacholapuram|Jolarpettai|Kadayanallur|Kalakkadu|Kallakkurichchi|Kallidaikurichchi|Kalugumalai|Kanchipuram|Kangayam|Kanniyakumari|Karaikkudi|Karamadai|Karur|Katpadi|Kattivakkam|Kayalpattinam|Keelakarai|Kodaikanal|Koothanallur|Kotagiri|Kovilpatti|Krishnagiri|Kulittalai|Kumbakonam|Kurinjippadi|Kuzhithurai|Lalgudi|Madambakkam|Madipakkam|Madukkarai|Madukkur|Madurai|Madurantakam|Mallasamudram|Manali|Manamadurai|Manapparai|Mandapam|Mannargudi|Marakkanam|Mayiladuthurai|Melur|Mettupalayam|Mettur|Minjur|Musiri|Muttupet|Nagappattinam|Nagercoil|Namagiripettai|Namakkal|Nambiyur|Naravarikuppam|Nattam|Neelankarai|Nellikkuppam|Nilakottai|Ooty|Padmanabhapuram|Palakkodu|Palani|Palladam|Pallappatti|Pallavaram|Pallikondai|Pallippatti|Panruti|Papanasam|Paramagudi|Pattukkottai|Pennadam|Pennagaram|Perambalur|Peranampattu|Peravurani|Periyakulam|Periyanayakkanpalaiyam|Perundurai|Perungudi|Pollachi|Polur|Ponneri|Poonamalle|Porur|Pudukkottai|Puliyangudi|Punjai Puliyampatti|Rajapalaiyam|Ramanathapuram|Rameswaram|Rasipuram|Saint Thomas Mount|Salem|Sathyamangalam|Sattur|Sholinghur|Singanallur|Sirkazhi|Sirumugai|Sivaganga|Sivagiri|Sivakasi|Sriperumbudur|Srivaikuntam|Srivilliputhur|Sulur|Surandai|Taramangalam|Teni|Thanjavur|Tharangambadi|Thenkasi|Thiruthani|Thiruvarur|Tindivanam|Tinnanur|Tiruchchendur|Tiruchengode|Tiruchirappalli|Tirukkoyilur|Tirunelveli|Tirupparangunram|Tiruppur|Tiruppuvanam|Tiruttangal|Tiruvallur|Tiruvannamalai|Tiruvottiyur|Tisaiyanvilai|Tondi|Turaiyur|Udankudi|Udumalaippettai|Usilampatti|Uttamapalaiyam|Uttiramerur|V.S.K.Valasai (Dindigul-Dist.)|Vadakku Valliyur|Vadamadurai|Vadippatti|Valparai|Vandavasi|Vaniyambadi|Vasudevanallur|Vattalkundu|Vedaraniyam|Vellore|Velur|Vettaikkaranpudur|Villupuram|Viravanallur|Virudunagar|Vriddhachalam|Walajapet|Wellington";
        c_a['Telangana']="Adilabad|Andol|Asifabad|Banswada|Bellampalli|Bhadrachalam|Bhaisa|Bhongir|Bodhan|Dasnapur|Devarkonda|Dornakal|Farrukhnagar|Gaddi Annaram|Gadwal|Ghatkesar|Hyderabad|Jagtial|Jangaon|Kamareddi|Karimnagar|Khammam|Kodar|Koratla|Kottagudem|Kukatpalli|Kyathampalle|Lal Bahadur Nagar|Mahbubabad|Mahbubnagar|Malkajgiri|Mancheral|Mandamarri|Manthani|Manuguru|Medak|Mirialguda|Nagar Karnul|Nalgonda|Narayanpet|Naspur|Nirmal|Nizamabad|Paloncha|Palwancha|Patancheru|Peddapalli|Quthbullapur|Ramagundam|Ramgundam|Sadaseopet|Sangareddi|Sathupalli|Secunderabad|Serilingampalle|Siddipet|Singapur|Sirsilla|Sriramnagar|Suriapet|Tandur|Uppal Kalan|Vemalwada|Vikarabad|Wanparti|Warangal|Yellandu|Zahirabad";
        c_a['Tripura']="Agartala|Barjala|Belonia|Dharmanagar|Kailashahar|Khowai|Udaipur";
        c_a['Uttar Pradesh']="Achhnera|Afzalgarh|Agra|Ahraura|Ajodhya|Akbarpur|Aliganj|Aligarh|Allahabad|Amroha|Anupshahr|Aonla|Atarra|Atrauli|Auraiya|Azamgarh|Baberu|Babina|Babrala|Bachhraon|Baghpat|Bah|Baheri|Bahjoi|Bahraigh|Balrampur|Banat|Banda|Bangarmau|Bansdih|Bansi|Baraut|Bareilly|Basti|Behat|Bela|Bewar|Bhadohi|Bharthana|Bharwari|Bhinga|Bhongaon|Bidhuna|Bijnor|Bilari|Bilaspur|Bilgram|Bilhaur|Bilsanda|Bilsi|Bilthra|Bindki|Bisalpur|Bisauli|Biswan|Budaun|Budhana|Bulandshahr|Chandauli|Chandpur|Chanduasi|Charkhari|Charthawal|Chhaprauli|Chharra|Chhata|Chhibramau|Chillupar|Chunar|Colonelganj|Dadri|Dasna|Dataganj|Deoband|Deoranian|Deoria|Dhampur|Dhanaura|Dhaurahra|Dibai|Etawah|Faridpur|Farrukhabad|Fatehabad|Fatehganj West|Fatehpur|Fatehpur Sikri|Firozabad|Fyzabad|Gajraula|Gangoh|Ganj Dundwara|Garhmuktesar|Ghatampur|Ghaziabad|Ghazipur|Ghosi|Gola Gokarannath|Gonda City|Gorakhpur|Govardhan|Greater Noida|Gulaothi|Gunnaur|Gursahaiganj|Gursarai|Haldaur|Hamirpur|Handia|Hapur|Hardoi|Hasanpur|Hastinapur|Hathras|Indergarh|Islamnagar|Itimadpur|Jagdishpur|Jahangirabad|Jais|Jalalabad|Jalali|Jalalpur|Jalaun|Jalesar|Jansath|Jarwal|Jaswantnagar|Jaunpur|Jewar|Jhalu|Jhansi|Jhinjhak|Jhinjhana|Jhusi|Kabrai|Kachhwa|Kaimganj|Kairana|Kakori|Kakrala|Kalpi|Kamalganj|Kandhla|Kannauj|Kanpur|Kant|Kanth|Karhal|Kasganj|Kemri|Khada|Khair|Khairabad|Khalilabad|Khatauli|Khekra|Kheri|Khurja|Khutar|Kiraoli|Kiratpur|Kithor|Konch|Kopaganj|Kosi|Kulpahar|Kunda|Kundarkhi|Laharpur|Lakhimpur|Lalganj|Lalitpur|Lar|Lawar Khas|Loni|Lucknow|Machhlishahr|Maghar|Maharaganj|Mahmudabad|Mahoba|Maholi|Mainpuri|Malihabad|Mandawar|Maniar|Manjhanpur|Marahra|Mariahu|Mathura|Mau|Mau Aimma|Maudaha|Mawana|Meerut|Mehndawal|Milak|Miranpur|Miranpur Katra|Mirganj|Mirzapur|Misrikh|Moradabad|Mubarakpur|Mughal Sarai|Muhammadabad|Muradnagar|Muzaffarnagar|Nagina|Najibabad|Nakur|Nanauta|Nanpara|Narauli|Naraura|Nautanwa|Nawabganj|Nichlaul|Nihtaur|Noida|Nurpur|Obra|Orai|Pachperwa|Padrauna|Pahasu|Palia Kalan|Parichhatgarh|Pawayan|Phalauda|Phaphund|Phulpur|Pihani|Pilibhit|Pilkhua|Pinahat|Pipraich|Pukhrayan|Puranpur|Purwa|Raebareli|Ramnagar|Rampur|Ranipur|Rasra|Rath|Raya|Renukut|Reoti|Richha|Robertsganj|Rudarpur|Rura|Sadabad|Safipur|Saharanpur|Sahaspur|Sahaswan|Sahawar|Saidpur|Sambhal|Samthar|Sandi|Sandila|Sarai Akil|Sarai Mir|Sarauli|Sardhana|Seohara|Shahabad|Shahganj|Shahi|Shahjanpur|Shahpur|Shamli|Shamsabad|Sherkot|Shikarpur|Shikohabad|Shishgarh|Sidhauli|Sikandarabad|Sikandarpur|Sikandra Rao|Sirsaganj|Sirsi|Sisauli|Siswa Bazar|Sitapur|Soron|Suar|Sultanpur|Surianwan|Tajpur|Tanda|Thakurdwara|Thana Bhawan|Tilhar|Tulsipur|Tundla|Ujhani|Un|Unnao|Usehat|Utraula|Varanasi|Vrindavan|Wazirganj|Zaidpur|Zamania";
        c_a['Uttarakhand']="Almora|Bazpur|Clement Town|Dehra Dun|Haldwani|Haridwar|Jaspur|Kashipur|Khatima|Kichha|Kotdwara|Laksar|Manglaur|Mussoorie|Naini Tal|Pauri|Pithoragarh|Raipur|Ramnagar|Ranikhet|Rishikesh|Roorkee|Sitarganj|Srinagar|Tanakpur|Tehri|Uttarkashi";
        c_a['West Bengal']="Adra|Aistala|Amlagora|Amta|Arambagh|Asansol|Ashoknagar Kalyangarh|Baduria|Baghdogra|Bagula|Baharampur|Bahula|Baidyabati|Baj Baj|Balarampur|Bali|Balurghat|Bangaon|Bankra|Bankura|Bansbaria|Barakpur|Baranagar|Barasat|Barddhaman|Baruipur|Beldanga|Bhadreswar|Bhatpara|Birpara|Bishnupur|Bolpur|Canning|Chakapara|Chandannagar|Chandrakona|Chittaranjan|Contai|Dalkola|Dam Dam|Darjiling|Dhulagari|Dhulian|Dhupgari|Diamond Harbour|Dinhata|Dubrajpur|Dumjor|Durgapur|Egra|Falakata|Farakka|Fort Gloster|Gangarampur|Garui|Ghatal|Gobardanga|Gosaba|Goyerkata|Guskhara|Habra|Haldia|Halisahar|Haora|Hasimara|Hugli|Ingraj Bazar|Islampur|Jaigaon|Jalpaiguri|Jamuria|Jangipur|Jaynagar-Majilpur|Jhalida|Jhargram|Kalimpong|Kaliyaganj|Kalna|Kalyani|Kamarhati|Kanchrapara|Kandi|Karsiyang|Katoya|Kenda|Kharagpur|Khardah|Khatra|Koch Bihar|Kolkata|Konnagar|Krishnanagar|Kultali|Kulti|Lakhyabad|Lalgola|Madhyamgram|Mahiari|Mahishadal|Mainaguri|Matabhanga|Medinipur|Memari|Monoharpur|Murshidabad|Nabagram|Naihati|Naksalbari|Nalhati|Nangi|Navadwip|Panchla|Pandua|Panihati|Pujali|Puruliya|Raghunathpur|Raiganj|Rajmahal|Ramjibanpur|Rampur Hat|Ranaghat|Raniganj|Rishra|Sainthia|Sankrail|Shantipur|Shiliguri|Shrirampur|Shyamnagar|Singur|Siuri|Sonamukhi|Srirampur|Taki|Tamluk|Tarakeswar|Titagarh|Tufanganj";




        $('#country').change(function(){
            var c = $(this).val();
            var state_arr = s_a[c].split("|");

            if (c>=0){
                $.each(state_arr, function (i, item_state) {
                    $('#state').append($('<option>', {
                        value: item_state,
                        text: item_state,
                    }, '</option>'));
                });
            }

        });

        $('#state').change(function(){
            var s = $(this).val();

            var city_arr = c_a[s].split("|");
            $('#city').empty();


            $.each(city_arr, function (j, item_city) {
                $('#city').append($('<option>', {
                    value: item_city,
                    text: item_city,
                }, '</option>'));
            });


        });
});



function messageDisplay(message, timeOut, type) {

    type = $.trim(type);
    if (type == "") {
        type = "error";
    }

    if ($.trim(timeOut) == "") {
        timeOut = 1500;
    }

    var element = $("#feedbackSection");
    var color = "#dc3545";
    if (type == "success") {
        color = "#28a745";
    } else if (type == "error") {
        color = "#dc3545";
    }
    element.attr("style", "background-color:" + color);
    $("div#feedbackSection span").html(message);
    element.animate({
        height: 70
    }, 300).show();

    if (timeOut != -1) {
        setTimeout(function () {
            element.animate({
                height: 0
            }, 300, function () {
                element.hide();
            });
        }, timeOut);
    }

}
