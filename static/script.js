function getAxisValues(axis) {
    var ValuesDivs = document.getElementById(axis); 
    var ValuesDiv = ValuesDivs.getElementsByTagName('div');
    const Values = [];
    for (var i = 0; i < ValuesDiv.length; i++) {
        Values.push(ValuesDiv[i].innerHTML);
    }
    return Values;
}
function getGoalValues(axis, dataPoints) {
    const num = dataPoints.length;
    const Values = [];
    for (var i = 0; i < num; i++) {
        if (axis) {
            Values.push(document.getElementsByClassName(axis)[0].innerHTML);
        } else {
            Values.push('0');
        }
    }
    return Values;
}

chart1 = new Chart(document.getElementById('caloricLineChart').getContext('2d'), {
    type: 'line',
    data: {
        labels: getAxisValues('caloricLineChartXValues'),
        datasets: [{
            label: 'Calories',
            fill: false, 
            lineTension: 0, 
            data: getAxisValues('caloricLineChartYValues'),
            backgroundColor: '#1b1b1b', 
            borderColor: '#1b1b1b', 
            pointRadius: 5, 
            pointHoverRadius: 10, 
            pointBackgroundColor: '#1b1b1b', 
            pointBorderColor: '#1b1b1b'
        },
        { 
            label: 'Target', 
            data: getGoalValues('caloricGoalValue', getAxisValues('caloricLineChartXValues')),
            borderColor: '#f00', 
            backgroundColor: '#f00', 
            borderWidth: 4,
            pointRadius: 0, 
        },
        { 
            label: '',
            data: getGoalValues(null, getAxisValues('caloricLineChartXValues')),
            pointRadius: 0,
            borderWidth: 0,
        }]
    }
});
chart2 = new Chart(document.getElementById('weightLineChart').getContext('2d'), {
    type: 'line',
    data: {
        labels: getAxisValues('weightLineChartXValues'),
        datasets: [{
            label: 'Weight',
            fill: false, 
            lineTension: 0, 
            data: getAxisValues('weightLineChartYValues'),
            backgroundColor: '#1b1b1b', 
            borderColor: '#1b1b1b', 
            pointRadius: 5, 
            pointHoverRadius: 10, 
            pointBackgroundColor: '#1b1b1b', 
            pointBorderColor: '#1b1b1b', 
        },
        { 
            label: 'Target', 
            data: getGoalValues('weightGoalValue', getAxisValues('weightLineChartXValues')), 
            borderColor: '#f00', 
            backgroundColor: '#f00',
            borderWidth: 4, 
            pointRadius: 0, 
        },
        { 
            label: '',
            data: getGoalValues(null, getAxisValues('weightLineChartYValues')),
            pointRadius: 0,
            borderWidth: 0,
        }]
    }
});

function openProfileCard() {
    const profileCard = document.getElementsByClassName('profile-card');
    for (var i = 0; i < profileCard.length; i++) {
        profileCard[i].classList.add('active-profile-card');
    }
    const profileCardBG = document.getElementsByClassName('profile-card-background');
    for (var i = 0; i < profileCardBG.length; i++) {
        profileCardBG[i].classList.add('active-profile-card-background');
    }
}

function closeProfileCard() {
    const profileCard = document.getElementsByClassName('profile-card');
    for (var i = 0; i < profileCard.length; i++) {
        profileCard[i].classList.remove('active-profile-card');
    }
    const profileCardBG = document.getElementsByClassName('profile-card-background');
    for (var i = 0; i < profileCardBG.length; i++) {
        profileCardBG[i].classList.remove('active-profile-card-background');
    }
    document.getElementsByClassName('edit-profile-card')[0].style.display = 'None';
}

function editProfile() {
    document.getElementsByClassName('edit-profile-card')[0].style.display = 'flex';
}

function searchFriends() {
    const newFriends = document.querySelector('.new-friends');
    newFriends.classList.add('active-new-friends');
    
    const Friends = newFriends.childElementCount;
    if (Friends < 3) {
        newFriends.style.height = Friends * 160 + 20 + 'px';
        newFriends.style.overflow = 'visible';
    } else {
        newFriends.style.height = 3 * 160 + 20 + 'px';
        newFriends.style.overflow = 'scroll';
    }
}

function openMealCard(classification, date, action_type) {
    const mealCard = document.querySelector('.add-meal-card');
    mealCard.style.display = "block";

    const background = document.querySelector('.add-meal-card-background');
    background.style.zIndex = 4;
    background.style.opacity = 0.4;

    document.querySelector('.add-meal-card-title').innerHTML = action_type + ' ' + classification;
    document.querySelector('.meal-classification').value = classification;
    document.querySelector('.meal-date').value = date;
    document.querySelector('.action-type').value = action_type;
}

function closeMealCard() {
    const mealCard = document.querySelector('.add-meal-card');
    mealCard.style.display = "none";

    const background = document.querySelector('.add-meal-card-background');
    background.style.zIndex = -1;
    background.style.opacity = 0;
}

function closeAlert() {
    const alert = document.querySelector(".alert-warning");
    alert.classList.remove("alert");
}

function openMealDropdown() {
    document.getElementById("add-meal-card-dropdown").classList.toggle("show");
    if (document.getElementsByClassName("meal-dropbtn")[0].innerHTML == "Close dropdown") {
        document.getElementsByClassName("meal-dropbtn")[0].innerHTML = "Open dropdown";
    } else if (document.getElementsByClassName("meal-dropbtn")[0].innerHTML == "Open dropdown") {
        document.getElementsByClassName("meal-dropbtn")[0].innerHTML = "Close dropdown";
    } 
}
    
function filterMealsFunction() {
    const input = document.getElementById("add-meal-card-dropdown-input");
    const filter = input.value.toUpperCase();
    const div = document.getElementById("add-meal-card-dropdown");
    const a = div.getElementsByClassName("add-meal-card-option");
    for (let i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

function changeMealName(item, event) {
    document.getElementById("add-meal-card-dropdown").classList.remove("show");
    document.getElementsByClassName("meal-dropbtn")[0].innerHTML = item.innerHTML;
    document.getElementsByClassName("meal-dropbtn")[0].style.backgroundColor = "#04AA6D";
    
    document.getElementsByClassName("meal-dropbtn-input")[0].value = item.innerHTML;
    event.preventDefault();
}
