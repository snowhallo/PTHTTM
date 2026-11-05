import os
import json
import logging
from typing import Dict, Any, List, Optional

try:
    from neo4j import GraphDatabase, Driver
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

from .graph_engine import graph_engine

logger = logging.getLogger("Neo4jManager")

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'neo4j_config.json')

class Neo4jDiabetesManager:
    """
    Manages connection and Cypher queries to a Neo4j Graph Database.
    Provides automated synchronization of Long Chau diabetes dataset into Neo4j
    and seamlessly falls back to In-memory GraphEngine when Neo4j is offline.
    """
    def __init__(self, uri=None, user=None, password=None):
        self.load_config()
        if uri: self.uri = uri
        if user: self.user = user
        if password: self.password = password
        self.driver: Optional[Any] = None
        self.connected = False
        self.connect()

    def load_config(self):
        """Loads connection config from neo4j_config.json or environment."""
        self.uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.environ.get("NEO4J_USER", "neo4j")
        self.password = os.environ.get("NEO4J_PASSWORD", "password")

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    self.uri = cfg.get("uri", self.uri)
                    self.user = cfg.get("user", self.user)
                    self.password = cfg.get("password", self.password)
            except Exception as e:
                logger.warning(f"Error reading neo4j_config.json: {e}")

    def save_config(self):
        """Persists current connection config to neo4j_config.json."""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    "uri": self.uri,
                    "user": self.user,
                    "password": self.password
                }, f, indent=2)
        except Exception as e:
            logger.warning(f"Error writing neo4j_config.json: {e}")

    def update_credentials(self, uri: str, user: str, password: str) -> Dict[str, Any]:
        """Updates credentials, tries to connect, and saves if successful or returns status."""
        self.uri = uri.strip()
        self.user = user.strip()
        self.password = password.strip()
        
        success = self.connect()
        self.save_config()
        
        if success:
            # Also auto-sync data to the newly connected database
            sync_res = self.sync_data()
            return {
                "success": True,
                "connected": True,
                "message": f"Kết nối thành công tới Neo4j tại {self.uri}! Đã đồng bộ dữ liệu đồ thị tri thức.",
                "sync": sync_res
            }
        else:
            return {
                "success": False,
                "connected": False,
                "message": f"Không thể kết nối tới Neo4j tại {self.uri}. Vui lòng kiểm tra xem Database trong Neo4j Desktop đã bấm 'Start' chưa và mật khẩu đã chính xác chưa."
            }

    def connect(self) -> bool:
        if not NEO4J_AVAILABLE:
            logger.info("Neo4j Python driver not installed. Operating in Local Graph Engine mode.")
            self.connected = False
            return False
            
        try:
            if self.driver:
                try: self.driver.close()
                except Exception: pass

            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                connection_timeout=2.5
            )
            self.driver.verify_connectivity()
            self.connected = True
            logger.info(f"Connected to Neo4j successfully at {self.uri}")
            return True
        except Exception as e:
            logger.warning(f"Could not connect to Neo4j at {self.uri} ({e}). Falling back to Local Graph Engine.")
            self.connected = False
            self.driver = None
            return False

    def get_status(self) -> Dict[str, Any]:
        """Check status of Neo4j connection."""
        is_conn = False
        server_info = "Offline (Using Local In-Memory Graph)"
        node_count = 0
        rel_count = 0
        
        if self.driver:
            try:
                self.driver.verify_connectivity()
                is_conn = True
                self.connected = True
                with self.driver.session() as session:
                    n_res = session.run("MATCH (n) RETURN count(n) AS cnt").single()
                    r_res = session.run("MATCH ()-[r]->() RETURN count(r) AS cnt").single()
                    node_count = n_res["cnt"] if n_res else 0
                    rel_count = r_res["cnt"] if r_res else 0
                server_info = f"Online at {self.uri} ({node_count} nodes, {rel_count} relations)"
            except Exception as e:
                is_conn = False
                self.connected = False
                server_info = f"Connection error: {e}"
        else:
            # Try a quick reconnect attempt if not connected
            if self.connect():
                return self.get_status()
                
        return {
            "neo4j_available": NEO4J_AVAILABLE,
            "connected": is_conn,
            "uri": self.uri,
            "user": self.user,
            "server_info": server_info,
            "node_count": node_count if is_conn else graph_engine.graph.number_of_nodes(),
            "relation_count": rel_count if is_conn else graph_engine.graph.number_of_edges(),
            "mode": "Neo4j Server" if is_conn else "Local In-Memory Engine"
        }

    def sync_data(self, data_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Synchronizes JSON diabetes knowledge base to Neo4j instance using Cypher queries.
        Creates unique constraints and batch merges nodes & relationships.
        """
        if not self.connected or not self.driver:
            graph_engine.load_data()
            return {
                "success": True,
                "message": "Loaded data into Local In-Memory Engine (Neo4j Server offline)",
                "nodes": graph_engine.graph.number_of_nodes(),
                "relations": graph_engine.graph.number_of_edges()
            }

        if data_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, 'longchau_diabetes_data.json')
            
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        try:
            with self.driver.session() as session:
                # 1. Create constraint
                try:
                    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE")
                except Exception as ce:
                    logger.info(f"Constraint notice: {ce}")
                
                # 2. Insert Nodes
                for node in data.get("nodes", []):
                    node_type = node.get("type", "Entity")
                    cypher = f"""
                    MERGE (n:Entity:{node_type} {{id: $id}})
                    SET n.label = $label,
                        n.type = $type,
                        n.summary = $summary,
                        n.active_ingredient = $active_ingredient,
                        n.manufacturer = $manufacturer,
                        n.dosage = $dosage,
                        n.price_ref = $price_ref,
                        n.longchau_url = $longchau_url,
                        n.diagnostic_criteria = $diagnostic_criteria
                    """
                    session.run(
                        cypher,
                        id=node.get("id"),
                        label=node.get("label", ""),
                        type=node_type,
                        summary=node.get("summary", ""),
                        active_ingredient=node.get("active_ingredient", ""),
                        manufacturer=node.get("manufacturer", ""),
                        dosage=node.get("dosage", ""),
                        price_ref=node.get("price_ref", ""),
                        longchau_url=node.get("longchau_url", ""),
                        diagnostic_criteria=node.get("diagnostic_criteria", "")
                    )
                
                # 3. Insert Edges
                for edge in data.get("edges", []):
                    rel_type = edge.get("label", "RELATED_TO").replace("-", "_").replace(" ", "_").upper()
                    cypher = f"""
                    MATCH (source:Entity {{id: $from_id}})
                    MATCH (target:Entity {{id: $to_id}})
                    MERGE (source)-[r:{rel_type}]->(target)
                    SET r.title = $title
                    """
                    session.run(
                        cypher,
                        from_id=edge.get("from"),
                        to_id=edge.get("to"),
                        title=edge.get("title", "")
                    )

            logger.info("Successfully synced all nodes and relationships to Neo4j!")
            return {
                "success": True,
                "message": f"Đồng bộ thành công {len(data.get('nodes', []))} nodes và {len(data.get('edges', []))} relationships vào Neo4j Database."
            }
        except Exception as e:
            logger.error(f"Error syncing to Neo4j: {e}")
            return {"success": False, "error": str(e)}

    def query_cypher(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Executes a custom Cypher query if Neo4j is available."""
        if not self.connected or not self.driver:
            return []
        try:
            with self.driver.session() as session:
                result = session.run(query, params or {})
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Cypher query error: {e}")
            return []

    def get_vis_graph(self) -> Dict[str, Any]:
        """Returns graph data for Vis.js representation."""
        return graph_engine.get_all_graph_data()

# Global singleton instance
neo4j_manager = Neo4jDiabetesManager()
