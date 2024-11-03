$(document).ready(
    function () {
        console.log(session_theme);
        setTheme(session_theme);

        $('#btn-light-bs-theme').click(
        function () {
            setTheme('light');
            setSession('light');
        }
        );

        $('#btn-dark-bs-theme').click(
        function () {
            setTheme('dark');
            setSession('dark');
        }
        );

        $('#btn-auto-bs-theme').click(
        function () {
            setTheme('auto');
            setSession('auto');
        }
        );
    }

);

function setTheme(theme){
    if (theme === 'auto') {
        let darkmode = window.matchMedia('(prefers-color-scheme: dark)').matches;
       if (darkmode) {
        $('html').attr('data-bs-theme', 'dark');
        $('#btn-auto-bs-theme').attr('aria-pressed', 'true');
        $('#btn-light-bs-theme').attr('aria-pressed', 'false');
        $('#btn-dark-bs-theme').attr('aria-pressed', 'false');
        console.log('click auto');
       }
        else{
            $('html').attr('data-bs-theme', 'light');
            $('#btn-auto-bs-theme').attr('aria-pressed', 'true');
            $('#btn-light-bs-theme').attr('aria-pressed', 'false');
            $('#btn-dark-bs-theme').attr('aria-pressed', 'false');
            console.log('click auto');
        }
    }
    else if (theme === 'light'){
        $('html').attr('data-bs-theme', 'light');
        $('#btn-auto-bs-theme').attr('aria-pressed', 'false');
        $('#btn-light-bs-theme').attr('aria-pressed', 'true');
        $('#btn-dark-bs-theme').attr('aria-pressed', 'false');
        console.log('click light');
    }
    else{
        $('html').attr('data-bs-theme', 'dark');
        $('#btn-auto-bs-theme').attr('aria-pressed', 'false');
        $('#btn-light-bs-theme').attr('aria-pressed', 'false');
        $('#btn-dark-bs-theme').attr('aria-pressed', 'true');
        console.log('click dark');
    }
}

function setSession(theme) {
    $.ajax({
        url: 'api/mode',
        method: 'GET',
        dataType: 'json',
        data: {mode : theme},
        error: function(xhr, status, error) {console.log(status, error);},
        success: function(response){
            console.log('sucess setting session mode');
        }
    });
}