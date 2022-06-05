const cont_btn = document.getElementById("continue");

cont_btn.addEventListener("click", async function(){
    let ackn = document.getElementById("acknowledge");
    let img_graph = document.getElementById("chart");
    let sample_cap = document.getElementById("sample_desc");
    let img_sample =document.getElementById("table");

    let data = {"url": document.getElementById("url").value};
    console.log("Sending URL:", data.url);
    ackn.textContent = "Analyzing Tweet...";

    let result = await sendPostRequest("/analyzeTweet", data);
    let image = await sendGetFile("/getImage");
    let sample = await sendGetFile("/getSample");

    ackn.textContent = "";
    img_graph.src = URL.createObjectURL(image);
    sample_cap.textContent = "Random Sample of Replies:";
    img_sample.src = URL.createObjectURL(sample);
});
