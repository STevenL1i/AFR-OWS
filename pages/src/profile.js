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
            document.getElementById("driverid").innerHTML = id;
            document.getElementById("drivergroup").innerHTML = data["group"];
            document.getElementById("team").innerHTML = data["team"];
            document.getElementById("driverstatus").innerHTML = data["status"];
            document.getElementById("joindate").innerHTML = data["joindate"];
        },
        error: function()
        {
            alert("server time out, try later");
            console.trace();
        }
    });
}

function refersh()
{
    window.location.reload();
}