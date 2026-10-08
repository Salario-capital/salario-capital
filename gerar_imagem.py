import json
import os
import re
import html

# Lê o artigo atual
with open("artigo_atual.json", "r", encoding="utf-8") as f:
    artigo = json.load(f)

titulo = artigo["titulo"]

# Texto curto para a imagem
texto = re.sub(r"[^\w\sÀ-ÿ]", "", titulo, flags=re.UNICODE)
palavras = texto.split()
linha1 = " ".join(palavras[:5])
linha2 = " ".join(palavras[5:10])

linha1 = html.escape(linha1)
linha2 = html.escape(linha2)

# SVG moderno de finanças
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#071A2B"/>
        <stop offset="100%" stop-color="#123B5D"/>
    </linearGradient>
    <linearGradient id="chart" x1="0" y1="1" x2="1" y2="0">
        <stop offset="0%" stop-color="#28C76F"/>
        <stop offset="100%" stop-color="#7BE495"/>
    </linearGradient>
</defs>

<rect width="1200" height="630" fill="url(#bg)"/>

<!-- elementos decorativos -->
<circle cx="1040" cy="110" r="150" fill="#FFFFFF" opacity="0.04"/>
<circle cx="1110" cy="510" r="220" fill="#28C76F" opacity="0.05"/>

<!-- gráfico -->
<polyline
    points="700,470 790,400 850,425 930,320 1010,350 1090,230"
    fill="none"
    stroke="url(#chart)"
    stroke-width="14"
    stroke-linecap="round"
    stroke-linejoin="round"/>

<circle cx="1090" cy="230" r="12" fill="#7BE495"/>

<!-- moedas -->
<circle cx="790" cy="185" r="55" fill="#28C76F" opacity="0.9"/>
<text x="790" y="205"
      text-anchor="middle"
      font-family="Arial, sans-serif"
      font-size="58"
      font-weight="bold"
      fill="white">R$</text>

<!-- título -->
<text x="90" y="120"
      font-family="Arial, sans-serif"
      font-size="28"
      font-weight="bold"
      fill="#7BE495"
      letter-spacing="3">SALÁRIO CAPITAL</text>

<text x="90" y="245"
      font-family="Arial, sans-serif"
      font-size="48"
      font-weight="bold"
      fill="white">{linha1}</text>

<text x="90" y="310"
      font-family="Arial, sans-serif"
      font-size="48"
      font-weight="bold"
      fill="white">{linha2}</text>

<text x="90" y="535"
      font-family="Arial, sans-serif"
      font-size="24"
      fill="#D7E3EC">Finanças • Investimentos • Economia</text>

</svg>'''

os.makedirs("imagens", exist_ok=True)

with open("imagens/artigo_atual.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("IMAGEM GERADA COM SUCESSO!")
print("Arquivo: imagens/artigo_atual.svg")
