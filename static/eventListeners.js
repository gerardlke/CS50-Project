function closeSearchFriends() {
    const newFriends = document.querySelector('.new-friends');
    newFriends.classList.remove('active-new-friends');
}
try {
    const searchFriendsInput = document.getElementsByClassName('search-friends-list-bar');
    searchFriendsInput[0].addEventListener("blur", closeSearchFriends);
}
catch(err) {}

function setMealChart(meal, chartName, goal) {
    const chart = meal.getElementsByClassName(chartName)[0];
    const nutrition_goal = meal.getElementsByClassName(goal)[0].innerHTML;
    newHeight = (Number(chart.innerHTML) / Number(nutrition_goal) * 100)
    if (newHeight > 100) {
        newHeight = 100;
    }
    newHeight = 100 - newHeight;
    newHeight = newHeight + "%"
    chart.style.height = newHeight;
    chart.style.setProperty('--fill-percentage', newHeight);
}

try{
    window.addEventListener('load', function() {
        meals = document.getElementsByClassName('day-meals');
        for (var i = 0; i < meals.length; i++) {
            const meal = meals[i];
            setMealChart(meal, "calorie-chart-" + (i + 1), "calorie-chart-goal");
            setMealChart(meal, "carbs-chart-" + (i + 1), "carbs-chart-goal");
            setMealChart(meal, "protein-chart-" + (i + 1), "protein-chart-goal");
            setMealChart(meal, "fats-chart-" + (i + 1), "fats-chart-goal");
        }
    })
}
catch(err) {}

try {
    img = document.getElementsByClassName("add-meal-img")[0];
    img.addEventListener("change", function() {
        const file = img.files[0];
        if (file) {
            const filename = file.name;
            document.getElementsByClassName("add-meal-img-file")[0].style.height = '22px';
            document.getElementsByClassName("add-meal-img-file")[0].style.display = 'block';
            document.getElementsByClassName("add-meal-img-file")[0].innerHTML = filename;
        }
    })
} catch(err) {}

try {
    document.getElementsByName("target-weight")[0].addEventListener('change', function() {
        document.getElementsByName("target-calories")[0].value = document.getElementsByName("target-weight")[0].value * 35;
        document.getElementsByName("target-carbs")[0].value = document.getElementsByName("target-weight")[0].value * 4.5;
        document.getElementsByName("target-protein")[0].value = document.getElementsByName("target-weight")[0].value * 1.6;
        document.getElementsByName("target-fats")[0].value = document.getElementsByName("target-weight")[0].value * 0.8;
    })
} catch(err) {}

try {
    document.getElementsByName("edit-target-weight")[0].addEventListener('change', function() {
        document.getElementsByName("edit-target-calories")[0].value = document.getElementsByName("edit-target-weight")[0].value * 35;
        document.getElementsByName("edit-target-carbs")[0].value = document.getElementsByName("edit-target-weight")[0].value * 4.5;
        document.getElementsByName("edit-target-protein")[0].value = document.getElementsByName("edit-target-weight")[0].value * 1.6;
        document.getElementsByName("edit-target-fats")[0].value = document.getElementsByName("edit-target-weight")[0].value * 0.8;
    })
} catch(err) {}

try {
    document.getElementsByClassName("carbs-progress-value")[0].style.strokeDashoffset = 305 - (270 / 100 * Number(document.getElementsByClassName("carbs-progress-text")[0].innerHTML.replace("%", "")));
    document.getElementsByClassName("protein-progress-value")[0].style.strokeDashoffset = 305 - (270 / 100 * Number(document.getElementsByClassName("protein-progress-text")[0].innerHTML.replace("%", "")));
    document.getElementsByClassName("fats-progress-value")[0].style.strokeDashoffset = 305 - (270 / 100 * Number(document.getElementsByClassName("fats-progress-text")[0].innerHTML.replace("%", "")));
} catch(err) {}