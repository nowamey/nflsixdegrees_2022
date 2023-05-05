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

renderer.parseJson("../data.json", renderer.draw)

