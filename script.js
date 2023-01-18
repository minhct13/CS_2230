const dropArea = document.querySelector('.drag-area')
const dragText = dropArea.querySelector('header')
const button = dropArea.querySelector('button')
const input = dropArea.querySelector('input')
let origin_image = NaN

const ori_img = document.getElementById("img-to-crop");
ori_img.style.display = "none";

button.addEventListener('click', ()=>{
    input.click()
})

input.addEventListener('change', function (){
    const file = this.files[0];
    origin_image = file
    showFile(file);
    
})

dropArea.addEventListener('dragover', (event)=>{
    event.preventDefault();
    dragText.textContent = "Drop to upload image"
})


dropArea.addEventListener('dragleave', (event)=>{
    event.preventDefault();
    dragText.textContent = "Drag and drop to upload image"
})

dropArea.addEventListener('drop', (event)=>{
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    origin_image = file
    showFile(file);
})

function showFile(file){
    const fileType = file.type;
    const validExtensions = ['image/jpeg', 'image/jpg', 'image/png'];
    if (validExtensions.includes(fileType)){
        const fileReader = new FileReader();
        fileReader.onload = () => {
            const fileUrl = fileReader.result;
            imgTag = `<img src="${fileUrl}">`
            dropArea.innerHTML = imgTag
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

submit_btn.addEventListener('click', ()=>{
    const file = origin_image
    show(file)
    addCropper()
})

function show(file){
    const fileReader = new FileReader();
    fileReader.onload = () => {
        const fileUrl = fileReader.result;
        ori_img.src = fileUrl;
        console.log(ori_img)
        ori_img.style.display = "block";
    }
    fileReader.readAsDataURL(file);
}

refresh_btn.addEventListener('click', ()=>{
    location.reload();
})

// =========================================

let cropper = NaN
// const image_to_crop = document.getElementById("origin-image")
function addCropper(){
    cropper = new Cropper(ori_img, {
        aspectRatio: 0,
        viewMode: 0,    
    });
}
// const img = document.getElementById("test")
// cropper = new Cropper(img, {
//     aspectRatio: 0,
//     viewMode: 0,    
// });


