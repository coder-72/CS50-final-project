$(document).ready(
function(){
    let timeout;

    function fetchResults(query){
       $('#results').empty();
       let html = "";
       let data = {};
       if (query === ""){
        data = {};
       }
       else{ data = {q : query};}
           $.ajax({
                url: 'api/search',
                method: 'GET',
                dataType: 'json',
                data: data,
                error: function(xhr, status, error) {console.log(status, error); $('#results').html('<h2 class="section-heading text-center">${error}</h2>');},
                success: function(response){

                let results = response.results;
                if (results.length != 0){
                    results.forEach(function (post) {
                        console.log(`result ${post.id} processed`)
                        html += `
                        <div class="col-md-4 d-flex align-items-stretch">
                            <div class="card mb-4 shadow-sm w-100">
                                <img src="${post.image}" class="card-img-top" alt="Post ${post.id}">
                                <div class="card-body d-flex flex-column h-100">
                                    <h5 class="card-title">${post.title}</h5>
                                    <p class="card-text">${post.subtitle}</p>
                                    <p class="card-date text-muted">${formatDate(post.date)}</p>
                                    <div class="mt-auto">
                                        <a href="/post/${post.id}" class="btn btn-primary p-2">Read More</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        `;


                    });
                $('#results').html(html);
                }
                else{
                  let html = '<h2 class="section-heading text-center">No results!</h2>';
                  $('#results').html(html);
                }


                }


           });
    }

    $('#search').on('input', function(){
        clearTimeout(timeout);
        timeout = setTimeout(function() {
                    fetchResults($('#search').val());
                }, 300);
    });

    $('#search').on('keydown', function(event) {
        // Check if the Enter key (key code 13) is pressed
        if (event.key === 'Enter') {
            window.location.assign(`/search?q=${$(this).val()}`);
        }
    });

    fetchResults($('#search').val())
});

function searchBtn(){
    window.location.assign(`/search?q=${$('#search').val()}`);
}





function formatDate(dateString) {
    // Parse the input date string
    const date = new Date(dateString);

    // Check if the date is valid
    if (isNaN(date)) {
        throw new Error('Invalid date format');
    }

    // Create options for the desired format
    const options = {
        weekday: 'short', // 'Sat'
        day: '2-digit',   // '13'
        month: 'short',   // 'Oct'
        year: 'numeric'   // '2024'
    };

    // Format the date using Intl.DateTimeFormat
    return new Intl.DateTimeFormat('en-US', options).format(date);
}