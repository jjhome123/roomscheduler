
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.passed').forEach(cell => 
        cell.style.display='none');
    if (document.querySelector('#past_times')) {
        document.querySelector("#past_times").addEventListener("click", () => {
            slot = document.querySelectorAll(".passed");
            if (document.querySelector("#past_times").checked) {
                slot.forEach(element => {
                    element.style.display = 'table-cell';
                });
            } else {
                slot.forEach(element => {
                    element.style.display = 'none';
                });
            }  
        });
    }  

    if (document.querySelector('.delete_rv')) {
        document.querySelectorAll('.delete_rv').forEach(button => {
            button.onmouseover = button.style.cursor = 'pointer';
            button.addEventListener('click', () => {
                if (confirm('Do you want to delete this reservation?')) {
                    let room, date, start, end;
                    document.querySelectorAll(`.rv${button.dataset.rv}`).forEach(element => {
                        if (element.dataset.room) {
                            room = element.dataset.room;
                        }
                        else if (element.dataset.date) {
                            date = element.dataset.date;
                        }
                        else if (element.dataset.start) {
                            start = element.dataset.start;
                        }
                        else if (element.dataset.end) {
                            end = element.dataset.end;
                        }
                    })
                    csrftoken = button.parentElement.parentElement.firstElementChild.value; // This is the csrf token value
                    request = new Request(
                        `/user/${document.querySelector('#user').innerHTML}`,
                        {
                            method: "POST",
                            headers: {"X-CSRFToken": csrftoken},
                        }
                    );
                    fetch(request, {
                        body: JSON.stringify({
                            user: document.querySelector('#user').innerHTML,
                            room: room,
                            date: date,
                            start: start,
                            end: end,
                        })
                    })
                    setTimeout(() => {
                        location.reload();
                    }, 300)
                }                 
            })
        })
    }

    if (document.querySelector('#date_hidden')) {
        let i = 1;
        rooms = [];
        check = true;
        cells = document.querySelectorAll('td');
        start = document.querySelector('#start');
        end = document.querySelector('#end');
        date = document.querySelector('#date');
        date.value = document.querySelector('#date_hidden').value;
        localStorage.clear();
        while (check === true) {
            room = document.querySelector(`.room${i}`);
            if (room) {
                room = document.querySelectorAll(`.room${i}`);
                room.forEach(item => {
                    if (!item.className.includes('passed') && !item.className.includes('header') && !item.className.includes('booked')) {
                        item.addEventListener('click', () => {
                            // Changes select option to correct room
                            document.querySelector('#submit_rv').disabled = true;
                            document.getElementById('room_option').value = document.querySelector(`.${item.dataset.room}`).innerHTML;
                            // If no start value OR a start value AND end value is present
                            if ((!localStorage.getItem('start')) || item.dataset.room !== localStorage.getItem('start') || item.parentElement.firstElementChild.dataset.time === start.value) {
                                document.querySelectorAll('.open').forEach(cell => {
                                    cell.style.backgroundColor = 'transparent';
                                });
                                item.style.backgroundColor = 'blue';
                                localStorage.setItem('start', item.dataset.room);
                                start.value = item.parentElement.firstElementChild.dataset.time;
                                end.value = null;
                            }
                            // If a start value is present AND no end value is present
                            else if (item.dataset.room === localStorage.getItem('start')) {
                                let [s_hour, s_min] = start.value.split(":");
                                s_hour = parseInt(s_hour);
                                s_min = parseInt(s_min);
                                let [e_hour, e_min] = item.parentElement.firstElementChild.dataset.time.split(':');
                                e_hour = parseInt(e_hour);
                                e_min = parseInt(e_min);                  
                                if (e_hour < s_hour || (e_hour === s_hour && e_min < s_min)) {
                                    document.querySelectorAll('.open').forEach(cell => {
                                        cell.style.backgroundColor = 'transparent';
                                    });
                                    item.style.backgroundColor = 'blue';
                                    localStorage.setItem('start', item.dataset.room);
                                    start.value = item.parentElement.firstElementChild.dataset.time;
                                    end.value = null; 
                                }
                                else {
                                    document.querySelector('#submit_rv').disabled = false;
                                    end.value = item.parentElement.firstElementChild.dataset.time;
                                    item.style.backgroundColor = 'red';
                                    localStorage.clear();
                                }
                            }
                        });
                    }
                });
                i++;
            } else {
                check = false;
            }
        }
    }
})