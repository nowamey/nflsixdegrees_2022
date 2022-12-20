async function mainEvent(){
    const playerData = await getData('/players_dict.json');
    const teamsData = await getData('/teams_map.json');

    
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