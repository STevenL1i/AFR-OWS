function login()
{
    const acct = document.getElementById("acctinput").value;
    const pwd = document.getElementById("pwdinput").value;
    
    $.ajax({
        url: "http://localhost:9000/login",
        type: "post",
        dataType: "json",

        data: JSON.stringify({
            username: acct,
            password: pwd
        }),
        success: function(data)
        {
            alert("logined");
            console.log(data);
        },
        error: function()
        {
            alert("failed");
            console.log("failed");
        }
    });
}