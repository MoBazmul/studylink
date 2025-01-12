const iconBtn = document.querySelector('i')
const navBar = document.querySelector('nav')
const fieldSet = document.querySelector('.fields-set')
const editForm = document.querySelector('.edit')
const year = document.querySelector('.year')
const formClass = document.querySelector('.form-class')
const addBtn = document.querySelector(".fa-plus")
const deleteBtn = document.querySelector('.deleteBtn')
const repliesBtn = document.querySelector('.replies')
const closeReplies = document.querySelector('.close-replies')
const replySection = document.querySelector(".reply-section")
const messageContent = document.querySelector('.message-content')
const display = document.querySelector('.display')
const more = document.querySelector('.more')
const unhide = document.querySelector('.hide-p')
const actionBtn = document.querySelector('.action')
const cancelBtn = document.querySelector('.cancel')
const confirmField = document.querySelector('.confirm-delete')
const homeUrl = "home";


if(year) {
  year.innerText = new Date().getFullYear()
}

if(repliesBtn) {
  repliesBtn.addEventListener("click", () => {
    replySection.style.display = "block"
    closeReplies.style.display = "block"
  })
}

if(closeReplies) {
  closeReplies.addEventListener("click", () => {
    replySection.style.display = "none"
    closeReplies.style.display = "none"
  })
}

if(actionBtn) {
  actionBtn.addEventListener('click', () => {
    confirmField.style.display = "block"
  })
}

if(cancelBtn) {
  cancelBtn.addEventListener('click', () => {
    confirmField.style.display = "none"
  })
}

if(more) {
  more.addEventListener('click', () => {
    unhide.style.display = "block"
    more.innerHTML = ""
  })
}

if (messageContent) {
  const messages = [
    "Discover high-quality, peer-reviewed study materials shared by other students in your courses",
    "Add resources that you find effective and help your peers succeed in their studies",
    "Connect with like-minded students and expand your academic network through shared courses and social media links",
    "Engage with a community of learners and exchange valuable study materials to enhance your academic experience"
  ];

  let messageIndex = 0;

  const changeMessage = () => {
    messageContent.classList.add('fade-out');

    setTimeout(() => {
      messageContent.innerText = messages[messageIndex];
      messageContent.classList.remove('fade-out');
      messageIndex = (messageIndex + 1) % messages.length;
    }, 500);
  };

  setInterval(changeMessage, 5000);
}

document.querySelectorAll('.save-resource').forEach((element) => {
  element.addEventListener('click', () => {
    const userId = element.getAttribute('data-key');
    const resourceId = element.getAttribute('data-another-key');

    fetch('/save_resource', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token() }}'
      },
      body: JSON.stringify({ user_id: userId, resource_id: resourceId })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('Resource saved successfully!');
      } else {
        console.log('Failed to save resource: ' + data.message);
      }
    })
    .catch(error => console.error('Error:', error));
  });
});


document.querySelectorAll('.fa-trash-o').forEach(element => {
  element.addEventListener('click', function() {
    const resourceId = this.getAttribute('data-key');

    fetch('/delete_resource', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token() }}'
      },
      body: JSON.stringify({ resource_id: resourceId })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('Resource deleted successfully!');
        location.reload();
      } else {
        console.log('Failed to delete resource.');
      }
    })
    .catch(error => console.error('Error:', error));
  });
});

iconBtn.addEventListener('click', () => {
  if (iconBtn.classList.contains('fa-bars') && !navBar.classList.contains('header__navbar')) {
    navBar.classList.add('header__navbar')
    iconBtn.classList.remove('fa-bars')
    iconBtn.classList.add('fa-times')
    iconBtn.style.fontSize = '40px';
  }
  else {
    navBar.classList.remove('header__navbar')
    iconBtn.classList.remove('fa-times')
    iconBtn.classList.add('fa-bars')
    iconBtn.style.fontSize = '30px';
  }
})

if(editForm) {
  editForm.addEventListener('click', () => {
    if(!formClass.classList.contains('transform')) {
      formClass.classList.remove('form-class')
      formClass.classList.add('transform')
    }
  })
}

if (deleteBtn) {
  deleteBtn.addEventListener('click', () => {
    fetch('/delete_account', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token() }}' 
      },
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.location.href = homeUrl; 
      } else {
        console.error('Failed to delete account:', data.message);
      }
    })
    .catch(error => console.error('Error:', error));
  });
}





