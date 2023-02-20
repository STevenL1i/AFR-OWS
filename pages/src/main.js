function showprofile()
{
    const id = sessionStorage.getItem("id");
    
    $.ajax({
        url: "http://43.139.83.100:9000/getprof",
        type: "post",
        dataType: "json",

        data: JSON.stringify({
            id: id
        }),
        success: function(data)
        {
            console.log(data);
            
        },
        error: function()
        {
            alert("server time out, try later");
            console.trace();
        }
    });
}