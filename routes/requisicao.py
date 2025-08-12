from flask import Blueprint, render_template, request, redirect, flash, jsonify
from models.database import conectar_bd

requisicao_bp = Blueprint("requisicao", __name__)

@requisicao_bp.route("/")
def index():
    return render_template("cadastroREQ.html")

@requisicao_bp.route("/cadastrar", methods=["POST"])
def cadastrar_requisicao():
    dados = request.form
    conexao = conectar_bd()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO requisicoes (
                tipo_documento, numero_documento, numero_requisicao, data_requisicao,
                unidade_solicitante, solicitante, tipo_equipamento,
                outros_equipamentos, quantidade_equipamentos, tipo_exame, outros_exames,
                data_recebimento, numero_protocolo, numero_caso,
                objetivo_pericia, nivel_prioridade, local_armazenamento, prateleira, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dados["tipo_documento"], dados["numero_documento"], dados["numero_requisicao"], dados["data_requisicao"],
            dados["unidade_solicitante"], dados["solicitante"], dados["tipo_equipamento"],
            dados.get("outros_equipamentos", ""), dados["quantidade_equipamentos"],
            dados["tipo_exame"], dados.get("outros_exames", ""),
            dados["data_recebimento"], dados["numero_protocolo"], dados["numero_caso"],
            dados["objetivo_pericia"], dados["nivel_prioridade"],
            dados["local_armazenamento"], dados["prateleira"], dados["status"]
        ))

        conexao.commit()
        flash("Requisição cadastrada com sucesso!", "success")
        return redirect("/")  

    except Exception as e:
        conexao.rollback()  
        flash(f"Erro ao cadastrar requisição: {str(e)}", "error")
        return redirect("/")  

    finally:
        conexao.close() 
        
@requisicao_bp.route("/buscar")
def pagina_buscar():
    return render_template("buscaREQ.html")

# Rota para buscar requisições (API)
@requisicao_bp.route("/buscar", methods=["GET"])
def buscar_requisicoes():
    
    numero_requisicao = request.args.get("numero_requisicao")
    status = request.args.get("status")
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    conexao = conectar_bd()
    cursor = conexao.cursor()

   
    query = "SELECT * FROM requisicoes WHERE 1=1"
    params = []

    if numero_requisicao:
        query += " AND numero_requisicao LIKE ?"
        params.append(f"%{numero_requisicao}%")
    if status:
        query += " AND status = ?"
        params.append(status)
    if data_inicio and data_fim:
        query += " AND data_requisicao BETWEEN ? AND ?"
        params.extend([data_inicio, data_fim])

    cursor.execute(query, params)
    requisicoes = cursor.fetchall()

    conexao.close()

    # Retornar os resultados em formato JSON
    return jsonify(requisicoes)


  