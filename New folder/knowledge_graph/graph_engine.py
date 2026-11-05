import json
import os
import networkx as nx

class DiabetesGraphEngine:
    """
    In-memory Knowledge Graph Engine using NetworkX and JSON dataset.
    Provides fast lookup, neighborhood expansion, shortest paths, and Vis.js serialization.
    """
    def __init__(self, data_path=None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, 'longchau_diabetes_data.json')
        self.data_path = data_path
        self.graph = nx.DiGraph()
        self.raw_data = {"nodes": [], "edges": [], "node_types": [], "graph_metadata": {}}
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Knowledge graph data file not found: {self.data_path}")
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)
            
        self.graph.clear()
        
        # Add nodes
        for node in self.raw_data.get("nodes", []):
            self.graph.add_node(
                node["id"],
                label=node.get("label", ""),
                type=node.get("type", "General"),
                summary=node.get("summary", ""),
                **{k: v for k, v in node.items() if k not in ["id", "label", "type", "summary"]}
            )
            
        # Add edges
        for edge in self.raw_data.get("edges", []):
            self.graph.add_edge(
                edge["from"],
                edge["to"],
                label=edge.get("label", "RELATED_TO"),
                title=edge.get("title", "")
            )

    def get_all_graph_data(self):
        """Returns nodes and edges formatted for Vis.js Network rendering."""
        color_map = {
            "Disease": {"background": "#0284c7", "border": "#0369a1", "highlight": {"background": "#38bdf8", "border": "#0284c7"}},
            "Symptom": {"background": "#ea580c", "border": "#c2410c", "highlight": {"background": "#fb923c", "border": "#ea580c"}},
            "RiskFactor": {"background": "#dc2626", "border": "#b91c1c", "highlight": {"background": "#f87171", "border": "#dc2626"}},
            "Complication": {"background": "#7c3aed", "border": "#6d28d9", "highlight": {"background": "#a78bfa", "border": "#7c3aed"}},
            "DrugClass": {"background": "#0d9488", "border": "#0f766e", "highlight": {"background": "#2dd4bf", "border": "#0d9488"}},
            "Medicine": {"background": "#059669", "border": "#047857", "highlight": {"background": "#34d399", "border": "#059669"}},
            "DietLifestyle": {"background": "#d97706", "border": "#b45309", "highlight": {"background": "#fbbf24", "border": "#d97706"}}
        }

        vis_nodes = []
        for node_id, data in self.graph.nodes(data=True):
            node_type = data.get("type", "General")
            c = color_map.get(node_type, {"background": "#64748b", "border": "#475569", "highlight": {"background": "#94a3b8", "border": "#64748b"}})
            
            # Format tooltip
            tooltip = f"<b>{data.get('label')}</b> ({node_type})<br>{data.get('summary', '')}"
            if "active_ingredient" in data:
                tooltip += f"<br><b>Hoạt chất:</b> {data.get('active_ingredient')}"
            if "price_ref" in data:
                tooltip += f"<br><b>Giá Long Châu:</b> {data.get('price_ref')}"

            vis_nodes.append({
                "id": node_id,
                "label": data.get("label"),
                "group": node_type,
                "title": tooltip,
                "color": c,
                "shape": "dot" if node_type != "Disease" else "diamond",
                "size": 28 if node_type == "Disease" else (22 if node_type in ["Medicine", "DrugClass"] else 18),
                "font": {"color": "#ffffff", "face": "Inter, system-ui, sans-serif", "size": 13, "bold": True if node_type == "Disease" else False},
                "data": data
            })

        vis_edges = []
        for u, v, data in self.graph.edges(data=True):
            vis_edges.append({
                "from": u,
                "to": v,
                "label": data.get("label", ""),
                "title": data.get("title", ""),
                "arrows": "to",
                "color": {"color": "#94a3b8", "highlight": "#0284c7", "opacity": 0.8},
                "font": {"size": 10, "align": "middle", "color": "#64748b", "strokeWidth": 2, "strokeColor": "#ffffff"}
            })

        return {
            "metadata": self.raw_data.get("graph_metadata", {}),
            "node_types": self.raw_data.get("node_types", []),
            "nodes": vis_nodes,
            "edges": vis_edges,
            "stats": {
                "total_nodes": self.graph.number_of_nodes(),
                "total_edges": self.graph.number_of_edges(),
                "density": round(nx.density(self.graph), 4)
            }
        }

    def search_entities(self, query):
        """Search nodes by label, summary, or active ingredient."""
        query = query.lower().strip()
        results = []
        if not query:
            return results
            
        for node_id, data in self.graph.nodes(data=True):
            label = data.get("label", "").lower()
            summary = data.get("summary", "").lower()
            ingredient = data.get("active_ingredient", "").lower()
            node_type = data.get("type", "").lower()
            
            score = 0
            if query == label:
                score += 100
            elif query in label:
                score += 50
            if query in ingredient:
                score += 40
            if query in summary:
                score += 20
            if query in node_type:
                score += 10
                
            if score > 0:
                results.append({
                    "id": node_id,
                    "score": score,
                    "label": data.get("label"),
                    "type": data.get("type"),
                    "data": data
                })
                
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def get_node_details_and_neighbors(self, node_id):
        """Get full details of a node and its incoming/outgoing relations."""
        if node_id not in self.graph:
            return None
            
        node_data = dict(self.graph.nodes[node_id])
        node_data["id"] = node_id
        
        outgoing = []
        for _, target, edge_data in self.graph.out_edges(node_id, data=True):
            target_data = dict(self.graph.nodes[target])
            outgoing.append({
                "target_id": target,
                "target_label": target_data.get("label"),
                "target_type": target_data.get("type"),
                "relation": edge_data.get("label"),
                "title": edge_data.get("title")
            })
            
        incoming = []
        for source, _, edge_data in self.graph.in_edges(node_id, data=True):
            source_data = dict(self.graph.nodes[source])
            incoming.append({
                "source_id": source,
                "source_label": source_data.get("label"),
                "source_type": source_data.get("type"),
                "relation": edge_data.get("label"),
                "title": edge_data.get("title")
            })
            
        return {
            "node": node_data,
            "outgoing": outgoing,
            "incoming": incoming
        }

    def query_subgraph_by_keywords(self, keywords):
        """Find subgraphs matching a set of medical keywords (symptoms, drugs, etc.)."""
        matched_nodes = set()
        for kw in keywords:
            search_res = self.search_entities(kw)
            for item in search_res[:3]:
                matched_nodes.add(item["id"])
                
        # Include 1-hop neighbors
        extended_nodes = set(matched_nodes)
        for n in matched_nodes:
            extended_nodes.update(self.graph.neighbors(n))
            extended_nodes.update(self.graph.predecessors(n))
            
        sub_g = self.graph.subgraph(extended_nodes)
        
        sub_nodes = []
        for n, data in sub_g.nodes(data=True):
            sub_nodes.append({"id": n, "label": data.get("label"), "type": data.get("type"), "data": data})
            
        sub_edges = []
        for u, v, data in sub_g.edges(data=True):
            sub_edges.append({"from": u, "to": v, "label": data.get("label"), "title": data.get("title")})
            
        return {
            "matched_seed_ids": list(matched_nodes),
            "nodes": sub_nodes,
            "edges": sub_edges
        }

# Global singleton instance
graph_engine = DiabetesGraphEngine()
