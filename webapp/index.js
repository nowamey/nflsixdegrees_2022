const Graph = require("graphology")
const data = require("../data.json")

// https://github.com/rjbriody/linkedin-neo4j
// referencing this repository was incredibly helpful
// sigma.js doesn't have enough documentation yet, unfortunately

const container = document.getElementById("sigma-container")
container.style.height = "100vh"
container.style.width = "100vw"

const graph = new Graph()
graph.import(data)

const renderer = sigma.init(container).drawingProperties({
  defaultLabelColor: "#fff",
  defaultLabelSize: 14,
  defaultHoverLabelBGColor: "#000",
  defaultLabelHoverColor: "#fff",
  labelThreshold: 8,
  defaultEdgeType: "curve",
  hoverFontStyle: "bold",
  fontStyle: "bold",
  activeFontStyle: "bold"
}).graphProperties({
  minNodeSize: 1,
  maxNodeSize: 7,
  minEdgeSize: 0.2,
  maxEdgeSize: 0.5
}).mouseProperties({
  minRatio: .75,
  maxRatio: 20
})

const render_direct_neighbors = event => {
  // retrieve edges from graph's nodes
  const node_edges = graph._nodes.get(event.content[0]).in
  renderer.iterNodes(node => {
    node.active = node.id === event.content[0]
    // im too lazy to work out the logic for this, so i just negated the good nodes LOL
    node.hidden = !(node_edges[node.id] !== undefined || node.id === event.content[0])
  })
  renderer.draw()
}

const remove_selection = () => {
  renderer.iterNodes(node => {
    node.active = false
    node.hidden = false
  })
  renderer.draw()
}

renderer.parseJson("../data.json", () => {
  console.log(renderer)
  console.log(graph)
  const clusters = {}
  const id_clusters = {}
  renderer.clusters = clusters
  renderer.id_clusters = id_clusters
  
  renderer.iterNodes((node) => {
    const {cluster} = node.attr
    if (!clusters[cluster]) clusters[cluster] = []
    clusters[cluster].push(node.id)
    id_clusters[node.id] = cluster
  })

  // click on a node
  renderer.bind("downnodes", render_direct_neighbors)
  renderer.draw()
})

// used to untoggle a selection
document.getElementById("remove-selection").addEventListener("click", remove_selection)






