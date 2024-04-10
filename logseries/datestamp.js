
function init() {

    var date = new Date();
    var f = document.getElementById("datestampField")
    
    const dateTimeFormat = new Intl.DateTimeFormat('en', { 
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit' 
    })
    f.value = dateTimeFormat.format(date)
}

function validate() {
    var f = document.getElementById("cases")
    console.log("cases=",f.value)
    if (f.value<0 || f.value>10000) {
        alert("You have to enter a number for cases")
        return
    }
    f = document.getElementById("rec")
    console.log("rec=",f.value)
    if (f.value<0 || f.value>10000) {
        alert("You have to enter a number for recovered")
    }
}