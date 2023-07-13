from database.arangodb import connect_to_arangodb


def search_plaintiffs_by_name(db, name):
    query = """
    FOR plaintiff IN plaintiffs
        FILTER @name IN plaintiff.Plaintiff[*]
        RETURN { id: plaintiff.id }
    """
    bindVars={'name': name}
    result = db.AQLQuery(query,rawResults=True, bindVars=bindVars)
    plaintiffs = [doc['id'] for doc in result]
   
    return plaintiffs


def search_defendants_by_plaintiff_id(db, plaintiff_id):
    query = """
    FOR defendant IN defendant
        FILTER defendant.id == @plaintiff_id
        RETURN { Defendant: defendant.Defendant }
    """
    result = db.AQLQuery(query, bindVars={'plaintiff_id': plaintiff_id}, rawResults=True)
    defendants = [doc['Defendant'] for doc in result]
    return defendants



def build_graph(root_node, child_nodes):
    graph = {
        "nodes": [{"id": root_node, "type": "plaintiff"}],
        "links": []
    }

    unique_child_nodes = set(tuple(node) for node in child_nodes)  # Convert to set of tuples

    for node in unique_child_nodes:
        graph["nodes"].append({"id": node[0], "type": "defendant"})
        graph["links"].append({"source": root_node, "target": node[0]})

    return graph


def generate_graph_data(root_node_name):
    db = connect_to_arangodb()
    root_nodes = search_plaintiffs_by_name(db, root_node_name)
    child_nodes = []

    if root_nodes:
        for plaintiff_id in root_nodes:
            child_nodes.extend(search_defendants_by_plaintiff_id(db, plaintiff_id))

        graph = build_graph(root_node_name, child_nodes)
        return graph
    else:
        return None
