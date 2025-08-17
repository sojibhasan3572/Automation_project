setTimeout(function(){
    $('#messages').fadeOut('slow')
}, 5000)

 const closeButtons = document.querySelectorAll('.close');
  closeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      btn.parentElement.style.display = 'none';
    });
  });