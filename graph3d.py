
from conans.model import Generator

import json
import textwrap


class graph3d(Generator):

    # using the great: https://github.com/vasturiano/3d-force-graph for visualization

    html_content = textwrap.dedent("""
        <head>
            <style> body {{ margin: 0; }} </style>
        
            <script type="text/javascript" src="https://unpkg.com/three@0.143.0/build/three.js"></script>
            <script type="text/javascript" src="https://unpkg.com/three@0.143.0/examples/js/renderers/CSS2DRenderer.js"></script>
            <script type="text/javascript" src="https://unpkg.com/3d-force-graph@1.70.10/dist/3d-force-graph.min.js"></script>
        </head>

        <style>
            .node-label {{
                font-size: 14px;
                padding: 0px 0px;
                border-radius: 0px;
                background-color: rgba(0,0,0,0.0);
                font-family: monospace;
                user-select: none;
            }}
        </style>

        <body>
            <div id="3d-graph"></div>
        
            <script>
            // Random tree
            const gData = {{
                "directed": true,
                "multigraph": false,
                "graph": {{}},
                "nodes": {nodes},
                "links": {links}
                }};

                const Graph = ForceGraph3D({{
                extraRenderers: [new THREE.CSS2DRenderer()]
                }})
                (document.getElementById('3d-graph'))
                .graphData(gData)
                .linkDirectionalArrowLength(3.5)
                .linkDirectionalArrowRelPos(1)
                .linkCurvature(0.2)
                .linkWidth(0.5)
                .nodeLabel('id')
                    .showNavInfo(false)
                    .nodeAutoColorBy('group')
                    .nodeThreeObject(node => {{
                        const nodeEl = document.createElement('div');
                        nodeEl.textContent = node.id;
                        nodeEl.style.color = node.color;
                        nodeEl.className = 'node-label';
                        return new THREE.CSS2DObject(nodeEl);
                    }})
                    .nodeThreeObjectExtend(true)
                   ;
            </script>
        </body>        
    """)

    level = 0

    @property
    def filename(self):
        return "conan-graph3d.html"

    def get_build_requires_names(self):
        return [name for (name, _) in self.conanfile.build_requires]

    @property
    def content(self):

        links = []
        nodes = []

        def _get_deps(current):
            if str(current) not in [node.get("name") for node in nodes]:
                nodes.append(
                    {"name": f"{current}", "id": f"{current}", "group": f"{self.level}"})
                for dependency in current.dependencies.values():
                    links.append(
                        {"source": f"{current}", "target": f"{dependency}"})
                    _get_deps(dependency)
                self.level = self.level + 1

        for dep in self.conanfile.dependencies.filter({"direct": True, "build": False}).values():
            _get_deps(dep)

        ret = self.html_content.format(
            nodes=json.dumps(nodes), links=json.dumps(links))
        return ret
