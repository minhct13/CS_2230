const dropArea = document.querySelector('.drag-area')
const dragText = dropArea.querySelector('header')
const button = dropArea.querySelector('button')
const input = dropArea.querySelector('input')
let origin_image = NaN

const ori_img = document.getElementById("img-to-crop");

button.addEventListener('click', () => {
    input.click()
})

input.addEventListener('change', function () {
    const file = this.files[0];
    origin_image = file
    showFile(file);

})

dropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    dragText.textContent = "Drop to upload image"
})


dropArea.addEventListener('dragleave', (event) => {
    event.preventDefault();
    dragText.textContent = "Drag and drop to upload image"
})

dropArea.addEventListener('drop', (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    origin_image = file
    showFile(file);
})


let queryImage = NaN
let cropper = NaN
function showFile(file) {
    const fileType = file.type;
    const validExtensions = ['image/jpeg', 'image/jpg', 'image/png'];
    if (validExtensions.includes(fileType)) {
        const fileReader = new FileReader();
        fileReader.onload = () => {
            const fileUrl = fileReader.result;
            imgTag = document.createElement("img")
            imgTag.id = "img-to-crop"
            imgTag.src = fileUrl
            imgTag.style="max-height: 50vh"
            while (dropArea.firstChild) {
                dropArea.removeChild(dropArea.lastChild);
            }
            dropArea.appendChild(imgTag)
            var options = {
                dragMode: 'move',
                viewMode: 2,
                modal: false,
                background: false,
            }
            cropper = new Cropper(imgTag, options);
            
        }
        fileReader.readAsDataURL(file);
    }
    else {
        alert("This is not image format, please choose again!");
        dragText.textContent = "Drag and drop to upload image"
    }
}

// =========================================

const submit_btn = document.getElementById('btn-1')
const refresh_btn = document.getElementById('btn-2')

submit_btn.addEventListener('click', () => {
    queryImage = cropper.getCroppedCanvas().toDataURL("image/png");
    // queryImage = btoa(queryImage)
    localStorage.setItem('queryImage', queryImage);
    window.open("/query.html", "_self")

})


refresh_btn.addEventListener('click', () => {
    location.reload();
})
