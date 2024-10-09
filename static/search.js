
$(document).ready(function() {
        let timeout; // Variable to hold the timeout ID

        // Function to fetch search results
        function fetchResults(query, endpoint) {
            $.ajax({
                url: '/_api/search/${endpoint}',  // Flask API endpoint
                method: 'GET',   // Use GET request
                data: { q: query },  // Pass the query
                success: function(response) {
                    let resultsContainer = $(`#${endpoint}-results`);
                    resultsContainer.empty();  // Clear previous results

                    if (response.length > 0) {
                        // Loop through results and display
                        response.forEach(function(item) {
                            //resultsContainer.append(`<li>${item.name}</li>`);

                            //TODO
                            let card = ;

                        });
                        resultsContainer.show();  // Show results container if there are results
                    } else {
                        resultsContainer.append('<p class = "display-1 p-4 text-center">No results found<p>');
                        resultsContainer.show();  // Show results container even if empty
                    }
                }
            });
        }


        $('#search-all-input').on('input', function() {
            let endpoint = 'all'
            clearTimeout(timeout); // Clear the previous timeout

            let query = $(this).val();  // Get the current input value
            if (query) {
                // Set a new timeout to delay the search
                timeout = setTimeout(function() {
                    fetchResults(query, endpoint);  // Call fetchResults if there is input
                }, 300); // 300 ms delay
            } else {
                $('#${endpoint}-results').hide();  // Hide results if the input is empty
            }
        });

        $('#search-recipes-input').on('input', function() {
            let endpoint = 'recipes'
            clearTimeout(timeout); // Clear the previous timeout

            let query = $(this).val();  // Get the current input value
            if (query) {
                // Set a new timeout to delay the search
                timeout = setTimeout(function() {
                    fetchResults(query, endpoint);  // Call fetchResults if there is input
                }, 300); // 300 ms delay
            } else {
                $('#${endpoint}-results').hide();  // Hide results if the input is empty
            }
        });

    });

