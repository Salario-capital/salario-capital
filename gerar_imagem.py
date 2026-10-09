
import json
import os
import re
import html
import uuid
import hashlib
import unicodedata

BASE_URL = (
    "https://salario-capital.github.io/"
    "salario-capital/imagens/"
)

with open("artigo_atual.json", "r", encoding="utf-8") as f:
    artigo = json.load(f)

titulo = artigo["titulo"].strip()
tema = artigo.get("tema", "").strip()

# Cria um nome exclusivo para esta imagem.
slug = unicodedata.normalize("NFKD", titulo)
slug = slug.encode("ascii", "ignore").decode("ascii").lower()
slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
slug = (slug[:45] or "artigo").rstrip("-")

identificador = uuid.uuid4().hex[:8]
nome_base = f"artigo-{slug}-{identificador}"

arquivo_svg = f"imagens/{nome_base}.svg"
arquivo_jpg = f"imagens/{nome_base}.jpg"

# O hash acrescenta uma variação visual baseada no tema e no título.
hash_visual = hashlib.sha256(
    f"{titulo}|{tema}".encode("utf-8")
).hexdigest()

cor_destaque = (
    "#28C76F" if int(hash_visual[0], 16) % 2 == 0
    else "#45B7D1"
)

texto = re.sub(r"[^\w\sÀ-ÿ]", "", titulo, flags=re.UNICODE)
palavras = texto.split()
linha1 = html.escape(" ".join(palavras[:5]))
linha2 = html.escape(" ".join(palavras[5:10]))

if not linha2:
    linha2 = html.escape(tema[:35])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="1200" height="630" viewBox="0 0 1200 630">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#071A2B"/>
    <stop offset="100%" stop-color="#123B5D"/>
  </linearGradient>
  <linearGradient id="chart" x1="0" y1="1" x2="1" y2="0">
    <stop offset="0%" stop-color="{cor_destaque}"/>
    <stop offset="100%" stop-color="#7BE495"/>
  </linearGradient>
</defs>

<rect width="1200" height="630" fill="url(#bg)"/>
<circle cx="1040" cy="110" r="150"
        fill="#FFFFFF" opacity="0.04"/>
<circle cx="1110" cy="510" r="220"
        fill="{cor_destaque}" opacity="0.10"/>

<polyline
  points="700,470 790,400 850,425 930,320 1010,350 1090,230"
  fill="none" stroke="url(#chart)" stroke-width="14"
  stroke-linecap="round" stroke-linejoin="round"/>

<circle cx="1090" cy="230" r="12" fill="#7BE495"/>
<circle cx="790" cy="185" r="55" fill="{cor_destaque}"/>

<text x="790" y="205" text-anchor="middle"
      font-family="Arial, sans-serif" font-size="58"
      font-weight="bold" fill="white">R$</text>

<text x="90" y="120" font-family="Arial, sans-serif"
      font-size="28" font-weight="bold"
      fill="#7BE495" letter-spacing="3">SALÁRIO CAPITAL</text>

<text x="90" y="245" font-family="Arial, sans-serif"
      font-size="48" font-weight="bold"
      fill="white">{linha1}</text>

<text x="90" y="310" font-family="Arial, sans-serif"
      font-size="48" font-weight="bold"
      fill="white">{linha2}</text>

<text x="90" y="535" font-family="Arial, sans-serif"
      font-size="24" fill="#D7E3EC">
  Finanças • Investimentos • Economia
</text>
</svg>'''

os.makedirs("imagens", exist_ok=True)

# Salva a imagem exclusiva e também a versão de visualização atual.
with open(arquivo_svg, "w", encoding="utf-8") as f:
    f.write(svg)

with open("imagens/artigo_atual.svg", "w", encoding="utf-8") as f:
    f.write(svg)

artigo["imagem_svg_arquivo"] = arquivo_svg
artigo["imagem_jpg_arquivo"] = arquivo_jpg
artigo["imagem_svg_url"] = BASE_URL + f"{nome_base}.svg"
artigo["imagem_jpg_url"] = BASE_URL + f"{nome_base}.jpg"

# Atualiza a imagem incorporada no HTML do artigo.
conteudo = artigo.get("conteudo", "")
conteudo = re.sub(
    r'https://salario-capital\.github\.io/'
    r'salario-capital/imagens/artigo_atual\.svg',
    artigo["imagem_svg_url"],
    conteudo
)
artigo["conteudo"] = conteudo

with open("artigo_atual.json", "w", encoding="utf-8") as f:
    json.dump(artigo, f, ensure_ascii=False, indent=2)

# Atualiza o último artigo do histórico.
try:
    with open("artigos.json", "r", encoding="utf-8") as f:
        historico = json.load(f)

    if historico.get("artigos"):
        ultimo = historico["artigos"][-1]
        ultimo["conteudo"] = re.sub(
            r'https://salario-capital\.github\.io/'
            r'salario-capital/imagens/artigo_atual\.svg',
            artigo["imagem_svg_url"],
            ultimo.get("conteudo", "")
        )
        ultimo["imagem_svg_url"] = artigo["imagem_svg_url"]
        ultimo["imagem_jpg_url"] = artigo["imagem_jpg_url"]

    with open("artigos.json", "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

except FileNotFoundError:
    print("Aviso: artigos.json não foi encontrado.")

print("IMAGEM EXCLUSIVA GERADA!")
print("SVG:", arquivo_svg)
print("JPG previsto:", arquivo_jpg)
print("URL:", artigo["imagem_svg_url"])
