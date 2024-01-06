{% block content %}

<script>
document.addEventListener('DOMContentLoaded', function () {
  // Get all elements with data-dropdown attribute
  var dropdowns = document.querySelectorAll('[data-dropdown]');

  // Add click event listener to each dropdown
  dropdowns.forEach(function (dropdown) {
    var button = dropdown.querySelector('[data-dropdown-button]');
    var menu = dropdown.querySelector('.dropdown-menu');

    button.addEventListener('click', function (event) {
      event.stopPropagation();
      menu.classList.toggle('show');
    });

    // Close the menu if user clicks outside of it
    document.addEventListener('click', function (event) {
      if (!dropdown.contains(event.target)) {
        menu.classList.remove('show');
      }
    });
  });
});
</script>
document.addEventListener('click',e=>{
    const isDropdownButton = e.target.matches('[data-dropdown-button]')
    if (!isDropdownButton && e.target.closest('[data-dropdown]') != null) return
    if(isDropdownButton) {
        const currentDropdown = e.target.closest('[data-dropdown]')
        currentDropdown.classList.toggle('active')
    }
    document.querySelectorAll('[data-dropdown].active').forEach(dropdown => {
        if(dropdown === currentDropdown) return
        dropdown.classList.remove('active')
    })
})

{% endblock %}

