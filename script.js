document.getElementById("input_data").addEventListener("submit", async function(e){
    e.preventDefault();

    const formData = new FormData(this);

    const res = await fetch('http://127.0.0.1:8000/', {
        method: 'POST',
        body: formData
    })

    const result = await res.json();
    
    const totalColumns = result.availableColumns;
    const qualitativeCol = result.qualitative;
    const quantitativeCol = result.quantitative;

    JSON.stringify(quantitativeCol);
    JSON.stringify(qualitativeCol);
    JSON.stringify(totalColumns);
    
    console.log(result);

    document.getElementById("columns").innerText = totalColumns;
    document.getElementById("qualitative").innerText = `Qualitative: ${qualitativeCol}`;
    document.getElementById("quantitative").innerText = `Quantitative: ${quantitativeCol}`;

    document.getElementById("columnNames").style.visibility = "visible";
    
})

document.getElementById("columnNames").addEventListener("submit", async function(e){
    e.preventDefault();

    const formm2 = new FormData(document.getElementById("input_data"));
    const input_text = document.getElementById("input_text").value;
    formm2.append("input_text", input_text);

    console.log(formm2);
    // get image details based on previous column names.

    const res2 = await fetch('http://127.0.0.1:8000/plot', {
        method: 'POST',
        body: formm2
    });

    const result2 = await res2.json();
    console.log(result2);

    document.getElementById("columnNames").style.visibility = "hidden";

    const img = document.createElement("img");
    img.src = result2.plot1;

    const barImg = document.createElement("img");
    barImg.src = result2.plot2;

    // const pieImg = document.createElement("img");
    // pieImg.src = result2.plot3;

    const scatterImg = document.createElement("img");
    scatterImg.src = result2.plot4;
    
    const histImg = document.createElement("img");
    histImg.src = result2.plot5;

    document.getElementById("basicplots").appendChild(img);
    document.getElementById("basicplots").appendChild(barImg);
    // document.getElementById("basicplots").appendChild(pieImg);
    document.getElementById("basicplots").appendChild(scatterImg);
    document.getElementById("basicplots").appendChild(histImg);
    // document.getElementById("columns").innerText = result.availableColumns;

    // document.getElementById("basicplots").appendChild(img);
})
