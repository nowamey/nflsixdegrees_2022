
function findConnection(playerData,teamsData,player1,player2){
    
}
async function mainEvent(){
    const playerData = await getData('/players_dict.json');
    const teamsData = await getData('/teams_map.json');
    const form = document.querySelector('#searchForm');
    const submit = document.querySelector('#startSearch');
    console.log(form);
    
    form.addEventListener('submit', (submitEvent) =>{
       submitEvent.preventDefault();
       console.log('Yeehaw');
    });
   
    
}
async function getData(path){
    fetch(path)
    .then(response => response.json())
    .then(data=> showInfo(data))
}
function showInfo(data){
    console.log(data);
}
document.addEventListener('DOMContentLoaded', async () => mainEvent());