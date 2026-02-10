const fs = require('fs');

async function updateData() {
    const token = process.env.STARTGG_TOKEN;
    const endpoint = "https://api.start.gg/gql/alpha";

    // 1. Define the query (Must be defined BEFORE the fetch call)
    const query = `
    query CombinedTournaments($perPage: Int, $stateMO: String!, $stateKS: String!, $videogameId: ID!, $coordinates: String!, $radius: String!) {
      Missouri: tournaments(query: { perPage: $perPage, filter: { addrState: $stateMO, upcoming: true, videogameIds: [$videogameId] } }) {
        nodes {
          name
          id
          numAttendees
          city
          addrState
          startAt
          slug
          images { url type }
          events { name numEntrants }
        }
      }
      KansasCityKS: tournaments(query: { perPage: $perPage, filter: { addrState: $stateKS, upcoming: true, videogameIds: [$videogameId], location: { distanceFrom: $coordinates, distance: $radius } } }) {
        nodes {
          name
          id
          numAttendees
          city
          addrState
          startAt
          slug
          images { url type }
          events { name numEntrants }
        }
      }
    }
    `;

    // Variables
    const variables = {
        "perPage": 15,
        "stateMO": "MO",
        "stateKS": "KS",
        "videogameId": 1386,
        "coordinates": "39.0989150, -94.6071131",
        "radius": "50mi"
    };

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify({ query, variables })
        });

        const json = await response.json();

        if (json.errors) {
            console.error("API Error:", json.errors);
            process.exit(1);
        }

        // Timestamp
        const finalData = {
            updatedAt: new Date().toISOString(),
            data: json.data
        };

        fs.writeFileSync('./tournaments.json', JSON.stringify(finalData, null, 2));
        console.log("Successfully updated tournaments.json");

    } catch (error) {
        console.error("Fetch failed:", error);
        process.exit(1);
    }
}

updateData();