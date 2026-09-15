"""
Programa principal (Modulo A del enunciado).

Por ahora este programa solo hace la parte de Huffman (Modulo B): lee un
archivo de texto, lo codifica con Huffman, lo decodifica, y se fija si
el resultado es igual al texto original.

Mas adelante, entre "codificar" y "decodificar" vamos a ir agregando los
pasos que todavia faltan (codificacion de canal, modulacion, el canal
con ruido, demodulacion...), a medida que los veamos en clase. Por ahora
no hace falta pensar en eso.
"""

import cli
import source
import report


def main():
    args, text = cli.setup()

    if args.dry_run:
        cli.print_dry_run_notice()
        return

    # Codificamos el texto con Huffman
    counts, probabilities = source.analyze_text(args.input)
    code = source.generate_huffman_code(probabilities)
    bits = source.encode_text(text, code)

    # (Aca, mas adelante, van a ir los pasos de codificacion de canal,
    # modulacion, canal y demodulacion)

    # Decodificamos de vuelta y guardamos el resultado
    received_text = source.decode_bits(bits, code)
    output_path = cli.build_output_path(args)
    source.save_text(received_text, output_path)

    # Armamos el Informe del Modulo B (tablas y ejemplos) en un .md
    report_path = cli.build_report_path(args)
    report.generate_module_b_report(text, counts, probabilities, code, bits, received_text, report_path)

    cli.print_results(output_path, report_path, received_text, text)


if __name__ == "__main__":
    main()
