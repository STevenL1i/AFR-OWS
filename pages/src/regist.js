function initializepage()
{
    $.ajax({
        url: "http://43.139.83.100:9000/getrace",
        type: "post",
        dataType: "json",
        data: JSON.stringify({}),
        success: function(data)
        {
            console.log(data);
            document.getElementById("round").innerHTML = data[0][0];
            document.getElementById("GP").innerHTML = data[0][2];
            sessionStorage.setItem("round", data[0][0]);
            sessionStorage.setItem("GP", data[0][3]);
        },
        error: function()
        {
            alert("server time out, try later");
            console.trace();
        }
    })
}


function getRegistration()
{
    const round = sessionStorage.getItem("round");
    const gp = sessionStorage.getItem("GP");

    $.ajax({
        url: "http://43.139.83.100:9000/getregist",
        type: "post",
        dataType: "json",
        data: JSON.stringify({
            "round": round,
            "GP": gp
        }),
        success: function(data)
        {
            console.log(data);

            var a1table = document.getElementById("A1regtable");
            var a1reg = data["A1"];
            for(var i = 0; i < a1reg.length; i++)
            {
                var row = a1table.insertRow(-1);
                var drivercell = row.insertCell(0);
                var regtimecell = row.insertCell(1);
                drivercell.innerHTML = a1reg[i][0];
                regtimecell.innerHTML = a1reg[i][5];
            }
            var row = a1table.insertRow(-1);
            var drivercounttag = row.insertCell(0);
            var drivercountcell = row.insertCell(1);
            drivercounttag.innerHTML = "";
            drivercountcell.innerHTML = a1reg.length + "人";


            var a2table = document.getElementById("A2regtable");
            var a2reg = data["A2"];
            for(var i = 0; i < a2reg.length; i++)
            {
                var row = a2table.insertRow(-1);
                var drivercell = row.insertCell(0);
                var regtimecell = row.insertCell(1);
                drivercell.innerHTML = a2reg[i][0];
                regtimecell.innerHTML = a2reg[i][5];
            }
            var row = a2table.insertRow(-1);
            var drivercounttag = row.insertCell(0);
            var drivercountcell = row.insertCell(1);
            drivercounttag.innerHTML = "";
            drivercountcell.innerHTML = a2reg.length + "人";


            var a3table = document.getElementById("A3regtable");
            var a3reg = data["A3"];
            for(var i = 0; i < a3reg.length; i++)
            {
                var row = a3table.insertRow(-1);
                var drivercell = row.insertCell(0);
                var regtimecell = row.insertCell(1);
                drivercell.innerHTML = a3reg[i][0];
                regtimecell.innerHTML = a3reg[i][5];
            }
            var row = a3table.insertRow(-1);
            var drivercounttag = row.insertCell(0);
            var drivercountcell = row.insertCell(1);
            drivercounttag.innerHTML = "";
            drivercountcell.innerHTML = a3reg.length + "人";

        },
        error: function()
        {
            alert("server time out, try later");
            console.trace();
        }
    })
}


function driverRegist()
{
    $.ajax({
        url: "http://43.139.83.100:9000/driverregist",
        type: "post",
        dataType: "json",
        data: JSON.stringify({
            id: sessionStorage.getItem("id"),
            gp: sessionStorage.getItem("GP"),
            racegroup: document.getElementById("racegroup").value
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

function driverWithdraw()
{
    $.ajax({
        url: "http://43.139.83.100:9000/driverwithdraw",
        type: "post",
        dataType: "json",
        data: JSON.stringify({
            id: sessionStorage.getItem("id"),
            gp: sessionStorage.getItem("GP"),
            racegroup: document.getElementById("racegroup").value
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