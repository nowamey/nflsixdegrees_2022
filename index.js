const Graph = require("graphology")
const { Sigma } = require("sigma")
const data = require("./data.json")

const container = document.getElementById("sigma-container")
container.style.height = "100vh"
container.style.width = "100vw"

const graph = new Graph()
graph.import(data)

const renderer = new Sigma(graph, container, {
  minEdgeSize: 0.2,
  maxEdgeSize: 0.5
});

// state modifiers

// handle searching
const inputs = ["player-a", "player-b"]
inputs.forEach(input_id => {
  document.getElementById(input_id).addEventListener("input", (event) => {
    console.log(event.target.value)
  })
})


