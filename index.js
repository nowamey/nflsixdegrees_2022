const Graph = require("graphology")
const sigma = require("sigma")
const Sigma = sigma.Sigma



const container = document.getElementById("sigma-container")
container.style.height = "100vh"
container.style.width = "100vw"

const graph = new Graph()

graph.addNode("Derp", { x: 0, y: 10, size: 5, label: "Derp", color: "blue" })
graph.addNode("herp", { x: 10, y: 0, size: 3, label: "herp", color: "red" })
graph.addEdge("herp", "Derp")

const renderer = new Sigma(graph, container);

sigma.parsers.json('your_graph_data.json', {
    container: 'your_container_id',
    settings: {
      defaultNodeColor: '#ec5148',
      defaultEdgeColor: '#999',
      maxEdgeSize: 0.5,
      minEdgeSize: 0.1,
      edgeColor: 'default',
      edgeHoverColor: 'default',
      edgeLabelSize: 'proportional',
      edgeLabelThreshold: 0,
      defaultNodeSize: 1,
      minNodeSize: 0.5,
      maxNodeSize: 8,
      labelThreshold: 6,
      defaultLabelSize: 12,
      edgeHoverExtremities: true,
      zoomMax: 10,
      zoomMin: 0.000001,
      sideMargin: 0.2,
      defaultEdgeType: 'curve',
  
      // layout configuration options
      autoResize: true,
      hideEdgesOnMove: true,
      batchEdgesDrawing: true,
      enableEdgeHovering: true,
      enableHovering: true,
      enableCamera: true,
      minEdgeSize: 0.01,
      maxEdgeSize: 0.1,
      scalingMode: 'inside',
      edgeHoverColor: 'edge',
      edgeHoverSizeRatio: 1.5,
      defaultEdgeHoverColor: '#000',
      defaultNodeHoverColor: '#000',
      defaultNodeHoverSize: 4,
      defaultNodeBorderColor: '#fff',
      defaultNodeBorderSize: 0,
      edgeHoverExtremities: true,
  
      // force atlas 2 layout options
      layout: {
        // parameters for the ForceAtlas2 algorithm
        gravitationalConstant: -100,
        barnesHutOptimize: false,
        barnesHutTheta: 0.5,
        edgeWeightInfluence: 0,
        scalingRatio: 10,
        strongGravityMode: false,
        slowDown: 1
      }
    }
  }, function(s) {
    // start the ForceAtlas2 layout
    s.startForceAtlas2();
  });
  

