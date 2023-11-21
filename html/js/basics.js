function showElement(element_id) {
  var x = document.getElementById(element_id);
  if (x.style.display === "none") {
    x.style.display = "table";
  } else {
    x.style.display = "none";
  }
}