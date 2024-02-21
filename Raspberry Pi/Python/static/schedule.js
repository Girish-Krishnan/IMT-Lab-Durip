        async function executeCommand(command, args) {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command, args }),
            });
            const result = await response.text();
            document.getElementById('result').textContent = result;
        }

        function addSchedule(event) {
            event.preventDefault();
            const form = event.target;
            const sensor = form.sensor.value;
            const start = form.start.value;
            const end = form.end.value;
            const state = form.state.value;
            const repeat = form.repeat.checked ? 'true' : '';
            const days = Array.from(form.days.selectedOptions).map(option => option.value).join(',');
            const endRepeat = form.endRepeat.value;
            const args = [sensor, start, end, state, repeat, days, endRepeat].filter(arg => arg !== '').join(',');
            executeCommand('add', args);
        }

        function removeSchedule(event) {
            event.preventDefault();
            const form = event.target;
            const sensor = form.sensor.value;
            const index = form.index.value;
            executeCommand('remove', `${sensor},${index}`);
        }

        async function viewSchedules() {
            const response = await fetch('/view_schedules', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            const schedules = await response.json();
            displaySchedules(schedules);
        }
    
        function displaySchedules(schedules) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = ''; // Clear previous content
            for (const [sensor, sensorSchedules] of Object.entries(schedules)) {
                const sensorDiv = document.createElement('div');
                sensorDiv.innerHTML = `<h3>${sensor}</h3>`;
                sensorSchedules.forEach(schedule => {
                    const scheduleDiv = document.createElement('div');
                    scheduleDiv.textContent = `Start: ${schedule.start}, End: ${schedule.end}, State: ${schedule.state}, Repeat: ${schedule.repeat}`;
                    sensorDiv.appendChild(scheduleDiv);
                });
                resultDiv.appendChild(sensorDiv);
            }
        }

        function overrideSensor(event) {
            event.preventDefault();
            const form = event.target;
            const sensor = form.sensor.value;
            const state = form.state.value;
            executeCommand('override', `${sensor},${state}`);
        }

        function removeOverride(event) {
            event.preventDefault();
            const sensor = event.target.sensor.value;
            executeCommand('remove_override', sensor);
        }