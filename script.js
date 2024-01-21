// window.open("popup.html", "XTree", "width=600,height=400");

document.getElementById("btn").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default form submission

    var url = document.getElementsByName('url')[0].value; // Get the value of the input field
    var tag = document.getElementsByName('tag')[0].value;
    var cname = document.getElementsByName('class_name')[0].value;
    var fname = document.getElementsByName('file_name')[0].value;
    console.log("Inputs triggered");
    scrape(url, tag, cname, fname);
});

function scrape(sUrl, tag, cont, fname) {
    var dwUrl;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "https://scrape-uoalk4whka-uc.a.run.app");
    xhr.responseType = 'json';
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    const body = JSON.stringify({
        "data": {
            "url": sUrl,
            "tag": tag,
            "cont": cont,
            "fname": fname
        }
    });

    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log("success");
            console.log(xhr.response);
            dwUrl = xhr.response['result']['message'];
            downloadURI(dwUrl, fname + ".csv")

        } else {
            throw new Error("Error: ${xhr.status}");
        }
    };
    console.log("sent request");
    xhr.send(body);
}

function downloadURI(uri, name) {
    var link = document.createElement("a");
    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
}
