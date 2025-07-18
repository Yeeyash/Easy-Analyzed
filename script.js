document.getElementById("input_data").addEventListener("submit", async function(e){
    e.preventDefault();

    const formData = new FormData(this);

    const res = await fetch('http://127.0.0.1:8000/', {
        method: 'POST',
        body: formData
    })

    const result = await res.json();
    console.log(result);

    //loading images from API:
    const img = document.createElement("img");
    img.src = result.plot;

    // img.width = 150;
    // // img.height = "auto";

    document.getElementById("basicplots").appendChild(img)
})