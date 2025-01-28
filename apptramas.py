import conn_db
import csv
import codecs
import zipfile
from flask import Flask, render_template, request, send_file

apptramas = Flask(__name__, template_folder='cont')
# Ruta para la página principal


def ejecutar_consulta_y_generar_archivo(conn, consulta, nombre_archivo, arch_descargar):
    cursor = conn.cursor()
    try:
        cursor.execute(consulta)
        rows = cursor.fetchall()
        with codecs.open(nombre_archivo, 'w', "ANSI") as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            for row in rows:
                writer.writerow(row)
        arch_descargar.append(nombre_archivo)
    except Exception as e:
        # Manejar errores
        print(f"Error executing query: {e}")
        return "Ha ocurrido un error. Por favor revisa los datos de tu formulario y la conexion a la base de datos."
    finally:
        cursor.close()


@apptramas.route('/', methods=['GET', 'POST'])
def main():

    if request.method == 'POST':
        arch_descargar = []
        # Obtener los valores de los combobox desde el formulario
        microred = request.form['microred']
        mes = request.form['mes']
        anio = request.form['anio']

        conn = conn_db.get_connection()
        if conn:

            dic_microredes = {
                "florencia de mora": "00005217",
                "huanchaco": "00005221",
                "la esperanza": "00005222",
                "laredo": "00005231",
                "moche": "00005234",
                "porvenir": "00005209",
                "salaverry": "00005239",
                "trujillo - metropolitano": "00005198",
                "victor larco": "00005242"
            }
            match microred:
                case microred if microred in dic_microredes:

                    cod_microred = dic_microredes[microred]

                    tabla = "T_CONSOLIDADO_NUEVA_TRAMA_HISMINSA"
                    condicion = f"Descripcion_MicroRed='{
                        microred}' AND Mes={mes}"

                    configuraciones_tramas = {
                        'trama1': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAA0'
                        },
                        'trama2': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAB1'
                        },
                        'trama3': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAB2'
                        },
                        'trama4': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAC1'
                        },
                        'trama5': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAC2'
                        },
                        'trama6': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAD1'
                        },
                        'trama7': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAD2'
                        },
                        'trama8': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAE0'
                        },
                        'trama9': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAF0'
                        },
                        'trama10': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAG0'
                        },
                        'trama11': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAH0'
                        },
                        'trama12': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAI0'
                        },
                        'trama13': {
                            'consulta': f"SELECT TOP 10 * FROM {tabla} WHERE {condicion}",
                            'sufijo': 'TAJ0'
                        }
                    }

                    for trama, config in configuraciones_tramas.items():
                        if request.form.get(f'chk{trama}') == 'on':
                            nombre_archivo = f"10000043_{cod_microred}_{
                                anio}_{mes}_{config['sufijo']}.txt"
                            ejecutar_consulta_y_generar_archivo(
                                conn, config['consulta'], nombre_archivo, arch_descargar)

            # ... (resto de tu código para crear el archivo ZIP y enviarlo)

            conn.close()
        microred = microred.replace(" ", "")
        # Crear un archivo ZIP
        with zipfile.ZipFile(f'tramas_mr_{microred}_{mes}_{anio}.zip', 'w') as zip:
            for archivo in arch_descargar:
                zip.write(archivo)
                # os.remove(archivo)

        # Enviar el archivo ZIP
        return send_file(f'tramas_mr_{microred}_{mes}_{anio}.zip', as_attachment=True)

    return render_template('index.html')


if __name__ == '__main__':
    apptramas.run(host="0.0.0.0", port=8000)
