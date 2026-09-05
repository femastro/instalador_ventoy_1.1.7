#!/bin/bash

clear

cp -r ventoy-1.1.17 /home/$USER/.ventoy-1.1.17

cp Ventoy.desktop /home/$USER/.local/share/applications

ln -s /home/$USER/.local/share/applications/Ventoy.desktop /home/$USER/Escritorio

# --- FUNCIÓN DE LA BARRA DE PROGRESO ---
barra_progreso() {
    local actual=$1
    local total=$2
    local ancho_barra=40  # Longitud en caracteres de la barra

    # Cánculo del porcentaje
    local porcentaje=$(( actual * 100 / total ))
    local completado=$(( actual * ancho_barra / total ))
    local restante=$(( ancho_barra - completado ))

    # Construcción de la barra
    local caracteres_completados=$(printf "%${completado}s" | tr ' ' '#')
    local caracteres_restantes=$(printf "%${restante}s" | tr ' ' '-')

    # \r regresa el cursor al inicio de la línea sin saltar de renglón
    printf "\rEspere : [%s%s] %3d%%" "$caracteres_completados" "$caracteres_restantes" "$porcentaje"
}

echo "==============================================================="
echo ""

# --- EJEMPLO DE USO ---
TOTAL_TAREAS=50

# Oculta el cursor de la terminal
tput civis

for ((i=1; i<=TOTAL_TAREAS; i++)); do
    # Simula una tarea pesada
    sleep 0.05
    
    # Llama a la función pasando el paso actual y el total
    barra_progreso $i $TOTAL_TAREAS
done

# Restaura el cursor y agrega un salto de línea final
tput cnorm

## FIN DE BARRA DE PROGRESO

echo ""
echo "==============================================================="
echo ""
echo "Proceso Terminado...."
