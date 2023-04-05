$(document).ready(function(){
    $('#bannerCarousel').owlCarousel({
        loop:true,
        lazyLoad:true,
        margin: 0,
        autoplay:true,
        autoplayTimeout:5000,
        smartSpeed: 2000,
        touchDrag  : true,
        mouseDrag  : true,
        dots: true,
        nav: true,
        responsiveClass:true,
        responsive:{
            1366:{
                items:1,
            },
            1024:{
                items:1,
            },
            760:{
                items:1,
            },
            750:{
                items:1,
                nav: false,
            },
            0:{
                items:1,
                nav: false,
            }
        }
    })
    
    $('#categoryCarousel').owlCarousel({
        loop:true,
        lazyLoad:true,
        margin:20,
        autoplay:false,
        autoplayTimeout:5000,
        smartSpeed: 2000,
        touchDrag  : true,
        mouseDrag  : true,
        dots: true,
        nav: true,
        responsiveClass:true,
        responsive:{
            1366:{
                items:4,
            },
            1024:{
                items:3,
            },
            760:{
                items:2,
            },
            0:{
                items:1,
                nav: true,
                dots: false
            }
        }
    })
    
    
    // $('#collectionsCarousel').owlCarousel({
    //     loop:true,
    //     lazyLoad:true,
    //     margin:20,
    //     autoplay:false,
    //     autoplayTimeout:5000,
    //     smartSpeed: 2000,
    //     touchDrag  : true,
    //     mouseDrag  : true,
    //     responsiveClass:true,
    //     responsive:{
    //         1366:{
    //             items:5
    //         },
    //         1024:{
    //             items:5,
    //         },
    //         768:{
    //             items:4,
    //             dots: true,
    //             nav: true
    //         },
    //         0:{
    //             items:1,
    //             nav: true,
    //             dots: false
    //         }
    //     }
    // })
    
    
    $('#feedbackCarousel').owlCarousel({
        loop:true,
        lazyLoad:true,
        margin:20,
        autoplay:true,
        autoplayTimeout:5000,
        smartSpeed: 2000,
        touchDrag  : true,
        mouseDrag  : true,
        dots: false,
        nav: true,
        responsiveClass:true,
        responsive:{
            1366:{
                items:3,
            },
            1024:{
                items:3,
            },
            768:{
                items:2,
                dots: true,
                nav: true
            },
            0:{
                items:1,
                nav: true,
                dots: false
            }
        }
    });
});
