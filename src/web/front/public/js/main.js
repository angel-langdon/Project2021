/*------------------------------------------------------------------
 * Theme Name: Designway Template
 * Theme URI: http://www.brandio.io/envato/designway
 * Author: Brandio
 * Author URI: http://www.brandio.io
 * Description: A Bootstrap Responsive HTML5 Template
 * Version: 1.0
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * Bootstrap v3.3.7 (http://getbootstrap.com)
 * Copyright 2017 Brandio.
 -------------------------------------------------------------------*/
"use strict";

// Add Slider functionality to the offices images.
$(".offices-slider","#info1").slick({
    dots: true,
    arrows: false,
    speed: 200
});

// Add Slider functionality to the testimonials.
$(".testimonials-slider","#testimonials").slick({
    dots: true,
    arrows: false,
    speed: 200
});

$(window).on("load", function() {
    // MainMenu button toggle function.
    $("#toggle-menu","#header").on("click", function(){
        $("#menu-holder","#header").toggleClass('hide-menu');
    });
    
    // Load Succes stories projects list from the Json file.
    var projectList = $(".projects-list", "#recent-studies");
    var projectBox = $(".project-box a","#recent-studies");
    
    $.getJSON( "data/data.json", function( data ) {
        var items = "";
        var prolength = 8;
        
        if(projectList.hasClass("full-list")){
            prolength = data.projects.length;
        }
        for(var i=0;i<prolength;i++){
            items += "<div class='col-xs-12 col-sm-6 col-md-3 project-box-holder'><div class='project-box'><a href='#' data-id='"+ i +"'><img class='project-img' src='" + data.projects[i].preview.img + "'  alt=''><div class='box-overlay'><h4>" + data.projects[i].preview.title + "</h4></div></a></div></div>";
        }
        projectList.html(items);

    }).done(function() {
        
    }).fail(function() {
        
    }).always(function() {
        // Adding click function to the project button to the popup for details.
        $(".project-box a","#recent-studies").on("click",function(e){
            e.preventDefault();
            loadProject($(this).data("id"));
            return false;
        });
    });
    
    // Load the project details from the Json file.
    var caseStudyPopup = $('#case-study-popup');
    var pageHolder = $('.page-holder');
    var projectSlider = $(".project-slider","#case-study-popup");
    
    function loadProject(projectId){
        caseStudyPopup.addClass("loading");
        caseStudyPopup.addClass("open");
        pageHolder.addClass("back");
        
        $.getJSON( "data/data.json", function( data ) {
            var items = "";
            $.each( data.projects[projectId].images, function( key, val ) {
                items += "<div><img src=" + val + " alt=" + key + "></div>";
            });
            
            projectSlider.html(items);
            projectSlider.slick({dots: true,arrows: false,speed: 200});
            
            $(".details-holder .project-title","#case-study-popup").html(data.projects[projectId].details.title);
            $(".details-holder .info-text","#case-study-popup").html(data.projects[projectId].details.info);
            $(".details-holder .skills","#case-study-popup").html(data.projects[projectId].details.skills);
            $(".details-holder .datecompleted","#case-study-popup").html(data.projects[projectId].details.datecompleted);
            $(".details-holder .dw-button-link","#case-study-popup").attr('href',data.projects[projectId].details.link);
            
        }).done(function() {
            
        }).fail(function() {
            
        }).always(function() {
            caseStudyPopup.removeClass("loading");
            projectSlider.slick({dots: true,arrows: false,speed: 200});
        });
    }
    
    // Adding click function to the close button in the project popup box.
    $("#closebtn","#case-study-popup").on("click",function(e){
        e.preventDefault();
        caseStudyPopup.removeClass("open");
        pageHolder.removeClass("back");
        projectSlider.slick('unslick');
        return false;
    });
    
    // About us page "aboutus.html"
    // Fix image resize issue.
    var storyImgHolder1 = $(".image-holder", "#story1");
    var storyText1 = $(".txt-col","#story1");
    var storyImgHolder2 = $(".image-holder", "#story2");
    var storyText2 = $(".txt-col","#story2");
    
    //// Popup slider images height fix
    var popupContent = $(".popup-content", "#case-study-popup");
    var projectSlider = $(".project-slider", "#case-study-popup");
    
    if ($(window).width() > 990) {
        storyImgHolder1.css("height",storyText1.height()+140);
        storyImgHolder2.css("height",storyText2.height()+140);
        
        //// Popup slider images height fix
        projectSlider.css("height",popupContent.height());
    }
    // About us page "aboutus.html"
    // Fix image resize issue when the window resized
    $(window).on("resize",function() {
        if ($(window).width() > 990) {
            storyImgHolder1.css("height",storyText1.height()+140);
            storyImgHolder2.css("height",storyText2.height()+140);
            
            //// Popup slider images height fix
            projectSlider.css("height",popupContent.height());
        }else{
            projectSlider.css("height","inherit");
        }
        return false;
    });
    
    // Contact form function.
    var form = $('#contactform');
    var formMessages = $('#form-messages');
    var ajaxButton = $('.ajax-button','#contactform');
    
    $(form).submit(function(e) {
        e.preventDefault();
        ajaxButton.addClass('sending');
        var formData = $(form).serialize();
        $.ajax({
            type: 'POST',
            url: $(form).attr('action'),
            data: formData
        }).done(function(response) {
            ajaxButton.removeClass('sending');
            $(formMessages).removeClass('error');
            $(formMessages).addClass('success');
            $(formMessages).text(response);

            $('#name','#contactform').val('');
            $('#email','#contactform').val('');
            $('#message','#contactform').val('');
        }).fail(function(data) {
            ajaxButton.removeClass('sending');
            $(formMessages).removeClass('success');
            $(formMessages).addClass('error');

            if (data.responseText !== '') {
                $(formMessages).text(data.responseText);
            } else {
                $(formMessages).text('Oops! An error occured and your message could not be sent.');
            }
        });
    });
    
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        $(document).off("scroll");

        var target = this.hash;
        var $target = $(target);
        
        if ($target.length) {
            var theTarget = $target.offset().top;
        }else{
            var theTarget = 0;
        }
        
        $('html, body').stop().animate({
            'scrollTop': theTarget
        }, 900, 'swing', function() {
            window.location.hash = target;
        });
    });
});
