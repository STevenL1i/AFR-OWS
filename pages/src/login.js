function login()
{
    const id = document.getElementById("acctinput").value;
    const pwd = document.getElementById("pwdinput").value;
    
    $.ajax({
        url: "http://43.139.83.100:9000/login",
        type: "post",
        dataType: "json",

        data: JSON.stringify({
            id: id,
            password: pwd
        }),
        success: function(data)
        {
            console.log(data);
            alert(data["validation"])
            if (data["validation"] === "login success")
            {
                sessionStorage.setItem("id", id);
                location.replace("AFR_Website/pages/main");
            }
        },
        error: function()
        {
            alert("server time out, try later");
            console.trace();
        }
    });
}