#Busco hacer una funcion generica que identifique cambios para commitear
    
def get_changes_to_commit(commit_data, data):
    
    filas_modificadas = []
    filas_eliminadas = []

    # Iterar sobre cada fila en los datos maestros
    for master_row in data:
        master_id = master_row['id']  # Suponiendo que 'id' es el identificador único de la fila

        # Buscar la fila correspondiente en los datos de commit
        commit_row = next((row for row in commit_data if row['id'] == master_id), None)

        # Si la fila no se encuentra en los datos de commit, se considera eliminada
        if commit_row is None:
            filas_eliminadas.append(master_row)

    # Iterar sobre cada fila en los datos de commit
    for commit_row in commit_data:
        commit_id = commit_row['id']

        # Buscar la fila correspondiente en los datos maestros
        master_row = next((row for row in data if row['id'] == commit_id), None)

        # Si la fila no se encuentra en los datos maestros, es una fila nueva o modificada
        if master_row is None:
            filas_modificadas.append(commit_row)
        else:
            # Comparar los valores de las columnas relevantes
            columnas_relevantes = ["node", "classe", "description", "level"]
            modificado = False
            for columna in columnas_relevantes:
                if master_row[columna] != commit_row[columna]:
                    modificado = True
                    break

            # Si se encontró una diferencia, agregar la fila a las modificadas
            if modificado:
                filas_modificadas.append(commit_row)
                #Falta el try catch de si todo salio correcto
    return[filas_modificadas, filas_eliminadas]
        