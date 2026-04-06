function Cancelpost()
{
    document.getElementById("title").value="";
    document.getElementById("destination").value="";
    document.getElementById("date").value="";
    document.getElementById("description").value="";
    document.getElementById("images").value="";
    document.getElementById("title").focus();
    document.getElementById("video").value="";
}

function load_cursor()
{
    document.getElementById("title").focus();
}



function Email(emailField)
{
    var reg = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (reg.test(emailField.value) == false)
    {
        alert("Invalid email, please check your email");
        return false;
    }
    return true;
}