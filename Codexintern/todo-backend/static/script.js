let token = "";

// Register User
async function register() {
    const username = document.getElementById("regUser").value;
    const password = document.getElementById("regPass").value;

    const res = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    alert(data.message || "Registered");
}

// Login User
async function login() {
    const username = document.getElementById("loginUser").value;
    const password = document.getElementById("loginPass").value;

    const res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    token = data.access_token || data.token;

    if (token) {
        document.getElementById("todoSection").style.display = "block";
        loadTodos();
    } else {
        alert("Login failed!");
    }
}

// Create Todo
async function createTodo() {
    const title = document.getElementById("todoTitle").value;
    const description = document.getElementById("todoDesc").value;

    await fetch("/todos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ title, description })
    });

    document.getElementById("todoTitle").value = "";
    document.getElementById("todoDesc").value = "";
    loadTodos();
}

// Load Todos
async function loadTodos() {
    const res = await fetch("/todos", {
        headers: { "Authorization": "Bearer " + token }
    });
    const todos = await res.json();

    const list = document.getElementById("todoList");
    list.innerHTML = "";

    todos.forEach(todo => {
        const li = document.createElement("li");
        li.innerHTML = `
            <span class="${todo.done ? 'done' : ''}">
                ${todo.title} - ${todo.description}
            </span>
            <div class="todo-actions">
                <button class="done" onclick="markDone(${todo.id})">Done</button>
                <button onclick="updateTodo(${todo.id})">Update</button>
                <button class="delete" onclick="deleteTodo(${todo.id})">Delete</button>
            </div>
        `;
        list.appendChild(li);
    });
}

// Mark as Done
async function markDone(id) {
    await fetch(`/todos/${id}/mark-done`, {
        method: "PATCH",
        headers: { "Authorization": "Bearer " + token }
    });
    loadTodos();
}

// Update Todo (prompt for new values)
async function updateTodo(id) {
    const newTitle = prompt("Enter new title:");
    const newDesc = prompt("Enter new description:");
    if (!newTitle && !newDesc) return;

    await fetch(`/todos/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ title: newTitle, description: newDesc })
    });
    loadTodos();
}

// Delete Todo
async function deleteTodo(id) {
    await fetch(`/todos/${id}`, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + token }
    });
    loadTodos();
}
