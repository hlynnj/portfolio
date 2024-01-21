# Web Lab Final Project

## Link: https://catto-cafe.herokuapp.com/
The website features a cat cafe where users can interact with the cats by clicking on them. Users can also load and save their data.

The website is primarily made up of three large components:
1. Front End: building webpage through ReactJS
2. Socket calls: updating webpage based on updating game logic
3. DB communication: via API calls

## Navigating the Files
Skeleton structure of the website was created using ReactJS  
ReactJS modules are located in /client/src/components/modules  
ReactJS pages are located in /client/src/components/pages  

Updating the cat cafe (running the "game" logic) happens in /server/logic.js  
The logic files sends socket calls to front end in /server/server-socket.js  
The cat cafe is updated on the screen through /client/src/canvasManager.js  

Loading/saving user data is done through MongoDB.  
MongoDB Schemas are located in /server/models  
MongoDB get + push requests are made in /server/api.js  
