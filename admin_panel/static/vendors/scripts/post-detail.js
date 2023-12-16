let rmBtn = document.querySelector('.rm-post')
let rmContainer = document.querySelector('.remove-container')
let noBtn = document.querySelector('.no-btn')
let editBtns = document.querySelectorAll('.edit-btn')
let hiddenInput = document.querySelector('.hidden-input')
let textComment = document.querySelector('.text-comment')
let addCommentBtn = document.querySelector('.add-comment-btn')
const openModal = () => {
    rmContainer.classList.remove('hid')
}
const closeModal = () => {
    rmContainer.classList.add('hid')
}
rmBtn.addEventListener('click', openModal)
noBtn.addEventListener('click', closeModal)

editBtns.forEach(item => {
    item.addEventListener('click', () => {
        let id = item.parentElement.parentElement.parentElement.dataset.id
        hiddenInput.value = id
        textComment.innerHTML = `reply to ${id} comment`
        addCommentBtn.classList.remove('hid')
    })
})

addCommentBtn.addEventListener('click', () => {
            textComment.innerHTML = `Add Comment`
    hiddenInput.value = ""
        addCommentBtn.classList.add('hid')
})