function getRadioList()
{
    $.ajax({
        url: "http://43.139.83.100:9000/getradiolist",
        type: "post",
        dataType: "json",
        data: JSON.stringify({

        }),
        success: function(data)
        {
            console.log(data);
            
            var songlisttable = document.getElementById("radiolisttable");
            var songlist = data["songlist"]
            for(var i = 0; i < songlist.length; i++)
            {
                var row = songlisttable.insertRow(-1);
                var orderid = row.insertCell(0);
                var songname = row.insertCell(1);
                var artist = row.insertCell(2);
                var timesplayed = row.insertCell(3);
                var lastplayed = row.insertCell(4);
                orderid.innerHTML = songlist[i][0];
                songname.innerHTML = songlist[i][1];
                artist.innerHTML = songlist[i][2];
                timesplayed.innerHTML = songlist[i][7];
                lastplayed.innerHTML = songlist[i][6];
            }

            // window.location.reload();
        },
        error: function()
        {
            alert("server time out, try later");
            console.trace();
        }
    })
}


function songorder()
{
    $.ajax({
        url: "http://43.139.83.100:9000/songorder",
        type: "post",
        dataType: "json",
        data: JSON.stringify({
            id: sessionStorage.getItem("id"),
            songname: document.getElementById("songnameinput").value,
            artist: document.getElementById("artistinput").value,
            album: document.getElementById("albuminput").value,
            link: document.getElementById("linkinput").value
        }),
        success: function(data)
        {
            console.log(data);
            alert(data["result"]);
            window.location.reload();
        },
        error: function()
        {
            alert("server time out, try later");
            console.trace();
        }
    })
}


function refersh()
{
    window.location.reload();
}