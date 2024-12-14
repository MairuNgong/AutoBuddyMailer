const AddItem=(event)=>{

  event.preventDefault()

  const name = document.getElementById("name").value.trim()
  const email = document.getElementById("email").value.trim()

  const participantList = document.getElementById("participants")

  const listItem = document.createElement("li")
  listItem.innerHTML = `${name} <span>${email}</span><button onclick="RemoveItem(this)">x</button>`
  
  participantList.appendChild(listItem)
  document.getElementById("name").value = ""
  document.getElementById("email").value = ""
}

const RemoveItem =(button)=>{
  const listItem = button.parentElement
  listItem.remove()
}

const SendEmail = (event) => {
  event.preventDefault();
  const participantList = document.getElementById("participants");
  const subject = document.getElementById("subject").value.trim()
  const body = document.getElementById("body").value.trim()
  if (participantList.childElementCount === 0) {
    alert("The participant list is empty!");
  } 
  else {
    const participants = Array.from(participantList.children).map((item) => {
      const name = item.childNodes[0].textContent.trim();
      const email = item.querySelector("span").textContent.trim();
      return { name, email };
    });

    for (const item of participants) {
      console.log(`Name: ${item.name}, Email: ${item.email}`);
    }
    console.log(subject)
    console.log(body)

  }
};