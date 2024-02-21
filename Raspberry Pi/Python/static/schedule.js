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

        function viewSchedules() {
            fetch('/view_schedules').then(response => response.text()).then(text => {
                document.getElementById('result').textContent = text;
            }
            );
        }