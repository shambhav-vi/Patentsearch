// Function to fetch patent details and update the search results
function fetchPatentDetails(patents) {
    // Array to store the updated patents with details
    let updatedPatents = [];
  
    // Function to fetch details for a single patent
    function fetchPatentDetail(index) {
      const patent = patents[index];
      const patentId = patent.patent_id;
  
      // Make a GET request to the server to fetch patent details
      fetch(`/patent_detail/${patentId}`)
        .then(response => response.json())
        .then(data => {
          // Add the fetched details to the patent object
          patent.details = data;
  
          // Push the updated patent to the array
          updatedPatents.push(patent);
  
          // Check if all patents have been processed
          if (updatedPatents.length === patents.length) {
            // All patent details have been fetched, update the search results
            updateSearchResults(updatedPatents);
          }
        })
        .catch(error => {
          console.log("Error fetching patent details:", error);
          // If there is an error fetching details, continue to the next patent
          if (index < patents.length - 1) {
            fetchPatentDetail(index + 1);
          } else {
            // All patent details have been fetched (even with errors), update the search results
            updateSearchResults(updatedPatents);
          }
        });
    }
  
    // Start fetching details for the first patent
    fetchPatentDetail(0);
  }
  
  // Function to update the search results with the fetched patent details
  function updateSearchResults(patents) {
    // Clear the existing search results
    const searchResultsContainer = document.getElementById("search-results");
    searchResultsContainer.innerHTML = "";
  
    // Iterate through the patents and create HTML elements for each patent
    patents.forEach(patent => {
      const title = patent.title;
      const abstract = patent.abstract;
      const details = patent.details;
      const patentUrl = patent.url;
  
      // Create HTML elements for the patent details
      const titleElement = document.createElement("h3");
      titleElement.textContent = title;
  
      const abstractElement = document.createElement("p");
      abstractElement.textContent = abstract;
  
      const detailsElement = document.createElement("p");
      detailsElement.textContent = `Author: ${details.author}\nInventor: ${details.inventor}`;
  
      const viewDetailsLink = document.createElement("a");
      viewDetailsLink.href = patentUrl;
      viewDetailsLink.textContent = "View Details";
  
      // Create a container element to hold the patent details
      const patentContainer = document.createElement("div");
      patentContainer.appendChild(titleElement);
      patentContainer.appendChild(abstractElement);
      patentContainer.appendChild(detailsElement);
      patentContainer.appendChild(viewDetailsLink);
  
      // Append the patent container to the search results container
      searchResultsContainer.appendChild(patentContainer);
    });
  }
  