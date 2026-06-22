document.addEventListener('DOMContentLoaded', function () {
    // Mobile nav toggle
    var toggle = document.getElementById('navToggle');
    var menu = document.getElementById('navMenu');
    if (toggle && menu) {
        toggle.addEventListener('click', function () {
            menu.classList.toggle('open');
        });
    }

    // Vocabulary filter
    var filterBtns = document.querySelectorAll('.vocab-filter button');
    filterBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            filterBtns.forEach(function (b) { b.classList.remove('active'); });
            btn.classList.add('active');
            var category = btn.getAttribute('data-category');
            document.querySelectorAll('.vocab-item').forEach(function (item) {
                if (!category || item.getAttribute('data-category') === category) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // Exam timer
    var timerEl = document.getElementById('examTimer');
    if (timerEl) {
        var totalSeconds = parseInt(timerEl.getAttribute('data-minutes'), 10) * 60 || 3600;
        function updateTimer() {
            if (totalSeconds <= 0) {
                timerEl.textContent = '00:00';
                return;
            }
            totalSeconds--;
            var m = Math.floor(totalSeconds / 60);
            var s = totalSeconds % 60;
            timerEl.textContent = String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
        }
        setInterval(updateTimer, 1000);
    }
});
