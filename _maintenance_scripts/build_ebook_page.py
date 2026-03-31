import os
import re

with open(r'c:\Projetos\ZHC\website\guia\cultivoapp-tutorial.html', 'r', encoding='utf-8') as f:
    html = f.read()

head_match = re.search(r'(<head>.*?</head>)', html, re.DOTALL)
header_match = re.search(r'(<header class="site-header">.*?</header>)', html, re.DOTALL)
footer_match = re.search(r'(<footer class="site-footer">.*?</html>)', html, re.DOTALL)

head = head_match.group(1).replace('CultivoApp — Guia Completo de Uso', 'E-Book O Efeito Entourage — Preview') if head_match else ''
# Adicionar CSS premium ao head
custom_styles = """
    <style>
        :root {
            --ebook-primary: #52b778;
            --ebook-dark: #06110f;
            --ebook-card: #0d1f14;
            --ebook-text: #e8f0e9;
            --ebook-accent: #2da15f;
            --glass-bg: rgba(13, 31, 20, 0.7);
            --glass-border: rgba(82, 183, 120, 0.2);
        }
        
        .ebook-landing {
            background-color: var(--ebook-dark);
            color: var(--ebook-text);
            font-family: 'Inter', system-ui, sans-serif;
        }

        .ebook-hero {
            position: relative;
            padding: 8rem 2rem 6rem;
            text-align: center;
            background: radial-gradient(circle at 50% 100%, #0d2b1c 0%, var(--ebook-dark) 80%);
            overflow: hidden;
        }
        
        .ebook-hero::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: url('../assets/efeito_entourage.jpg') center/cover;
            opacity: 0.05;
            z-index: 0;
        }

        .ebook-hero-content {
            position: relative;
            z-index: 1;
            max-width: 800px;
            margin: 0 auto;
        }

        .ebook-title {
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #fff 0%, var(--ebook-primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .ebook-subtitle {
            font-size: 1.25rem;
            color: rgba(232, 240, 233, 0.8);
            margin-bottom: 2.5rem;
            line-height: 1.6;
        }

        .ebook-cta {
            display: inline-block;
            background: var(--ebook-primary);
            color: #fff;
            padding: 1rem 2.5rem;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1rem;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(82, 183, 120, 0.4);
        }

        .ebook-cta:hover {
            background: var(--ebook-accent);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(82, 183, 120, 0.6);
        }

        .preview-section {
            padding: 6rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
        }

        .section-header {
            text-align: center;
            margin-bottom: 4rem;
        }

        .section-header h2 {
            font-size: 2.5rem;
            color: var(--ebook-primary);
            margin-bottom: 1rem;
        }

        .preview-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 3rem;
            align-items: center;
        }

        .preview-card {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }

        .preview-card:hover {
            transform: translateY(-5px);
            border-color: rgba(82, 183, 120, 0.4);
        }

        .preview-image-wrapper {
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-bottom: 1.5rem;
        }

        .preview-image-wrapper img {
            width: 100%;
            display: block;
            transition: transform 0.5s ease;
        }

        .preview-card:hover .preview-image-wrapper img {
            transform: scale(1.02);
        }

        .preview-info h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #fff;
        }

        .preview-info p {
            color: rgba(232, 240, 233, 0.7);
            line-height: 1.5;
        }
        
        .cta-bottom {
            text-align: center;
            padding: 6rem 2rem;
            background: linear-gradient(180deg, var(--ebook-dark) 0%, #081a12 100%);
        }

    </style>
</head>"""
if head:
    head = head.replace('</head>', custom_styles)

header = header_match.group(1) if header_match else ''
footer = footer_match.group(1) if footer_match else ''

body_content = f"""
<body class="ebook-landing">
{header}
<main>
    <section class="ebook-hero">
        <div class="ebook-hero-content">
            <h1 class="ebook-title">O Efeito Entourage</h1>
            <p class="ebook-subtitle">
                Desvende a ciência por trás da sinergia entre canabinoides e terpenos. Um guia definitivo e ricamente embasado para maximizar o potencial terapêutico da Cannabis Medicinal.
            </p>
            <a href="#preview" class="ebook-cta">Visualizar Amostra Grátis</a>
        </div>
    </section>

    <section id="preview" class="preview-section">
        <div class="section-header">
            <h2>Por dentro do E-Book</h2>
            <p style="color: rgba(232,240,233,0.7); max-width: 600px; margin: 0 auto;">Confira algumas páginas exclusivas da nossa edição premium e descubra o padrão científico Flor de Minas.</p>
        </div>

        <div class="preview-grid">
            <!-- Capa -->
            <div class="preview-card">
                <div class="preview-image-wrapper">
                    <img src="../assets/prints_Ebook/ebook_page_0.png" alt="Capa Oficial do Ebook">
                </div>
                <div class="preview-info">
                    <h3>Capa & Apresentação</h3>
                    <p>Design premium que reflete a seriedade e o rigor científico do conteúdo elaborado pela nossa equipe de especialistas.</p>
                </div>
            </div>

            <!-- Sumário -->
            <div class="preview-card">
                <div class="preview-image-wrapper">
                    <img src="../assets/prints_Ebook/ebook_page_3.png" alt="Índice Analítico">
                </div>
                <div class="preview-info">
                    <h3>Índice Analítico</h3>
                    <p>Uma jornada estruturada de aprendizado, passando da teoria do Sistema Endocanabinoide até aplicações clínicas avançadas.</p>
                </div>
            </div>
            
            <!-- Capítulo 1 -->
            <div class="preview-card">
                <div class="preview-image-wrapper">
                    <img src="../assets/prints_Ebook/ebook_page_6.png" alt="A Ciência da Cannabis">
                </div>
                <div class="preview-info">
                    <h3>Fundamentos Científicos</h3>
                    <p>Mergulhe na base de como os fitocanabinoides interagem com nossos receptores CB1 e CB2 de forma sinérgica.</p>
                </div>
            </div>

            <!-- Terpenos -->
            <div class="preview-card">
                <div class="preview-image-wrapper">
                    <img src="../assets/prints_Ebook/ebook_page_28.png" alt="Exemplo prático de terpenos">
                </div>
                <div class="preview-info">
                    <h3>Catálogo de Terpenos</h3>
                    <p>Análises detalhadas dos principais terpenos da cannabis, como o Mirceno, abordando seus perfis aromáticos e terapêuticos.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="cta-bottom">
        <h2 style="font-size: 2.5rem; margin-bottom: 1.5rem; color: #fff;">Pronto para transformar seu tratamento?</h2>
        <p style="color: rgba(232,240,233,0.8); margin-bottom: 2.5rem; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.6;">
            Adquira o conhecimento necessário para entender as associações entre os compostos da Cannabis e alcance uma terapia altamente otimizada.
        </p>
        <a href="https://pay.flordeminas.com.br/entourage" class="ebook-cta" style="padding: 1.2rem 3rem; font-size: 1.2rem;">Garantir Meu E-Book Agora</a>
    </section>
</main>
{footer}
"""

with open(r'c:\Projetos\ZHC\website\guia\ebook-entourage.html', 'w', encoding='utf-8') as f:
    f.write(f'<!DOCTYPE html>\n<html lang="pt-BR">\n{head}\n{body_content}')
print("Página do E-Book Recriada com Sucesso Total!")
