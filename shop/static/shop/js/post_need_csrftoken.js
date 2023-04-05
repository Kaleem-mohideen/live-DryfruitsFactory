$(function () {
  $.ajaxsetup ({
    headers:{"x-csrftoken":getcookie ("csrftoken")}
  });
});
    //To prevent csrf (cross-site request forgery) cross-site request forgery,When making a post request, you need to create a random code in the cookie
    function getcookie (name)
    {
      var arr, reg=new regexp ("(^ |)" + name + "= ([^;] *) (;| $)");
      /*
        The above sentence is equivalent to:
      var arr;
      var reg=new regexp ("(^ |)" + name + "= ([^;] *) (;| $)");
       * /
      if (arr=document.cookie.match (reg))
        return decodeuri (arr [2]);//ecmascript v3 has removed the unescape () function from the standard and opposes its use,                      //So decodeuri () and decodeuricomponent () should be used instead.
      else
        return null;
    }
