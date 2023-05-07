const Graph = require("graphology")
const data = require("../data.json")

// https://github.com/rjbriody/linkedin-neo4j
// referencing this repository was incredibly helpful
// sigma.js doesn't have enough documentation yet, unfortunately

const button_container = document.getElementById("cluster-buttons")

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
  minNodeSize: 2,
  maxNodeSize: 9,
  minEdgeSize: 0.2,
  maxEdgeSize: 0.5
}).mouseProperties({
  minRatio: .75,
  maxRatio: 20
})

const selected_nodes = new Set()
let current_cluster = null

// returns a path of nodes
const bfs = (source, target) => {
  const visited = new Set()
  const queue = [[source]]

  while (queue.length > 0) {
    const path = queue.shift()
    const node = path[path.length - 1]

    if (node === target) return path

    graph.forEachNeighbor(node, neighbor => {
      if (visited.has(neighbor)) return

      const newPath = [...path, neighbor]
      visited.add(neighbor)
      queue.push(newPath)
    })
  }

  return []
}

const remove_selection = () => {
  renderer.iterNodes(node => {
    node.active = false
    node.hidden = false
  })

  renderer.draw()
}

const render = () => {
  const selected_nodes_len = selected_nodes.size
  if (selected_nodes_len == 0) {
    return remove_selection()
  }

  let path = selected_nodes_len == 1 ? 
    graph._nodes.get(Array.from(selected_nodes.values())[0]).in : bfs(...selected_nodes.keys())

  renderer.iterNodes(node => {

    if (selected_nodes_len == 1) {
      node.active = selected_nodes.has(node.id)
      node.hidden = false    
    } else if (selected_nodes_len == 2) {
      node.active = (path.includes(node.id) || selected_nodes.has(node.id))
      node.hidden = !(path.includes(node.id) || selected_nodes.has(node.id))
    }
  })

  renderer.draw()
}

const add_node_to_render = (event) => {
  const node_id = event.content[0]

  // prevent having 3+ players selected
  if (selected_nodes.size === 2 && !selected_nodes.has(node_id)) {
    selected_nodes.delete(selected_nodes.values().next().value)
  }

  // remove node if already selected, otherwise add
  const method = selected_nodes.has(node_id) ? "delete" : "add"
  selected_nodes[method](node_id)

  render()
}

const toggle_cluster = cluster => {
  selected_nodes.clear() // empty all selected players/path

  // toggle cluster
  if (cluster === current_cluster) {
    current_cluster = null
    return remove_selection()
  }

  current_cluster = cluster

  renderer.iterNodes(node => {
    // we always show these mfs
    node.active = false
    node.hidden = !(renderer.id_clusters[node.id] === cluster)
  })

  renderer.draw()
}

const players = {}

renderer.parseJson("../data.json", () => {
  const clusters = {}
  const id_clusters = {}
  renderer.clusters = clusters
  renderer.id_clusters = id_clusters
  
  renderer.iterNodes((node) => {
    const {cluster} = node.attr
    if (!clusters[cluster]) clusters[cluster] = []
    clusters[cluster].push(node.id)
    id_clusters[node.id] = cluster

    players[node.label.toLowerCase()] = node.id
  })

  // ensures cluster buttons are in order
  const cluster_numbers = Object.keys(clusters)
  cluster_numbers.sort((a, b) => a - b)

  cluster_numbers.forEach(cluster => {
    cluster = parseInt(cluster)

    const button = document.createElement("button")
    button.textContent = `Cluster #${cluster}`

    button.addEventListener("click", () => {
      toggle_cluster(cluster)
    })

    button_container.appendChild(button)
  })

  // embed list of clusters

  // click on a node
  renderer.bind("downnodes", add_node_to_render)
  renderer.draw()
})

const search_button = document.getElementById("search-player-button")
const search_bar_input = document.getElementById("player-search-input")

search_button.addEventListener("click", () => {
  const player_name = search_bar_input.value.toLowerCase()

  if (players[player_name]) add_node_to_render({"content": [players[player_name]]})

  console.log("could not find player")
})