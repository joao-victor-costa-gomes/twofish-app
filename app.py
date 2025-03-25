from flask import Flask, render_template, request
from algorithm.twofish import encrypt, decrypt

app = Flask(__name__)

# Converter texto para hexadecimal
def texto_para_hex(texto):
    hexa = texto.encode('utf-8').hex()
    return hexa

# Converter hexadecimal para texto
def hex_para_texto(hex_str):
    return bytes.fromhex(hex_str).decode('utf-8')

def criptografar_texto(chave, mensagem):
    chave_hexa = texto_para_hex(chave)
    chave_completa = chave_hexa.zfill(32)

    mensagem_hexa = texto_para_hex(mensagem)
    mensagem_completa = mensagem_hexa.zfill(32)

    mensagem_criptografada = encrypt(mensagem_completa, chave_completa)

    return mensagem_criptografada

def descriptografar_texto(chave, mensagem_criptografada):
    chave_hexa = texto_para_hex(chave)
    chave_completa = chave_hexa.zfill(32)

    mensagem_descriptografada_hexa = decrypt(mensagem_criptografada, chave_completa)

    mensagem_descriptografada = hex_para_texto(mensagem_descriptografada_hexa)

    return mensagem_descriptografada

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado_cripto = ""
    resultado_descripto = ""

    if request.method == 'POST':
        acao = request.form.get('acao')
        chave = request.form.get('chave')
        texto = request.form.get('texto')

        if len(chave) > 16:
            erro = "Erro: a chave não pode ter mais de 16 caracteres."
            if acao == 'criptografar':
                resultado_cripto = erro
            else:
                resultado_descripto = erro
        else:
            try:
                if acao == 'criptografar':
                    resultado_cripto = criptografar_texto(chave, texto)
                elif acao == 'descriptografar':
                    resultado_descripto = descriptografar_texto(chave, texto)
            except Exception as e:
                if acao == 'criptografar':
                    resultado_cripto = f"Erro: {str(e)}"
                else:
                    resultado_descripto = f"Erro: {str(e)}"

    return render_template('index.html', 
                           resultado_cripto=resultado_cripto, 
                           resultado_descripto=resultado_descripto)

if __name__ == '__main__':
    app.run(debug=True)
