$(document).ready(
    function () {
        function setTheme(theme){
            if (theme === 'auto') {
                let darkmode = window.matchMedia('(prefers-color-scheme: dark)').matches;
               if (darkmode) {
                $('html').attr('data-bs-theme', 'dark')
               }
                else{
                    $('html').attr('data-bs-theme', 'light')
                }
            }
            else if (theme == 'light'){
                $('html').attr('data-bs-theme', 'light')
            }
            else{
                $('html').attr('data-bs-theme', 'dark')
            }
        }
        $('#btn-light-bs-theme').click(
        function () {
            setTheme('light');
            $(this).attr('aria-pressed', 'true');
            $('#btn-auto-bs-theme').attr('aria-pressed', 'false');
            $('#btn-dark-bs-theme').attr('aria-pressed', 'false');
            console.log('click light');
        }
        );

        $('#btn-dark-bs-theme').click(
        function () {
            setTheme('dark');
            $(this).attr('aria-pressed', 'true');
            $('#btn-light-bs-theme').attr('aria-pressed', 'false');
            $('#btn-auto-bs-theme').attr('aria-pressed', 'false');
            console.log('click dark');
        }
        );

        $('#btn-auto-bs-theme').click(
        function () {
            setTheme('auto');
            $(this).attr('aria-pressed', 'true');
            $('#btn-light-bs-theme').attr('aria-pressed', 'false');
            $('#btn-dark-bs-theme').attr('aria-pressed', 'false');
            console.log('click auto');
        }
        );

        setTheme('auto');
        console.log('ready')
    }

);
console.log('hello');