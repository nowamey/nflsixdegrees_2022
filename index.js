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


renderer.setSetting("nodeReducer", (node, data) => {
    const state = {}
    const res = { ...data };
  
    if (state.hoveredNeighbors && !state.hoveredNeighbors.has(node) && state.hoveredNode !== node) {
      res.label = "";
      res.color = "#f6f6f6";
    }
  
    if (state.selectedNode === node) {
      res.highlighted = true;
    } else if (state.suggestions && !state.suggestions.has(node)) {
      res.label = "";
      res.color = "#f6f6f6";
    }

    console.log(res);
  
    return res;
  });

