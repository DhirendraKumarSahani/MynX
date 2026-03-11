async function sendMessage(){

const input = document.getElementById("user-input")
const message = input.value.trim()

if(!message) return

const chatBox = document.getElementById("chat-messages")

// ======================
// AI Loading animation
// ======================

let loading = document.createElement("div")

loading.className = "ai-loading"

loading.innerHTML = `
<span></span>
<span></span>
<span></span>
`

chatBox.appendChild(loading)

/* -------------------------------
USER MESSAGE
-------------------------------- */

const userDiv = document.createElement("div")
userDiv.className = "user-msg"
userDiv.innerText = message

chatBox.appendChild(userDiv)

input.value = ""

loading.remove()
/* -------------------------------
AI MESSAGE CONTAINER
-------------------------------- */

let aiDiv = document.createElement("div")
aiDiv.className = "ai-msg"

/* ACTION BUTTONS */

let actions = document.createElement("div")
actions.className = "message-actions"

actions.innerHTML = `
<button class="copy-btn">Copy</button>
`

/* CONTENT AREA */

let content = document.createElement("div")
content.className = "ai-content"

/* APPEND */

aiDiv.appendChild(actions)
aiDiv.appendChild(content)

chatBox.appendChild(aiDiv)


/* -------------------------------
API CALL
-------------------------------- */

const response = await fetch("/api/v1/chat/stream",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
query:message,
thread_id:"web-user"
})
})

const reader = response.body.getReader()
const decoder = new TextDecoder()

let fullText = ""

/* -------------------------------
STREAM LOOP
-------------------------------- */

while(true){

const {done,value} = await reader.read()

if(done) break

const chunk = decoder.decode(value)

const events = chunk.split("\n\n")

events.forEach(event => {

if(event.startsWith("data:")){

const clean = event.replace("data:", "").trim()

try{

const parsed = JSON.parse(clean)

if(parsed.token){

/* ACCUMULATE TEXT */

fullText += parsed.token

/* FIX BROKEN NUMBERED LIST */

fullText = fullText.replace(/(\d+)\.\n/g,"$1. ")

/* RENDER MARKDOWN */

content.innerHTML = marked.parse(fullText) + '<span class="typing-cursor"></span>'

/* ADD COPY BUTTONS TO CODE */

addCodeCopyButtons()

/* AUTO SCROLL */

chatBox.scrollTop = chatBox.scrollHeight

}

if(parsed.done){

console.log(
"%c🚀 AI Response Stream Finished",
"background:#0f172a; color:#38bdf8; padding:6px 12px; font-weight:bold; border-radius:6px;"
)

// remove typing cursor
document.querySelector(".typing-cursor")?.remove()

}

}catch(e){

console.log("Parse error:", clean)

}

}

})

}


/* -------------------------------
SYNTAX HIGHLIGHT
-------------------------------- */

document.querySelectorAll("pre code").forEach((block)=>{

if(!block.dataset.highlighted){

hljs.highlightElement(block)

}

})


/* -------------------------------
MATH RENDER
-------------------------------- */

renderMathInElement(content,{
delimiters:[
{left:"$$", right:"$$", display:true},
{left:"$", right:"$", display:false}
]
})

}



/* ======================================
COPY AI MESSAGE BUTTON
====================================== */

document.addEventListener("click",function(e){

if(e.target.classList.contains("copy-btn")){

const message = e.target.closest(".ai-msg")
.querySelector(".ai-content").innerText

navigator.clipboard.writeText(message)

e.target.innerText = "Copied!"

setTimeout(()=>{
e.target.innerText = "Copy"
},1500)

}

})



/* ======================================
CODE BLOCK COPY BUTTON
====================================== */

function addCodeCopyButtons(){

document.querySelectorAll("pre").forEach((block)=>{

if(block.querySelector(".code-copy")) return

let btn = document.createElement("button")
btn.className = "code-copy"
btn.innerText = "Copy"

btn.style.position = "absolute"
btn.style.top = "6px"
btn.style.right = "6px"
btn.style.fontSize = "12px"

block.style.position = "relative"

block.appendChild(btn)

btn.onclick = ()=>{

navigator.clipboard.writeText(block.innerText)

btn.innerText = "Copied!"

setTimeout(()=>{
btn.innerText = "Copy"
},1200)

}

})

}