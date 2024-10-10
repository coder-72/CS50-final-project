$(document).ready(function() {
    let timeout; // Variable to hold the timeout ID
    let placeholderImage = $('#data').data('image-url')

    // Function to fetch search results
    function fetchAllResults(query, endpoint) {
        $.ajax({
            url: `/_api/search/${endpoint}`,  // Flask API endpoint
            method: 'GET',   // Use GET request
            data: { q: query },  // Pass the query
            success: function(response) {
                let resultsContainer = $(`#${endpoint}-results`);
                resultsContainer.empty();  // Clear previous results

                // Check if searchResults exists and is an array
                let foundResults = false;

                // Loop through each result group in searchResults
                response.searchResults.forEach(function(resultGroup) {
                    if (resultGroup.results.length > 0) {
                        foundResults = true; // We found at least one result

                        // Loop through each result in the current group
                        resultGroup.results.forEach(function(item) {

                            let text = item.content ? item.content : "No text";
                            let card = `
                                <div class="col mb-4">
                                    <div class="card" style="width: 18rem;">
                                        <div class="card-img-wrapper m-1 mx-auto">
                                            <img src="${ item.image }" class="card-img-top img-thumbnail" alt="item image" onerror="console.error('Image failed to load.'); this.onerror=null; this.src='${placeholderImage}';">
                                        </div>
                                        <div class="card-body">
                                            <h5 class="card-title">${item.name}</h5>
                                            <p class="card-text">${text}</p>
                                            <a href="${item.link}" class="btn btn-primary">View</a>
                                        </div>
                                    </div>
                                </div>
                            `;

                            resultsContainer.append(card);
                        });


                    }

                });

                // Show a message if no results were found
                if (!foundResults) {
                    resultsContainer.append('<p class="display-1 p-4 text-center">No results found</p>');
                }
                resultsContainer.html(resultsContainer.html().replace(/<b>/g, '').replace(/<\/b>/g, ''));
                resultsContainer.show();  // Show results container
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);  // Log error to console
                $(`#${endpoint}-results`).append('<p class="text-danger">An error occurred while fetching results.</p>');
            }
        });
    }

        // Function to fetch search results
    function fetchResults(query, endpoint) {
        $.ajax({
            url: `/_api/search/${endpoint}`,  // Flask API endpoint
            method: 'GET',   // Use GET request
            data: { q: query },  // Pass the query
            success: function(response) {
                let resultsContainer = $(`#${endpoint}-results`);
                resultsContainer.empty();  // Clear previous results

                // Check if searchResults exists and is an array
                let foundResults = false;


                if (response.code === 200 && response.results.length > 0) {
                    foundResults = true;

                    response.results.forEach(function(item) {

                        let text = item.content ? item.content : "No text";
                        let card = `
                            <div class="col mb-4">
                                <div class="card" style="width: 18rem;">
                                        <div class="card-img-wrapper m-1 mx-auto">
                                            <img src="${ item.image }" class="card-img-top img-thumbnail" alt="item image" onerror="console.error('Image failed to load.'); this.onerror=null; this.src='${placeholderImage}';">
                                        </div>
                                        <div class="card-body">
                                            <h5 class="card-title">${item.name}</h5>
                                            <p class="card-text">${text}</p>
                                            <a href="${item.link}" class="btn btn-primary">View</a>
                                        </div>
                                    </div>
                                </div>
                            `;

                            resultsContainer.append(card);
                        });


                }

                // Show a message if no results were found
                if (!foundResults) {
                    resultsContainer.append('<p class="display-1 p-4 text-center">No results found</p>');
                }
                resultsContainer.html(resultsContainer.html().replace(/<b>/g, '').replace(/<\/b>/g, ''));
                resultsContainer.show();  // Show results container
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);  // Log error to console
                $(`#${endpoint}-results`).append('<p class="display-1 p-4 text-danger text-center">An error occurred while fetching results.</p>');
            }
        });
    }

    $('#search-all-input').on('input', function() {
        let endpoint = 'all';
        clearTimeout(timeout); // Clear the previous timeout

        let query = $(this).val();  // Get the current input value
        if (query) {
            // Set a new timeout to delay the search
            timeout = setTimeout(function() {
                fetchAllResults(query, endpoint);  // Call fetchResults if there is input
            }, 500); // 300 ms delay
        } else {
            $(`#${endpoint}-results`).hide();  // Hide results if the input is empty
        }
    });

    $('#search-recipes-input').on('input', function() {
        let endpoint = 'recipes';
        clearTimeout(timeout); // Clear the previous timeout

        let query = $(this).val();  // Get the current input value
        if (query) {
            // Set a new timeout to delay the search
            timeout = setTimeout(function() {
                fetchResults(query, endpoint);  // Call fetchResults if there is input
            }, 300); // 300 ms delay
        } else {
            $(`#${endpoint}-results`).hide();  // Hide results if the input is empty
        }
    });



});



