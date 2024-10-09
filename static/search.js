$(document).ready(function() {
    let timeout; // Variable to hold the timeout ID

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

                // Loop through each result group in searchResults
                response.searchResults.forEach(function(resultGroup) {
                    if (resultGroup.results.length > 0) {
                        foundResults = true; // We found at least one result

                        // Loop through each result in the current group
                        resultGroup.results.forEach(function(item) {

                            let placeholder = "https://placehold.co/600x400?text=Hello\nWorld";
                            let canLoad = isImageLoaded(item.image);
                            let image = canLoad ? item.image : placeholder;
                            let card = `
                                <div class="col">
                                    <div class="card" style="width: 18rem;">
                                        <img src="${ image }" class="card-img-top img-thumbnail" alt="...">
                                        <div class="card-body">
                                            <h5 class="card-title">${item.name}</h5>
                                            <p class="card-text">${truncateByWords(item.content, 20)}</p> <!-- Limit to 1 sentence -->
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

                resultsContainer.show();  // Show results container
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);  // Log error to console
                $(`#${endpoint}-results`).append('<p class="text-danger">An error occurred while fetching results.</p>');
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
                fetchResults(query, endpoint);  // Call fetchResults if there is input
            }, 300); // 300 ms delay
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

function truncateByWords(text, maxWords) {
    const words = text.split(' ');
    if (words.length > maxWords) {
        return words.slice(0, maxWords).join(' ') + '...'; // Add ellipsis
    }
    return text;
}



function isImageLoaded(url) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = url;

        img.onload = () => resolve(true);  // Image loaded successfully
        img.onerror = () => reject(false);  // Failed to load the image
    });
}
