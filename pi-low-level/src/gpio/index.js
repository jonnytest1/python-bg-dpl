

let last = 0;
function enablePin(e) {
    const path = e.target.attributes.getNamedItem("path").value + "/main";
    let body = e.target.on ? "disablegpio" : "enablegpio"
    if(!isNaN(+e.target.value) && e.target.value !== "") {
        body = e.target.value
    }

    if(last < Date.now() - 500) {
        last = Date.now();
        fetch(path, {
            method: "POST",
            body: body
        })

    }


    e.target.on = !e.target.on
    e.target.textContent = e.target.on ? "disable" : "enable"

}  