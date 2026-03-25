/*
========================================
 Dataset Image Downloader
 Single click = single download
========================================
*/

document.addEventListener("DOMContentLoaded", function () {

    const images = document.querySelectorAll(".dataset-image");

    images.forEach(img => {

        img.style.cursor = "pointer";

        img.addEventListener("click", function () {
            downloadImage(img);
        });

    });

});


function downloadImage(img) {

    const imageUrl = img.src;

    const filename = imageUrl.split("/").pop();

    const link = document.createElement("a");

    link.href = imageUrl;
    link.download = filename;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
