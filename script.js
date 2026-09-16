// ==========================================
// SMART HABIT TRACKER
// ==========================================


// Get today's date

const today = new Date();

const todayKey =
    today.getFullYear() +
    "-" +
    String(today.getMonth() + 1).padStart(2, "0") +
    "-" +
    String(today.getDate()).padStart(2, "0");


// Display date

document.getElementById("todayDate").innerText =
    today.toLocaleDateString("en-IN", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"
});


// Load habits from browser storage

let habits =
    JSON.parse(localStorage.getItem("smartHabits")) || [];


// ==========================================
// SAVE DATA
// ==========================================

function saveData() {

    localStorage.setItem(
        "smartHabits",
        JSON.stringify(habits)
    );

}


// ==========================================
// ADD HABIT
// ==========================================

function addHabit() {

    const name =
        document.getElementById("habitInput").value.trim();

    const reminder =
        document.getElementById("reminderInput").value;


    if (name === "") {

        alert("Please enter a habit!");

        return;
    }


    const habit = {

        id: Date.now(),

        name: name,

        reminder: reminder,

        date: todayKey,

        completed: false

    };


    habits.push(habit);

    saveData();

    document.getElementById("habitInput").value = "";

    displayHabits();

    updateStats();

    displayWeekly();

}


// ==========================================
// DISPLAY TODAY'S HABITS
// ==========================================

function displayHabits() {

    const list =
        document.getElementById("habitList");

    list.innerHTML = "";


    const todayHabits =
        habits.filter(habit => habit.date === todayKey);


    if (todayHabits.length === 0) {

        list.innerHTML =
            "<p>No habits added today 🌸</p>";

        return;
    }


    todayHabits.forEach(habit => {

        const div =
            document.createElement("div");

        div.className =
            "habit " +
            (habit.completed ? "completed" : "");


        div.innerHTML = `

            <div class="habit-info">

                <div class="habit-name">
                    ${habit.name}
                </div>

                <div class="reminder">
                    ⏰ Reminder: ${habit.reminder || "Not set"}
                </div>

            </div>


            <div class="actions">

                <button
                    class="complete-btn"
                    onclick="completeHabit(${habit.id})">

                    ${habit.completed ? "↩ Undo" : "✓ Complete"}

                </button>


                <button
                    class="edit-btn"
                    onclick="editHabit(${habit.id})">

                    ✏ Edit

                </button>


                <button
                    class="delete-btn"
                    onclick="deleteHabit(${habit.id})">

                    🗑 Delete

                </button>

            </div>
        `;


        list.appendChild(div);

    });

}


// ==========================================
// COMPLETE HABIT
// ==========================================

function completeHabit(id) {

    const habit =
        habits.find(h => h.id === id);


    if (!habit) return;


    habit.completed =
        !habit.completed;


    saveData();

    displayHabits();

    updateStats();

    displayWeekly();

}


// ==========================================
// DELETE HABIT
// ==========================================

function deleteHabit(id) {

    const confirmDelete =
        confirm("Delete this habit?");


    if (!confirmDelete) return;


    habits =
        habits.filter(h => h.id !== id);


    saveData();

    displayHabits();

    updateStats();

    displayWeekly();

}


// ==========================================
// EDIT HABIT
// ==========================================

function editHabit(id) {

    const habit =
        habits.find(h => h.id === id);


    if (!habit) return;


    const newName =
        prompt("Enter new habit name:", habit.name);


    if (newName === null || newName.trim() === "") {

        return;
    }


    const newReminder =
        prompt(
            "Enter reminder time (HH:MM):",
            habit.reminder
        );


    habit.name =
        newName.trim();


    if (newReminder !== null) {

        habit.reminder =
            newReminder;

    }


    saveData();

    displayHabits();

}


// ==========================================
// UPDATE STATISTICS
// ==========================================

function updateStats() {

    const todayHabits =
        habits.filter(
            h => h.date === todayKey
        );


    const total =
        todayHabits.length;


    const completed =
        todayHabits.filter(
            h => h.completed
        ).length;


    let percentage = 0;


    if (total > 0) {

        percentage =
            Math.round(
                (completed / total) * 100
            );

    }


    document.getElementById("totalHabits")
        .innerText = total;


    document.getElementById("completedHabits")
        .innerText = completed;


    document.getElementById("progressText")
        .innerText = percentage + "%";


    document.getElementById("progressFill")
        .style.width = percentage + "%";


    document.getElementById("streak")
        .innerText = calculateStreak();

}


// ==========================================
// CALCULATE STREAK
// ==========================================

function calculateStreak() {

    let streak = 0;

    let currentDate = new Date();


    while (true) {

        const key =
            currentDate.getFullYear() +
            "-" +
            String(
                currentDate.getMonth() + 1
            ).padStart(2, "0") +
            "-" +
            String(
                currentDate.getDate()
            ).padStart(2, "0");


        const dayHabits =
            habits.filter(
                h => h.date === key
            );


        const hasCompleted =
            dayHabits.some(
                h => h.completed
            );


        if (!hasCompleted) {

            break;

        }


        streak++;


        currentDate.setDate(
            currentDate.getDate() - 1
        );

    }


    return streak;

}


// ==========================================
// WEEKLY VIEW
// ==========================================

function displayWeekly() {

    const weeklyList =
        document.getElementById("weeklyList");

    weeklyList.innerHTML = "";


    for (let i = 6; i >= 0; i--) {

        const date =
            new Date();


        date.setDate(
            date.getDate() - i
        );


        const key =
            date.getFullYear() +
            "-" +
            String(
                date.getMonth() + 1
            ).padStart(2, "0") +
            "-" +
            String(
                date.getDate()
            ).padStart(2, "0");


        const dayHabits =
            habits.filter(
                h => h.date === key
            );


        const total =
            dayHabits.length;


        const completed =
            dayHabits.filter(
                h => h.completed
            ).length;


        let percentage = 0;


        if (total > 0) {

            percentage =
                Math.round(
                    (completed / total) * 100
                );

        }


        const dayDiv =
            document.createElement("div");

        dayDiv.className = "day";


        dayDiv.innerHTML = `

            <span>
                ${date.toLocaleDateString(
                    "en-IN",
                    {
                        weekday: "short",
                        day: "numeric",
                        month: "short"
                    }
                )}
            </span>

            <span>
                ${completed}/${total}
                (${percentage}%)
            </span>

        `;


        weeklyList.appendChild(dayDiv);

    }

}


// ==========================================
// AUTOMATIC REMINDER
// ==========================================

function checkReminders() {

    const now =
        new Date();


    const currentTime =
        String(
            now.getHours()
        ).padStart(2, "0")
        +
        ":" +
        String(
            now.getMinutes()
        ).padStart(2, "0");


    const todayHabits =
        habits.filter(
            h =>
                h.date === todayKey &&
                !h.completed &&
                h.reminder === currentTime
        );


    todayHabits.forEach(habit => {

        const reminderKey =
            "reminded_" +
            habit.id +
            "_" +
            todayKey;


        if (
            !localStorage.getItem(
                reminderKey
            )
        ) {

            alert(
                "⏰ Habit Reminder!\n\n" +
                habit.name
            );


            localStorage.setItem(
                reminderKey,
                "true"
            );

        }

    });

}


// Check reminder every 30 seconds

setInterval(
    checkReminders,
    30000
);


// ==========================================
// INITIAL LOAD
// ==========================================

displayHabits();

updateStats();

displayWeekly();
