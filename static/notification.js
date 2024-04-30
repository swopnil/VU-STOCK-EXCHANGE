function toggleNotification() {
    var notificationContent = document.getElementById("notification-content");
    if (notificationContent.style.display === "block") {
        notificationContent.style.display = "none";
    } else {
        // Fetch recent actions and populate the notification content
        fetchRecentActions()
            .then(actions => {
                populateNotificationContent(actions);
                notificationContent.style.display = "block";
            })
            .catch(error => console.error('Error fetching recent actions:', error));
    }
}

function fetchRecentActions() {
    // Make a request to fetch recent actions (buy/sell)
    return fetch("/recent_actions")
        .then(response => response.json());
}

function populateNotificationContent(actions) {
    var notificationContent = document.getElementById("notification-content");
    if (actions.length === 0) {
        notificationContent.innerHTML = "<p>No recent actions</p>";
    } else {
        var dropdownHTML = "<ul>";
        actions.forEach(action => {
            dropdownHTML += `<li>${action}</li>`;
        });
        dropdownHTML += "</ul>";
        notificationContent.innerHTML = dropdownHTML;
    }
}
