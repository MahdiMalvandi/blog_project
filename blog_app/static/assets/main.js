const navItems = document.querySelector(".nav__items");
const navOpenBtn = document.querySelector("#open__nav-btn");
const navCloseBtn = document.querySelector("#close__nav-btn");

const openNav = () => {
  navItems.style.display = "flex";
  navOpenBtn.style.display = "none";
  navCloseBtn.style.display = "inline-block";
};
const closeNav = () => {
  navItems.style.display = "none";
  navCloseBtn.style.display = "none";
  navOpenBtn.style.display = "inline-block";
};

navOpenBtn.addEventListener("click", openNav);
navCloseBtn.addEventListener("click", closeNav);

// dashborad
// const sidebar = document.querySelector("aside");
// const showSidebarBtn = document.querySelector("#show__sidebar-btn");
// const hideSidebarBtn = document.querySelector("#hide__sidebar-btn");

// const showSidebar = () => {
//   sidebar.style.left = "0";
//   showSidebarBtn.style.display = "none";
//   hideSidebarBtn.style.display = "inline-block";
// };
// const hideSidebar = () => {
//   sidebar.style.left = "-100%";
//   showSidebarBtn.style.display = "block";
//   hideSidebarBtn.style.display = "none";
// };

// showSidebarBtn.addEventListener("click", showSidebar);
// hideSidebarBtn.addEventListener("click", hideSidebar);

const copyBtn = document.querySelector(".uil.uil-copy-alt")
const copyText = () => {
  const link = copyBtn.parentElement.firstElementChild.innerHTML
  navigator.clipboard.writeText(link)
}
copyBtn.addEventListener("click", copyText)