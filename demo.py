<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Educational Content Scraper Results</title>
    <!-- Tailwind CSS CDN for easy styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles for Inter font and some base elements */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6; /* Light gray background */
            color: #374151; /* Dark gray text */
            line-height: 1.6;
        }

        /* Container for content */
        .container {
            max-width: 960px;
            margin: 2rem auto;
            padding: 1.5rem;
            background-color: #ffffff;
            border-radius: 0.75rem; /* Rounded corners */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Header styling */
        h1 {
            color: #1f2937; /* Darker text for headings */
            font-size: 2.25rem; /* text-4xl */
            font-weight: 700; /* font-bold */
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Section for individual scraped items */
        .scraped-item {
            background-color: #f9fafb; /* Lighter background for items */
            padding: 1.25rem;
            margin-bottom: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #e5e7eb; /* Light border */
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }

        .scraped-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
        }

        .scraped-item h2 {
            font-size: 1.5rem; /* text-2xl */
            font-weight: 600; /* font-semibold */
            color: #1d4ed8; /* Blue for titles */
            margin-bottom: 0.5rem;
        }

        .scraped-item p {
            font-size: 1rem; /* text-base */
            color: #4b5563; /* Medium gray for content */
        }

        .scraped-item .type-tag {
            display: inline-block;
            background-color: #dbeafe; /* Light blue */
            color: #1e40af; /* Darker blue */
            padding: 0.25rem 0.75rem;
            border-radius: 9999px; /* Full rounded */
            font-size: 0.75rem; /* text-xs */
            font-weight: 500;
            margin-bottom: 0.75rem;
        }

        /* Responsive design using Tailwind's utility classes */
        @media (max-width: 768px) {
            .container {
                margin: 1rem auto;
                padding: 1rem;
            }
            h1 {
                font-size: 1.75rem; /* text-3xl on small screens */
            }
            .scraped-item h2 {
                font-size: 1.25rem; /* text-xl on small screens */
            }
        }

        /* Loading indicator styles */
        .loading-spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-left-color: #3b82f6;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Educational Content Scraper</h1>
        <p class="text-center text-lg text-gray-600 mb-8">
            Enter a topic below to search for educational content.
        </p>

        <!-- Search Bar Section -->
        <div class="mb-8 flex flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-4">
            <input
                type="text"
                id="search-query-input"
                placeholder="e.g., Quantum Computing, History of Rome"
                class="flex-grow w-full md:w-3/5 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
            >
            <button
                id="search-button"
                class="w-full md:w-auto px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200 flex items-center justify-center space-x-2"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                </svg>
                <span>Search Content</span>
            </button>
        </div>

        <!-- Loading Indicator -->
        <div id="loading-indicator" class="hidden flex justify-center items-center py-4">
            <div class="loading-spinner"></div>
            <p class="ml-3 text-gray-600">Searching for educational content...</p>
        </div>

        <!-- Error Message -->
        <div id="error-message" class="hidden bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative mb-4" role="alert">
            <strong class="font-bold">Error!</strong>
            <span class="block sm:inline" id="error-text">Something went wrong. Please try again.</span>
        </div>

        <!-- Results Container -->
        <div id="results-container" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Search results will be dynamically inserted here -->
            <p class="text-center text-gray-500 col-span-full" id="initial-message">Your search results will appear here.</p>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const searchQueryInput = document.getElementById('search-query-input');
            const searchButton = document.getElementById('search-button');
            const resultsContainer = document.getElementById('results-container');
            const loadingIndicator = document.getElementById('loading-indicator');
            const errorMessage = document.getElementById('error-message');
            const errorText = document.getElementById('error-text');
            const initialMessage = document.getElementById('initial-message');

            /**
             * Displays an error message to the user.
             * @param {string} message - The error message to display.
             */
            function displayError(message) {
                errorText.textContent = message;
                errorMessage.classList.remove('hidden');
                errorMessage.classList.add('flex');
            }

            /**
             * Hides the error message.
             */
            function hideError() {
                errorMessage.classList.add('hidden');
                errorMessage.classList.remove('flex');
                errorText.textContent = '';
            }

            /**
             * Fetches educational content based on the search query.
             * This function simulates a call to a backend API that would
             * use the google_search tool to find information.
             */
            async function performSearch() {
                const query = searchQueryInput.value.trim();

                if (!query) {
                    displayError("Please enter a search query.");
                    return;
                }

                // Clear previous results and error messages
                resultsContainer.innerHTML = '';
                hideError();
                initialMessage.classList.add('hidden');

                // Show loading indicator
                loadingIndicator.classList.remove('hidden');

                try {
                    // Define the prompt for the LLM to perform a web search and format results
                    let prompt = Perform a web search for '${query}' focusing on educational content. Return the results as a JSON array of objects, where each object has 'title', 'snippet', and 'url'. Only include relevant educational content.;

                    let chatHistory = [];
                    chatHistory.push({ role: "user", parts: [{ text: prompt }] });

                    // Define the expected structured response schema
                    const payload = {
                        contents: chatHistory,
                        generationConfig: {
                            responseMimeType: "application/json",
                            responseSchema: {
                                type: "ARRAY",
                                items: {
                                    type: "OBJECT",
                                    properties: {
                                        "title": { "type": "STRING" },
                                        "snippet": { "type": "STRING" },
                                        "url": { "type": "STRING" }
                                    },
                                    "propertyOrdering": ["title", "snippet", "url"]
                                }
                            }
                        }
                    };

                    const apiKey = ""; // Canvas will automatically provide the API key
                    const apiUrl = https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey};

                    // Make the fetch call to the Gemini API
                    const response = await fetch(apiUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    const result = await response.json();

                    if (result.candidates && result.candidates.length > 0 &&
                        result.candidates[0].content && result.candidates[0].content.parts &&
                        result.candidates[0].content.parts.length > 0) {
                        const jsonString = result.candidates[0].content.parts[0].text;
                        const scrapedData = JSON.parse(jsonString);

                        if (scrapedData.length === 0) {
                            resultsContainer.innerHTML = '<p class="text-center text-gray-500 col-span-full">No educational content found for your query. Try a different search term.</p>';
                        } else {
                            // Populate the results container with fetched data
                            scrapedData.forEach(item => {
                                const itemDiv = document.createElement('div');
                                itemDiv.className = 'scraped-item';
                                itemDiv.innerHTML = `
                                    <span class="type-tag">Web Result</span>
                                    <h2><a href="${item.url}" class="text-blue-600 hover:underline" target="_blank">${item.title}</a></h2>
                                    <p>${item.snippet}</p>
                                `;
                                resultsContainer.appendChild(itemDiv);
                            });
                        }
                    } else {
                        displayError("Could not retrieve search results. The model response was unexpected.");
                    }

                } catch (error) {
                    console.error("Error during search:", error);
                    displayError("Failed to perform search. Please check your network connection or try again later.");
                } finally {
                    // Hide loading indicator
                    loadingIndicator.classList.add('hidden');
                }
            }

            // Event listener for the search button
            searchButton.addEventListener('click', performSearch);

            // Allow search on Enter key press in the input field
            searchQueryInput.addEventListener('keypress', (event) => {
                if (event.key === 'Enter') {
                    performSearch();
                }
            });
        });
    </script>
</body>
</html>