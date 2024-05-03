mechanics = {
    "id": list(range(1, 44)),  # IDs desde 1 hasta 43
    "node": [
        "Vehicle",  # Raíz
        "Engine System", "Transmission System", "Braking System", "Electrical System", "Cooling System",
        "Suspension System", "Steering System", "Wheel Assembly", "Air Conditioning System",
        "Engine Block", "Cylinder Head", "Crankshaft", "Piston", "Camshaft",
        "Gearbox", "Clutch", "Flywheel", "Drive Shaft",
        "Disc Brakes", "Drum Brakes", "ABS Module",
        "Battery", "Alternator", "Starter Motor", "Wiring Harness",
        "Radiator", "Water Pump", "Thermostat", "Coolant Hose",
        "Shock Absorbers", "Springs", "Control Arms",
        "Steering Wheel", "Power Steering Pump", "Steering Rack",
        "Tires", "Wheels", "Hubs",
        "AC Compressor", "AC Condenser", "Evaporator", "Refrigerant Lines"
    ],
    "classe": [
        "",  # Raíz
        "Vehicle", "Vehicle", "Vehicle", "Vehicle", "Vehicle",
        "Vehicle", "Vehicle", "Vehicle", "Vehicle",
        "Engine System", "Engine System", "Engine System", "Engine System", "Engine System",
        "Transmission System", "Transmission System", "Transmission System", "Transmission System",
        "Braking System", "Braking System", "Braking System",
        "Electrical System", "Electrical System", "Electrical System", "Electrical System",
        "Cooling System", "Cooling System", "Cooling System", "Cooling System",
        "Suspension System", "Suspension System", "Suspension System",
        "Steering System", "Steering System", "Steering System",
        "Wheel Assembly", "Wheel Assembly", "Wheel Assembly",
        "Air Conditioning System", "Air Conditioning System", "Air Conditioning System", "Air Conditioning System"
    ],
    "description": [
        "The entire vehicle system",
        "System managing engine operations", "System for power transmission", "System handling vehicle braking", "System managing vehicle's electrical components", "System for engine cooling",
        "System handling the vehicle's suspension", "System for steering control", "Assembly of wheels", "System for vehicle climate control",
        "Main part of the engine", "Top part of the engine housing valves", "Converts reciprocating motion to rotational force", "Engine component for combustion", "Shaft to open and close valves",
        "Contains the gears of the vehicle", "Connects and disconnects the engine power", "Stores rotational energy", "Transfers power from gearbox to wheels",
        "Brakes using disc mechanism", "Brakes using drum mechanism", "Anti-lock braking system module",
        "Stores electrical energy", "Generates electricity for charging", "Motor for starting the engine", "Handles vehicle's electrical wiring",
        "Helps cool the engine", "Pumps coolant through engine", "Controls coolant flow", "Hoses carrying the coolant",
        "Dampens the impact of road irregularities", "Coils or leafs providing suspension", "Arms connecting wheels and vehicle frame",
        "Wheel that steers the vehicle", "Pump assisting in steering effort", "Gear assembly for steering",
        "Contact point between vehicle and road", "Circular components holding the tires", "Central part of the wheel",
        "Controls the flow and pressure of the AC system", "Condenses refrigerant from gaseous to liquid", "Part of the AC system where heat absorption occurs", "Carry refrigerant between AC components"
    ],
    "level": [
        1,  # Raíz
        2, 2, 2, 2, 2,
        2, 2, 2, 2,
        3, 3, 3, 3, 3,
        3, 3, 3, 3,
        3, 3, 3,
        3, 3, 3, 3,
        3, 3, 3, 3,
        3, 3, 3,
        3, 3, 3,
        3, 3, 3,
        3, 3, 3, 3
    ],
    "is_endpoint": [
        False,
        False, False, False, False, False,
        False, False, False, False,
        True, True, True, True, True,
        True, True, True, True,
        True, True, True,
        True, True, True, True,
        True, True, True, True,
        True, True, True,
        True, True, True,
        True, True, True,
        True, True, True, True
    ]
}

def report():
    # Revisar que todas las listas tengan el mismo tamaño
    lengths = {key: len(value) for key, value in mechanics.items()}
    if len(set(lengths.values())) == 1:
        print("Todas las listas tienen el mismo largo.")
    else:
        print("Los largos de las listas varían:", lengths)
    # Verificar nodo raíz único y referencias de padres
    root_nodes = [node for node, parent in zip(mechanics['node'], mechanics['classe']) if not parent]

    if len(root_nodes) > 1:
        print(f"Error: Hay múltiples nodos raíz: {root_nodes}")
    elif len(root_nodes) == 0:
        print("Error: No hay ningún nodo raíz definido.")
    else:
        print(f"Nodo raíz único encontrado: {root_nodes[0]}")

    # Verificar que todos los nodos padres existen
    parent_nodes = set(mechanics['classe']) - {''}  # Elimina la cadena vacía que representa la raíz
    node_set = set(mechanics['node'])

    undefined_parents = parent_nodes - node_set
    if undefined_parents:
        print(f"Error: Hay nodos padres referenciados que no existen como nodos: {undefined_parents}")
    else:
        print("Todas las referencias de padres son correctas.")
