const url = "http://localhost:8000/sent-emails";

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
    const data = {
      participants: Array.from(participantList.children).reduce((acc, item) => {
        const name = item.childNodes[0].textContent.trim();
        const email = item.querySelector("span").textContent.trim();
        acc[name] = email;
        return acc;
      }, {}),
      subject: subject,
      template: body,
    };

    Postdata(url,data)
  }
};


async function Postdata(url,data) {
  try{
    const response = await fetch(url,{
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data),
    })

    if (!response.ok){
      
      throw new Error(`Error : ${response.status}`)
    }

    const responseData = await response.json()
    console.log("Response data:", responseData)
    alert("Email sent successfully")
  }
  catch(error){
    console.error("Error", error)
    alert(`Error: ${error}`)
  }
}