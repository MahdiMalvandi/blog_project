const copyBtn = document.querySelector(".uil.uil-copy-alt")
const copyText = () => {
  const link = copyBtn.parentElement.firstElementChild.firstElementChild.innerHTML
  navigator.clipboard.writeText(link)

}
copyBtn.addEventListener("click", copyText)