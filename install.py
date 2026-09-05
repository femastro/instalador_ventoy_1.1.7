import os
import shutil
import sys
from pathlib import Path


def verificar_root():
    """Solicita permisos de superusuario si no se ejecuta como root."""
    if os.geteuid() != 0:
        print("Este programa requiere permisos de administrador.")
        print("Solicitando permisos con sudo...\n")
        try:
            os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
        except Exception as e:
            print(f"Error al elevar privilegios: {e}")
            sys.exit(1)


def dibuja_barra_progreso(
    actual, total, prefijo="Procesando", etiqueta="", longitud=30
):
    """Renderiza una barra de progreso dinámica en la terminal."""
    porcentaje = (actual / total) if total > 0 else 1.0
    lleno = int(longitud * porcentaje)
    barra = "█" * lleno + "-" * (longitud - lleno)

    # Imprime en la misma línea usando \r
    sys.stdout.write(
        f"\r{prefijo} [{barra}] {int(porcentaje * 100)}% {etiqueta}"
    )
    sys.stdout.flush()

    if actual >= total:
        print()  # Salto de línea al terminar


def copiar_archivo_con_progreso(origen: Path, destino: Path):
    """Copia un archivo mostrando la barra de progreso byte por byte."""
    if not origen.exists() or not origen.is_file():
        print(f"ERROR: No se encontró el archivo '{origen}'")
        return

    print(f"Copiando archivo: '{origen.name}'")
    destino.parent.mkdir(parents=True, exist_ok=True)

    tamanio_total = origen.stat().st_size
    bytes_copiados = 0
    bloque_bytes = 1024 * 64  # Bloques de 64 KB

    with open(origen, "rb") as f_origen, open(destino, "wb") as f_destino:
        while True:
            buffer = f_origen.read(bloque_bytes)
            if not buffer:
                break
            f_destino.write(buffer)
            bytes_copiados += len(buffer)

            mb_copiados = bytes_copiados / (1024 * 1024)
            mb_totales = tamanio_total / (1024 * 1024)

            dibuja_barra_progreso(
                bytes_copiados,
                tamanio_total,
                prefijo="Archivo",
                etiqueta=f"({mb_copiados:.1f}/{mb_totales:.1f} MB)",
            )

    shutil.copystat(origen, destino)
    os.chmod(destino, 0o755)  # Otorga permisos de ejecución si es necesario
    print("-> Archivo copiado exitosamente.\n")


def copiar_carpeta_con_progreso(origen: Path, destino: Path):
    """Copia una carpeta completa mostrando la barra de progreso archivo por archivo."""
    if not origen.exists() or not origen.is_dir():
        print(f"ERROR: No se encontró la carpeta '{origen}'")
        return

    # Mapea todos los archivos dentro de la carpeta origen
    todos_los_archivos = [p for p in origen.rglob("*") if p.is_file()]
    total_archivos = len(todos_los_archivos)

    if total_archivos == 0:
        print(f"La carpeta '{origen.name}' está vacía.")
        return

    print(
        f"Copiando carpeta: '{origen.name}' ({total_archivos} archivos en total)..."
    )

    for i, archivo in enumerate(todos_los_archivos, 1):
        # Replica la estructura interna dentro del destino
        ruta_relativa = archivo.relative_to(origen)
        destino_archivo = destino / ruta_relativa

        destino_archivo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(archivo, destino_archivo)

        dibuja_barra_progreso(
            i,
            total_archivos,
            prefijo="Carpeta",
            etiqueta=f"({i}/{total_archivos} archivos)",
        )

    print("-> Carpeta copiada exitosamente.\n")


def main():
    verificar_root()

    directorio_script = Path(__file__).resolve().parent

    # Configuración de rutas
    carpeta_origen = directorio_script / "ventoy-1.1.17"
    carpeta_destino = Path("/opt/ventoy")

    archivo_origen = directorio_script / "Ventoy.desktop"
    archivo_destino = Path("~/.local/share/applications/Ventoy.desktop")

    # Ejecución de la instalación con progreso
    copiar_carpeta_con_progreso(carpeta_origen, carpeta_destino)
    copiar_archivo_con_progreso(archivo_origen, archivo_destino)

    print("¡Proceso completado exitosamente!")


if __name__ == "__main__":
    main()