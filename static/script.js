// -----------------------------
// Initialize Map
// -----------------------------

var map = L.map('map').setView([22.5726, 88.3639], 12);

// OpenStreetMap Tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {

    attribution: '&copy; OpenStreetMap contributors'

}).addTo(map);


// Route polyline
let routeLine = null;


// -----------------------------
// Find Route
// -----------------------------

async function findRoute() {

    const start = document.getElementById("start").value;

    const end = document.getElementById("end").value;


    if(start === "" || end === "")
    {
        alert("Please enter both locations.");
        return;
    }


    try{

        const response = await fetch("/route",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                start:start,

                end:end

            })

        });


        const data = await response.json();


        if(!data.success)
        {
            alert(data.message);
            return;
        }


        // Remove previous route
        if(routeLine)
        {
            map.removeLayer(routeLine);
        }


        // Draw route
        routeLine = L.polyline(data.route,{

            color:"blue",

            weight:6,

            opacity:0.8

        }).addTo(map);


        // Zoom to route
        map.fitBounds(routeLine.getBounds());


        // Show distance
        document.getElementById("result").innerHTML =

            "Distance : " + data.distance + " km";



    }

    catch(error){

        console.log(error);

        alert("Server Error");

    }

}   
